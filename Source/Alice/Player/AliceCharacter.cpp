#include "Player/AliceCharacter.h"
#include "Player/DressComponent.h"
#include "Player/WeaponComponent.h"
#include "Combat/StatComponent.h"
#include "Combat/HitboxComponent.h"
#include "Combat/LockOnComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequence.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Components/CapsuleComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputActionValue.h"
#include "Components/InputComponent.h"
#include "NiagaraFunctionLibrary.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"
#include "Game/AliceGameMode.h"
#include "Engine/StaticMeshActor.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Enemy/EnemyCharacter.h"
#include "EngineUtils.h"

AAliceCharacter::AAliceCharacter()
{
	// Third-person camera: spring arm on the capsule, fixed length, no collision collapse.
	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(GetCapsuleComponent());
	CameraBoom->TargetArmLength = 400.f;
	CameraBoom->SocketOffset = FVector(0.f, 0.f, 90.f);   // raise pivot to shoulder height
	CameraBoom->bUsePawnControlRotation = true;            // arm rotates with controller
	CameraBoom->bDoCollisionTest = false;                  // never collapse to 1st person
	CameraBoom->bEnableCameraLag = true;
	CameraBoom->CameraLagSpeed = 10.f;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;
	FollowCamera->FieldOfView = 80.f;

	// Player rotates to face movement; controller yaw drives the camera only.
	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	LockOn  = CreateDefaultSubobject<ULockOnComponent>(TEXT("LockOn"));
	Dresses = CreateDefaultSubobject<UDressComponent>(TEXT("Dresses"));
	Weapon  = CreateDefaultSubobject<UWeaponComponent>(TEXT("Weapon"));

	if (Stats)
	{
		Stats->MaxHP = 650.f; Stats->HP = 650.f; // player tuning vs enemies
		Stats->MaxStamina = 120.f; Stats->Stamina = 120.f;
	}
	if (Hitbox)
	{
		Hitbox->HitTemplate.Damage = 85.f;
		Hitbox->HitTemplate.PostureDamage = 35.f;
		Hitbox->ForwardReach = 200.f;
		Hitbox->bForceForwardArc = true;
	}
	if (GetMesh())
	{
		GetMesh()->SetRelativeLocationAndRotation(FVector(0.f, 0.f, -88.f), FRotator(0.f, -90.f, 0.f));
	}

	GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
	GetCharacterMovement()->BrakingDecelerationWalking = 2000.f;
	bUseControllerRotationYaw = false;
}

void AAliceCharacter::BeginPlay()
{
	Super::BeginPlay();

	// Camera from constructor (3rd-person boom on capsule). No runtime recreation —
	// that created a duplicate camera and broke the view. Just enforce safe settings.
	if (CameraBoom)
	{
		CameraBoom->TargetArmLength = 400.f;
		CameraBoom->bDoCollisionTest = false;
		CameraBoom->bUsePawnControlRotation = true;
		CameraBoom->SocketOffset = FVector(0.f, 0.f, 90.f);
	}
	if (GetMesh())
	{
		GetMesh()->SetRelativeLocationAndRotation(FVector(0.f, 0.f, -88.f), FRotator(0.f, -90.f, 0.f));
		GetMesh()->SetRelativeScale3D(FVector(1.f, 1.f, 1.f));
	}

	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (UEnhancedInputLocalPlayerSubsystem* Subsystem =
			ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PC->GetLocalPlayer()))
		{
			if (DefaultMappingContext)
			{
				Subsystem->AddMappingContext(DefaultMappingContext, 0);
			}
		}
	}

	if (GetMesh() && GetMesh()->GetSkeletalMeshAsset())
	{
		// Se ha um AnimBP atribuido (mesmo vazio), usa modo Blueprint -> habilita
		// AnimInstance valido -> Dynamic Montages no DefaultSlot dao crossfade suave.
		// Sem AnimBP, cai em SingleNode (troca seca, sem blend).
		if (GetMesh()->GetAnimClass())
		{
			GetMesh()->SetAnimationMode(EAnimationMode::AnimationBlueprint);
		}
		else
		{
			GetMesh()->SetAnimationMode(EAnimationMode::AnimationSingleNode);
		}
	}

	// Spawn dress mesh in runtime (NewObject) — independent of BP subobject regen.
	if (!DressMesh && DressMeshAsset && GetMesh())
	{
		DressMesh = NewObject<USkeletalMeshComponent>(this, TEXT("DressMeshRT"));
		DressMesh->SetupAttachment(GetMesh());
		DressMesh->SetSkeletalMeshAsset(DressMeshAsset);
		DressMesh->RegisterComponent();
		DressMesh->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
	}
	if (DressMesh && DressMesh->GetSkeletalMeshAsset() && GetMesh())
	{
		DressMesh->SetLeaderPoseComponent(GetMesh());
	}

	Base_Idle = Anim_Idle; Base_Run = Anim_Run;
	Base_Atk1 = Anim_Atk1; Base_Atk2 = Anim_Atk2; Base_Atk3 = Anim_Atk3;
	if (Dresses)
	{
		Dresses->OnDressChanged.AddDynamic(this, &AAliceCharacter::OnDressChangedHandler);
		Dresses->OnCorruptionChanged.AddDynamic(this, &AAliceCharacter::OnCorruptionChangedHandler);
		Dresses->OnDressTransform.AddDynamic(this, &AAliceCharacter::OnDressTransformHandler);
	}

	InitDressMID();
	ApplyDressLook(Dresses ? Dresses->Current : EDressType::None);
}

void AAliceCharacter::OnDressChangedHandler(EDressType NewDress)
{
	SetWeaponProfile(NewDress);  // grip + combo style + stance + reach per weapon
	if (Weapon) Weapon->Equip(static_cast<int32>(NewDress)); // faithful weapon mesh per dress
	ApplyDressLook(NewDress);   // recolor emissive/tint to the new dress
	TriggerDressShift();        // dissolve-reform shimmer = "o vestido muda"
	CurrentClip = nullptr; // force re-eval
}

void AAliceCharacter::SetWeaponProfile(EDressType D)
{
	FWeaponProfile P;
	switch (D)
	{
	case EDressType::Coelho:     // Punhal — estocada, 1 mão, rápido
		P.Grip = EWeaponGrip::OneHand; P.ComboHits = 4; P.DamageMult = 0.80f; P.PostureMult = 0.8f; P.Reach = 185.f; P.SpeedMult = 0.78f; P.bThrust = true; break;
	case EDressType::Cheshire:   // Adaga — empunhadura dupla, multi-hit rápido
		P.Grip = EWeaponGrip::Dual;    P.ComboHits = 5; P.DamageMult = 0.65f; P.PostureMult = 0.7f; P.Reach = 165.f; P.SpeedMult = 0.68f; break;
	case EDressType::Chapeleiro: // Cajado — longo alcance, estica (Wukong)
		P.Grip = EWeaponGrip::OneHand; P.ComboHits = 3; P.DamageMult = 1.00f; P.PostureMult = 1.0f; P.Reach = 360.f; P.SpeedMult = 1.05f; P.bExtends = true; break;
	case EDressType::Lagarta:    // Foice — corte e ceifar, arco largo, 1 mão
		P.Grip = EWeaponGrip::OneHand; P.ComboHits = 3; P.DamageMult = 1.15f; P.PostureMult = 1.1f; P.Reach = 290.f; P.SpeedMult = 1.05f; break;
	case EDressType::Rainha:     // Espadão — corte pesado, 2 mãos, lento
		P.Grip = EWeaponGrip::TwoHand; P.ComboHits = 3; P.DamageMult = 1.70f; P.PostureMult = 1.6f; P.Reach = 300.f; P.SpeedMult = 1.40f; break;
	default:                     // Faca — estocada + corte, 1 mão, equilibrada
		P.Grip = EWeaponGrip::OneHand; P.ComboHits = 3; P.DamageMult = 1.00f; P.PostureMult = 1.0f; P.Reach = 200.f; P.SpeedMult = 1.00f; P.bThrust = true; break;
	}
	WeaponProfile = P;

	if (P.Grip == EWeaponGrip::TwoHand)
	{
		Anim_Idle = Anim_GS_Idle ? Anim_GS_Idle : Base_Idle;
		Anim_Run  = Anim_GS_Run  ? Anim_GS_Run  : Base_Run;
		if (Anim_GS_Atk) { Anim_Atk1 = Anim_GS_Atk; Anim_Atk2 = Anim_GS_Atk; Anim_Atk3 = Anim_GS_Atk; }
	}
	else if (P.Grip == EWeaponGrip::Dual)
	{
		Anim_Idle = Base_Idle; Anim_Run = Base_Run;
		if (Anim_Dual_Atk) { Anim_Atk1 = Anim_Dual_Atk; Anim_Atk2 = Anim_Dual_Atk; Anim_Atk3 = Anim_Dual_Atk; }
	}
	else
	{
		Anim_Idle = Base_Idle; Anim_Run = Base_Run;
		Anim_Atk1 = Base_Atk1; Anim_Atk2 = Base_Atk2; Anim_Atk3 = Base_Atk3;
	}
	if (Hitbox) { Hitbox->ForwardReach = P.Reach; }
}

void AAliceCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);

	if (HeartCorruption > 0.f && !bDead)
	{
		HeartCorruption = FMath::Max(0.f, HeartCorruption - HeartDecayPerSec * DeltaSeconds);
	}

	USkeletalMeshComponent* M = GetMesh();
	if (!M || !M->GetSkeletalMeshAsset())
	{
		return; // static VisualMesh + procedural handled by Super::Tick
	}

	// --- Dress magic-shader drive (runs every frame, independent of anim path) ---
	if (DressMIDs.Num() > 0)
	{
		float DAmt = 0.f;
		if (DissolveTime > 0.f)
		{
			DissolveTime -= DeltaSeconds;
			const float F = 1.f - FMath::Clamp(DissolveTime / FMath::Max(0.01f, DissolveDur), 0.f, 1.f);
			DAmt = FMath::Sin(F * PI) * DissolvePeak; // 0 -> peak -> 0 over the shift
		}
		const float Pow = BaseEmissivePower + DAmt * 5.f; // flare brighter mid-shift
		for (UMaterialInstanceDynamic* Mid : DressMIDs)
		{
			if (!Mid) continue;
			Mid->SetScalarParameterValue(TEXT("DissolveAmount"), DAmt);
			Mid->SetScalarParameterValue(TEXT("EmissivePower"), Pow);
		}
	}
	// --- Run petal trail (Camada 6) ---
	if (!bDead && GetVelocity().Size2D() > 520.f)
	{
		TrailAccum += DeltaSeconds;
		if (TrailAccum >= 0.06f) { TrailAccum = 0.f; SpawnTrailPetal(); }
	}
	else { TrailAccum = 0.f; }

	const bool bHasClips = (Anim_Idle || Anim_Walk || Anim_Run || Anim_Attack || Anim_Dodge || Anim_Hit || Anim_Death);
	if (bHasClips)
	{
		// Real skeletal animation via SingleNode (when AnimSequences are assigned).
		UAnimSequence* Want = nullptr;
		bool bLoop = true;
		if (bDead)                                   { Want = Anim_Death;  bLoop = false; }
		else if (bAttacking && ActiveAttackClip)     { Want = ActiveAttackClip; bLoop = false; }
		else if (bAttacking && Anim_Attack)          { Want = Anim_Attack; bLoop = false; }
		else if (DodgeRollTime > 0.f && Anim_Dodge)  { Want = Anim_Dodge;  bLoop = false; }
		else if (bBlocking && Anim_Block)            { Want = Anim_Block;  bLoop = true; }
		else if (HitRecoil > 0.55f && Anim_Hit)      { Want = Anim_Hit;    bLoop = false; }
		else
		{
			const float S = GetVelocity().Size2D();
			Want = (S > 540.f && Anim_Run) ? Anim_Run : ((S > 40.f && Anim_Walk) ? Anim_Walk : Anim_Idle);
			bLoop = true;
		}
		if (Want && Want != CurrentClip)
		{
			CurrentClip = Want;
			// Crossfade real: com AnimInstance (AnimBP atribuido, mesmo vazio) toca o clip
			// como Dynamic Montage no DefaultSlot, com BlendIn/BlendOut -> transicao suave
			// idle<->walk<->run + ataques, sem o "loop travado" da troca seca de PlayAnimation.
			if (UAnimInstance* AnimInst = M->GetAnimInstance())
			{
				const bool bSharp = (bAttacking || DodgeRollTime > 0.f || bDead);
				const float BlendIn   = bSharp ? 0.06f : 0.20f;
				const float BlendOut  = bSharp ? 0.10f : 0.25f;
				const float LoopCount = bLoop ? 0.f : 1.f; // 0 = loop infinito
				AnimInst->PlaySlotAnimationAsDynamicMontage(
					Want, TEXT("DefaultSlot"), BlendIn, BlendOut, 1.f, LoopCount);
			}
			else
			{
				M->PlayAnimation(Want, bLoop);
			}
		}
		return;
	}

	// No AnimSequences yet -> drive the skeletal mesh rigidly so Eve still has life,
	// preserving the -90 facing. Reads shared anim state advanced by Super::Tick.
	const float SpeedA = FMath::Clamp(GetVelocity().Size2D() / 600.f, 0.f, 1.f);
	float BobZ = FMath::Sin(AnimTime * FMath::Lerp(2.2f, 10.f, SpeedA)) * FMath::Lerp(1.5f, 5.5f, SpeedA);
	float Roll = FMath::Sin(AnimTime * FMath::Lerp(1.1f, 5.f, SpeedA)) * FMath::Lerp(1.5f, 6.f, SpeedA);
	float Pitch = 0.f, Fwd = 0.f, Sink = 0.f;

	if (bDead)
	{
		Pitch = DeathLean;
		Sink = FMath::Sin(FMath::DegreesToRadians(DeathLean)) * 38.f;
	}
	else
	{
		Fwd = AttackBlend * 28.f;
		Pitch += AttackBlend * -32.f;
		if (DodgeRollTime > 0.f)
		{
			const float Frac = 1.f - (DodgeRollTime / FMath::Max(0.01f, DodgeRollDur));
			Roll += Frac * 360.f;
			Sink += FMath::Sin(Frac * PI) * 18.f;
		}
		if (HitRecoil > 0.f)
		{
			Pitch += HitRecoil * 24.f;
			Fwd -= HitRecoil * 12.f;
		}
	}

	M->SetRelativeLocation(FVector(Fwd, 0.f, -88.f + BobZ - Sink));
	M->SetRelativeRotation(FRotator(Pitch, -90.f, Roll));
}

void AAliceCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	// Legacy axis/action bindings (mappings in DefaultInput.ini) — robust for headless setup.
	PlayerInputComponent->BindAxis("MoveForward", this, &AAliceCharacter::MoveForward);
	PlayerInputComponent->BindAxis("MoveRight", this, &AAliceCharacter::MoveRight);
	PlayerInputComponent->BindAxis("Turn", this, &APawn::AddControllerYawInput);
	PlayerInputComponent->BindAxis("LookUp", this, &APawn::AddControllerPitchInput);
	PlayerInputComponent->BindAxis("CycleDress", this, &AAliceCharacter::AxisCycleDress);

	PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);
	PlayerInputComponent->BindAction("Jump", IE_Released, this, &ACharacter::StopJumping);
	PlayerInputComponent->BindAction("Sprint", IE_Pressed, this, &AAliceCharacter::OnSprintStart);
	PlayerInputComponent->BindAction("Sprint", IE_Released, this, &AAliceCharacter::OnSprintStop);
	PlayerInputComponent->BindAction("Attack", IE_Pressed, this, &AAliceCharacter::OnAttackInput);
	PlayerInputComponent->BindAction("Dodge", IE_Pressed, this, &AAliceCharacter::OnDodgeInput);
	PlayerInputComponent->BindAction("Guard", IE_Pressed, this, &AAliceCharacter::OnGuardStart);
	PlayerInputComponent->BindAction("Guard", IE_Released, this, &AAliceCharacter::OnGuardStop);
	PlayerInputComponent->BindAction("LockOn", IE_Pressed, this, &AAliceCharacter::OnLockOnInput);
	PlayerInputComponent->BindAction("Heal", IE_Pressed, this, &AAliceCharacter::OnHealInput);
	PlayerInputComponent->BindAction("Skill", IE_Pressed, this, &AAliceCharacter::OnSkillInput);
	PlayerInputComponent->BindAction("Interact", IE_Pressed, this, &AAliceCharacter::OnInteractInput);
}

void AAliceCharacter::OnMove(const FInputActionValue& V)
{
	const FVector2D Axis = V.Get<FVector2D>();
	if (!Controller) return;

	const FRotator YawRot(0.f, Controller->GetControlRotation().Yaw, 0.f);
	const FVector Fwd = FRotationMatrix(YawRot).GetUnitAxis(EAxis::X);
	const FVector Right = FRotationMatrix(YawRot).GetUnitAxis(EAxis::Y);

	AddMovementInput(Fwd, Axis.Y);
	AddMovementInput(Right, Axis.X);

	const FVector Combined = (Fwd * Axis.Y) + (Right * Axis.X);
	if (!Combined.IsNearlyZero())
	{
		LastMoveWorldDir = Combined.GetSafeNormal();
	}
}

void AAliceCharacter::OnLook(const FInputActionValue& V)
{
	const FVector2D Axis = V.Get<FVector2D>();
	AddControllerYawInput(Axis.X);
	AddControllerPitchInput(Axis.Y);
}

void AAliceCharacter::OnSprintStart() { GetCharacterMovement()->MaxWalkSpeed = SprintSpeed; }
void AAliceCharacter::OnSprintStop()  { GetCharacterMovement()->MaxWalkSpeed = WalkSpeed; }

void AAliceCharacter::OnAttackInput()  { PerformCombo(); }

void AAliceCharacter::PerformCombo()
{
	if (bDead || bGroggy) return;
	if (!Anim_Atk1) { Attack(); return; } // no combo clips -> base attack
	if (bAttacking) { bComboQueued = true; return; } // buffer next hit
	if (!Stats || !Stats->SpendStamina(AttackStaminaCost)) return;
	bAttacking = true;
	ComboStep = 0;
	DoComboStep(0);
}

void AAliceCharacter::DoComboStep(int32 Step)
{
	UAnimSequence* Clip = Anim_Atk1;
	if (Step == 1 && Anim_Atk2) Clip = Anim_Atk2;
	else if (Step >= 2 && Anim_Atk3) Clip = Anim_Atk3;
	ActiveAttackClip = Clip;
	CurrentClip = nullptr; // force Tick to (re)play the new clip
	if (Hitbox)
	{
		Hitbox->ForwardReach = WeaponProfile.Reach;
		Hitbox->HitTemplate.Damage = 85.f * WeaponProfile.DamageMult * (1.f + 0.12f * Step); // ramps through combo
		Hitbox->HitTemplate.PostureDamage = 35.f * WeaponProfile.PostureMult;
		Hitbox->bForceForwardArc = true;
		Hitbox->BeginWindow();
	}
	if (WeaponProfile.bThrust)
	{
		LaunchCharacter(GetActorForwardVector() * 430.f, true, false); // estocada (thrust lunge)
	}
	const float Spd = FMath::Max(0.3f, WeaponProfile.SpeedMult);
	GetWorldTimerManager().SetTimer(ComboActiveTimer, this, &AAliceCharacter::EndComboWindow, 0.30f * Spd, false);
	GetWorldTimerManager().SetTimer(ComboStepTimer, this, &AAliceCharacter::AdvanceCombo, 0.62f * Spd, false);
}

void AAliceCharacter::EndComboWindow()
{
	if (Hitbox) Hitbox->EndWindow();
}

void AAliceCharacter::AdvanceCombo()
{
	if (bComboQueued && ComboStep < WeaponProfile.ComboHits - 1)
	{
		bComboQueued = false;
		ComboStep++;
		if (Stats && Stats->SpendStamina(AttackStaminaCost * 0.7f))
		{
			DoComboStep(ComboStep);
			return;
		}
	}
	EndCombo();
}

void AAliceCharacter::EndCombo()
{
	bAttacking = false;
	bComboQueued = false;
	ComboStep = 0;
	ActiveAttackClip = nullptr;
}
void AAliceCharacter::OnDodgeInput()
{
	FVector Dir = FVector::ZeroVector;
	if (Controller)
	{
		const FRotator Yaw(0.f, Controller->GetControlRotation().Yaw, 0.f);
		const FVector F = FRotationMatrix(Yaw).GetUnitAxis(EAxis::X);
		const FVector R = FRotationMatrix(Yaw).GetUnitAxis(EAxis::Y);
		Dir = F * InputF + R * InputR;
	}
	if (Dir.IsNearlyZero()) Dir = -GetActorForwardVector();
	Dodge(Dir.GetSafeNormal());
}

void AAliceCharacter::MoveForward(float Value)
{
	InputF = Value;
	if (Controller && Value != 0.f)
	{
		const FRotator Yaw(0.f, Controller->GetControlRotation().Yaw, 0.f);
		AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::X), Value);
	}
}

void AAliceCharacter::MoveRight(float Value)
{
	InputR = Value;
	if (Controller && Value != 0.f)
	{
		const FRotator Yaw(0.f, Controller->GetControlRotation().Yaw, 0.f);
		AddMovementInput(FRotationMatrix(Yaw).GetUnitAxis(EAxis::Y), Value);
	}
}

void AAliceCharacter::AxisCycleDress(float Value)
{
	if (Dresses && FMath::Abs(Value) > 0.5f)
	{
		Dresses->CycleDress(Value);
	}
}
void AAliceCharacter::OnGuardStart() { StartBlock(); }
void AAliceCharacter::OnGuardStop()  { StopBlock(); }
void AAliceCharacter::OnLockOnInput() { if (LockOn) LockOn->Toggle(); }
void AAliceCharacter::OnCycleInput(const FInputActionValue& V)
{
	if (LockOn) LockOn->CycleTarget(V.Get<float>());
}
void AAliceCharacter::OnHealInput()    { Heal(); }
void AAliceCharacter::OnSkillInput()
{
	if (bDead || bGroggy || !Dresses) return;
	const EDressType D = Dresses->Current;
	if (Dresses->UseSkill())             // spends sanity + raises corruption (may transform)
	{
		CastDressSkill(D);               // the actual boss-power effect
		SpawnPetals(34);
		TriggerDressShift();
	}
}
void AAliceCharacter::OnInteractInput()
{
	// Checkpoint / interactable handled by overlap volumes broadcasting to the player.
	RestAtCheckpoint();
}
void AAliceCharacter::OnSwitchDressInput(const FInputActionValue& V)
{
	if (Dresses) Dresses->CycleDress(V.Get<float>());
}

FString AAliceCharacter::PetalMatPath() const
{
	const EDressType D = Dresses ? Dresses->Current : EDressType::None;
	switch (D)
	{
	case EDressType::Coelho:     return TEXT("/Game/Alice/Materials/M_GlowBlue");
	case EDressType::Cheshire:   return TEXT("/Game/Alice/Materials/M_GlowMagenta");
	case EDressType::Chapeleiro: return TEXT("/Game/Alice/Materials/M_GlowGreen");
	case EDressType::Lagarta:    return TEXT("/Game/Alice/Materials/M_GlowBlue");
	case EDressType::Rainha:     return TEXT("/Game/Alice/Materials/M_GlowRed");
	default:                     return TEXT("/Game/Alice/Materials/M_GlowMagenta");
	}
}

void AAliceCharacter::SpawnPetals(int32 N)
{
	if (!GetWorld()) return;
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (!Cube) return;
	UMaterialInterface* Mat = LoadObject<UMaterialInterface>(nullptr, *PetalMatPath());
	const FVector Base = GetActorLocation();
	for (int32 i = 0; i < N; ++i)
	{
		const FVector Dir = FVector(FMath::FRandRange(-1.f, 1.f), FMath::FRandRange(-1.f, 1.f), FMath::FRandRange(0.2f, 1.f)).GetSafeNormal();
		const FVector Loc = Base + FVector(0.f, 0.f, 60.f) + Dir * FMath::FRandRange(20.f, 120.f);
		FActorSpawnParameters Sp;
		Sp.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* A = GetWorld()->SpawnActor<AStaticMeshActor>(Loc, FRotator(FMath::FRandRange(0.f, 360.f), FMath::FRandRange(0.f, 360.f), FMath::FRandRange(0.f, 360.f)), Sp);
		if (!A) continue;
		A->SetActorEnableCollision(false);
		if (UStaticMeshComponent* MC = A->GetStaticMeshComponent())
		{
			MC->SetMobility(EComponentMobility::Movable);
			MC->SetStaticMesh(Cube);
			MC->SetWorldScale3D(FVector(0.06f, 0.12f, 0.012f));
			if (Mat) MC->SetMaterial(0, Mat);
			MC->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		}
		A->SetLifeSpan(0.9f);
	}
}

void AAliceCharacter::InitDressMID()
{
	DressMIDs.Reset();
	USkeletalMeshComponent* M = GetMesh();
	if (!M) return;
	// Force the dress master onto every slot at runtime (the SK asset ships with a
	// flat DefaultMaterial; this override is the reliable path), then drive via MID.
	UMaterialInterface* DressMat = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Alice/Materials/M_AliceDress"));
	const int32 N = FMath::Max(1, M->GetNumMaterials());
	for (int32 i = 0; i < N; ++i)
	{
		if (DressMat) M->SetMaterial(i, DressMat);
		if (UMaterialInstanceDynamic* Mid = M->CreateAndSetMaterialInstanceDynamic(i))
		{
			DressMIDs.Add(Mid);
		}
	}
}

void AAliceCharacter::ApplyDressLook(EDressType D)
{
	const float cf = Dresses ? Dresses->GetCurrentCorruption() / 100.f : 0.f;
	RefreshDressMaterial(D, cf);
}

void AAliceCharacter::RefreshDressMaterial(EDressType D, float CorruptFrac)
{
	FLinearColor Tint, Emis;
	float Power = 2.0f;
	switch (D)
	{
	case EDressType::Coelho:     Tint = FLinearColor(0.92f, 0.90f, 0.82f); Emis = FLinearColor(1.0f, 0.85f, 0.40f); Power = 2.2f; break; // branco/ouro
	case EDressType::Cheshire:   Tint = FLinearColor(0.55f, 0.30f, 0.60f); Emis = FLinearColor(1.0f, 0.20f, 0.85f); Power = 2.6f; break; // magenta
	case EDressType::Chapeleiro: Tint = FLinearColor(0.50f, 0.70f, 0.55f); Emis = FLinearColor(0.5f, 1.00f, 0.45f); Power = 2.4f; break; // verde-chá
	case EDressType::Lagarta:    Tint = FLinearColor(0.40f, 0.60f, 0.70f); Emis = FLinearColor(0.2f, 0.90f, 0.90f); Power = 2.4f; break; // teal-fumaça
	case EDressType::Rainha:     Tint = FLinearColor(0.55f, 0.12f, 0.14f); Emis = FLinearColor(1.0f, 0.12f, 0.18f); Power = 3.0f; break; // vermelho
	default:                     Tint = FLinearColor(0.60f, 0.72f, 0.92f); Emis = FLinearColor(0.7f, 0.85f, 1.00f); Power = 1.8f; break; // azul base
	}
	// Corruption (roteiro §6.1): cloth bruises toward near-black, emissive bleeds to
	// Cheshire purple, and the glow intensifies as the dress decays toward transformation.
	const float cf = FMath::Clamp(CorruptFrac, 0.f, 1.f);
	Tint = FMath::Lerp(Tint, FLinearColor(0.08f, 0.0f, 0.10f, 1.f), cf * 0.85f);
	Emis = FMath::Lerp(Emis, FLinearColor(0.65f, 0.0f, 0.95f, 1.f), cf * 0.80f);
	Power = Power + cf * 3.0f;

	BaseEmissivePower = Power;
	for (UMaterialInstanceDynamic* Mid : DressMIDs)
	{
		if (!Mid) continue;
		Mid->SetVectorParameterValue(TEXT("BaseTint"), Tint);
		Mid->SetVectorParameterValue(TEXT("EmissiveColor"), Emis);
		Mid->SetScalarParameterValue(TEXT("EmissivePower"), Power);
	}
}

void AAliceCharacter::OnCorruptionChangedHandler(EDressType D, float Corruption)
{
	if (D == Dresses->Current)
	{
		RefreshDressMaterial(D, Corruption / 100.f);
	}
}

void AAliceCharacter::DamageEnemiesInRadius(const FVector& Center, float Radius, float Dmg, float Posture, bool bCone, float ConeDot)
{
	if (!GetWorld()) return;
	const FVector Fwd = GetActorForwardVector();
	const float R2 = Radius * Radius;
	for (TActorIterator<AEnemyCharacter> It(GetWorld()); It; ++It)
	{
		AEnemyCharacter* E = *It;
		if (!E || E->IsDeadChar()) continue;
		const FVector Delta = E->GetActorLocation() - Center;
		if (Delta.SizeSquared() > R2) continue;
		if (bCone && FVector::DotProduct(Fwd, Delta.GetSafeNormal2D()) < ConeDot) continue;

		FHitData H;
		H.Damage = Dmg;
		H.PostureDamage = Posture;
		H.ImpactPoint = E->GetActorLocation();
		H.ImpactDir = Delta.GetSafeNormal();
		H.Strength = EHitStrength::Heavy;
		H.Instigator = this;
		IDamageable::Execute_ReceiveHit(E, H);
	}
}

void AAliceCharacter::CastDressSkill(EDressType D)
{
	const FVector Loc = GetActorLocation();
	switch (D)
	{
	case EDressType::Coelho: // Fracture do Tempo — freeze nearby enemies in slow-time
	{
		RestoreSlowedEnemies();
		for (TActorIterator<AEnemyCharacter> It(GetWorld()); It; ++It)
		{
			AEnemyCharacter* E = *It;
			if (!E || E->IsDeadChar()) continue;
			if (FVector::DistSquared(E->GetActorLocation(), Loc) > 2600.f * 2600.f) continue;
			E->CustomTimeDilation = 0.30f;
			SlowedEnemies.Add(E);
		}
		GetWorldTimerManager().SetTimer(TimeFractureTimer, this, &AAliceCharacter::RestoreSlowedEnemies, 3.0f, false);
		break;
	}
	case EDressType::Cheshire: // Passo Sombrio — dash + i-frames + brief invisibility
	{
		bInvulnerable = true;
		LaunchCharacter(GetActorForwardVector() * 1500.f + FVector(0, 0, 120.f), true, false);
		if (GetMesh()) GetMesh()->SetVisibility(false);
		GetWorldTimerManager().SetTimer(SkillStateTimer, this, &AAliceCharacter::EndSkillState, 0.9f, false);
		break;
	}
	case EDressType::Chapeleiro: // Rabisco do Caos — chaotic AoE nova around Alice
	{
		DamageEnemiesInRadius(Loc, 480.f, 130.f, 70.f, false, 0.f);
		SpawnPetals(40);
		break;
	}
	case EDressType::Lagarta: // Fumaça do Sonho — lingering dream-poison cloud
	{
		PoisonLoc = Loc;
		PoisonTicksLeft = 10; // ~5s of DoT
		GetWorldTimerManager().SetTimer(PoisonTimer, this, &AAliceCharacter::PoisonTick, 0.5f, true, 0.f);
		break;
	}
	case EDressType::Rainha: // Corte Real — heavy forward execution cut
	{
		LaunchCharacter(GetActorForwardVector() * 500.f, true, false);
		DamageEnemiesInRadius(Loc, 360.f, 220.f, 120.f, true, 0.2f);
		DoHitStop(0.14f);
		break;
	}
	default:
		break;
	}
}

void AAliceCharacter::PoisonTick()
{
	DamageEnemiesInRadius(PoisonLoc, 520.f, 24.f, 10.f, false, 0.f);
	// smoke puff at the cloud
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (Cube && GetWorld())
	{
		UMaterialInterface* Mat = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Alice/Materials/M_GlowBlue"));
		for (int32 i = 0; i < 4; ++i)
		{
			const FVector P = PoisonLoc + FVector(FMath::FRandRange(-220.f, 220.f), FMath::FRandRange(-220.f, 220.f), FMath::FRandRange(10.f, 160.f));
			FActorSpawnParameters Sp; Sp.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			if (AStaticMeshActor* A = GetWorld()->SpawnActor<AStaticMeshActor>(P, FRotator(FMath::FRandRange(0.f, 360.f), FMath::FRandRange(0.f, 360.f), 0.f), Sp))
			{
				A->SetActorEnableCollision(false);
				if (UStaticMeshComponent* MC = A->GetStaticMeshComponent())
				{
					MC->SetMobility(EComponentMobility::Movable);
					MC->SetStaticMesh(Cube);
					MC->SetWorldScale3D(FVector(0.9f, 0.9f, 0.9f));
					if (Mat) MC->SetMaterial(0, Mat);
					MC->SetCollisionEnabled(ECollisionEnabled::NoCollision);
				}
				A->SetLifeSpan(0.6f);
			}
		}
	}
	if (--PoisonTicksLeft <= 0)
	{
		GetWorldTimerManager().ClearTimer(PoisonTimer);
	}
}

void AAliceCharacter::RestoreSlowedEnemies()
{
	for (TWeakObjectPtr<AActor>& W : SlowedEnemies)
	{
		if (AActor* A = W.Get()) A->CustomTimeDilation = 1.f;
	}
	SlowedEnemies.Reset();
}

void AAliceCharacter::EndSkillState()
{
	bInvulnerable = false;
	if (GetMesh()) GetMesh()->SetVisibility(true);
}

void AAliceCharacter::OnDressTransformHandler(EDressType D)
{
	// 100% corruption -> signature transformation burst (roteiro §6.1).
	TriggerDressShift();
	SpawnPetals(64);
	DamageEnemiesInRadius(GetActorLocation(), 620.f, 200.f, 110.f, false, 0.f);
	bInvulnerable = true;
	GetWorldTimerManager().SetTimer(SkillStateTimer, this, &AAliceCharacter::EndSkillState, 0.8f, false);
}

void AAliceCharacter::TriggerDressShift()
{
	DissolveTime = DissolveDur; // Tick ramps DissolveAmount 0->peak->0 = magic reform
}

void AAliceCharacter::SpawnTrailPetal()
{
	if (!GetWorld()) return;
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (!Cube) return;
	UMaterialInterface* Mat = LoadObject<UMaterialInterface>(nullptr, *PetalMatPath());
	const FVector Loc = GetActorLocation() - GetActorForwardVector() * 22.f + FVector(0.f, 0.f, FMath::FRandRange(10.f, 55.f));
	FActorSpawnParameters Sp;
	Sp.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AStaticMeshActor* A = GetWorld()->SpawnActor<AStaticMeshActor>(Loc,
		FRotator(FMath::FRandRange(0.f, 360.f), FMath::FRandRange(0.f, 360.f), FMath::FRandRange(0.f, 360.f)), Sp);
	if (!A) return;
	A->SetActorEnableCollision(false);
	if (UStaticMeshComponent* MC = A->GetStaticMeshComponent())
	{
		MC->SetMobility(EComponentMobility::Movable);
		MC->SetStaticMesh(Cube);
		MC->SetWorldScale3D(FVector(0.05f, 0.10f, 0.01f));
		if (Mat) MC->SetMaterial(0, Mat);
		MC->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
	A->SetLifeSpan(0.5f);
}

void AAliceCharacter::Landed(const FHitResult& Hit)
{
	Super::Landed(Hit);
	SpawnPetals(14); // petal puff on landing (real cloth lift = Chaos Cloth, editor)
}

void AAliceCharacter::Dodge(const FVector& WorldDir)
{
	if (bDead || bGroggy || GetCharacterMovement()->IsFalling()) return;
	if (!Stats || Stats->Stamina < DodgeStaminaCost) return;

	LastDodgeTime = NowSeconds();

	if (RoseDriftPetals)
	{
		UNiagaraFunctionLibrary::SpawnSystemAttached(
			RoseDriftPetals, GetMesh(), NAME_None,
			FVector::ZeroVector, FRotator::ZeroRotator,
			EAttachLocation::SnapToTarget, true);
	}
	OnRoseDrift(WorldDir.GetSafeNormal(), false);
	SpawnPetals(18); // Rose Drift petal burst (per-dress color)

	Super::Dodge(WorldDir); // spends stamina + plays dodge montage (i-frame notify)
}

void AAliceCharacter::ReceiveHit_Implementation(const FHitData& Hit)
{
	// Perfect Rose Drift: an incoming hit lands inside our i-frame window right after a dodge.
	if (!bDead && bInvulnerable && (NowSeconds() - LastDodgeTime) <= PerfectDodgeWindow)
	{
		OnRoseDrift(Hit.ImpactDir * -1.f, true);
		UGameplayStatics::SetGlobalTimeDilation(this, PerfectDodgeTimeScale);

		FTimerDelegate Restore;
		Restore.BindLambda([this]() { UGameplayStatics::SetGlobalTimeDilation(this, 1.f); });
		GetWorldTimerManager().SetTimer(PerfectTimer, Restore, PerfectDodgeDuration, false);
		return; // hit negated
	}

	Super::ReceiveHit_Implementation(Hit);

	if (!bDead && !bInvulnerable && Hit.CorruptionBuildup > 0.f)
	{
		AddHeartCorruption(Hit.CorruptionBuildup); // Lídia's Corrupção do Coração
	}
}

void AAliceCharacter::AddHeartCorruption(float Amount)
{
	if (bDead || Amount <= 0.f) return;
	HeartCorruption = FMath::Clamp(HeartCorruption + Amount, 0.f, HeartCorruptionMax);
	if (HeartCorruption >= HeartCorruptionMax)
	{
		// Full build-up procs: burst damage + drains sanity/healing (roteiro §7).
		if (Stats)
		{
			Stats->ApplyDamage(140.f, 0.f);
			Stats->Sanity = FMath::Max(0.f, Stats->Sanity - 30.f);
		}
		SpawnPetals(40);
		HeartCorruption = 0.f;
	}
}

float AAliceCharacter::GetHeartCorruptionPercent() const
{
	return HeartCorruptionMax > 0.f ? HeartCorruption / HeartCorruptionMax : 0.f;
}

void AAliceCharacter::Heal()
{
	if (bDead || FlaskCharges <= 0 || !Stats) return;
	FlaskCharges--;
	Stats->Heal(FlaskHealAmount);
	if (HealMontage)
	{
		PlayAnimMontage(HealMontage);
	}
}

void AAliceCharacter::AddErgo(int32 Amount)  { Ergo += FMath::Max(0, Amount); }
bool AAliceCharacter::SpendErgo(int32 Amount)
{
	if (Ergo < Amount) return false;
	Ergo -= Amount;
	return true;
}

void AAliceCharacter::RestAtCheckpoint()
{
	AAliceGameMode* GM = Cast<AAliceGameMode>(UGameplayStatics::GetGameMode(this));
	if (GM && !GM->CanRest())
	{
		return; // only rest when standing at a checkpoint
	}
	if (Stats) Stats->RestoreFull();
	FlaskCharges = MaxFlaskCharges;
	if (GM) GM->OnPlayerRested();
}

void AAliceCharacter::HandleDeath()
{
	Super::HandleDeath();
	if (AAliceGameMode* GM = Cast<AAliceGameMode>(UGameplayStatics::GetGameMode(this)))
	{
		GM->OnPlayerDied(this);
	}
}
