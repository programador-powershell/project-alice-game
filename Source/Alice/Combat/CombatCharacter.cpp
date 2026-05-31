#include "Combat/CombatCharacter.h"
#include "Combat/StatComponent.h"
#include "Combat/HitboxComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimMontage.h"
#include "Engine/World.h"
#include "TimerManager.h"

ACombatCharacter::ACombatCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	Stats = CreateDefaultSubobject<UStatComponent>(TEXT("Stats"));
	Hitbox = CreateDefaultSubobject<UHitboxComponent>(TEXT("Hitbox"));

	VisualMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VisualMesh"));
	VisualMesh->SetupAttachment(GetCapsuleComponent());
	VisualMesh->SetRelativeLocation(FVector(0.f, 0.f, -90.f));
	VisualMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.f, 540.f, 0.f);
	bUseControllerRotationYaw = false;
}

float ACombatCharacter::NowSeconds() const
{
	const UWorld* W = GetWorld();
	return W ? W->GetTimeSeconds() : 0.f;
}

void ACombatCharacter::BeginPlay()
{
	Super::BeginPlay();

	if (Stats)
	{
		Stats->OnDeath.AddDynamic(this, &ACombatCharacter::HandleDeath);
		Stats->OnPostureBreak.AddDynamic(this, &ACombatCharacter::HandlePostureBreak);
	}
	if (Hitbox)
	{
		Hitbox->Mesh = GetMesh();
	}
	if (VisualMesh && VisualMeshAsset)
	{
		VisualMesh->SetStaticMesh(VisualMeshAsset);
		VisualMesh->SetRelativeScale3D(FVector(VisualMeshScale));
	}
	VisualBaseLoc = VisualMesh ? VisualMesh->GetRelativeLocation() : FVector(0.f, 0.f, -90.f);
}

void ACombatCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (!VisualMesh)
	{
		return;
	}
	AnimTime += DeltaSeconds;

	if (bDead)
	{
		DeathLean = FMath::FInterpTo(DeathLean, 82.f, DeltaSeconds, 3.5f);
		VisualMesh->SetRelativeRotation(FRotator(DeathLean, 0.f, 0.f));
		VisualMesh->SetRelativeLocation(VisualBaseLoc - FVector(0.f, 0.f, FMath::Sin(FMath::DegreesToRadians(DeathLean)) * 38.f));
		return;
	}

	FVector Loc = VisualBaseLoc;
	FRotator Rot = FRotator::ZeroRotator;

	// Idle / locomotion bob + sway, scaled by ground speed.
	const float SpeedA = FMath::Clamp(GetVelocity().Size2D() / 600.f, 0.f, 1.f);
	const float BobFreq = FMath::Lerp(2.2f, 10.f, SpeedA);
	const float BobAmp = FMath::Lerp(1.5f, 5.5f, SpeedA);
	Loc.Z += FMath::Sin(AnimTime * BobFreq) * BobAmp;
	Rot.Roll += FMath::Sin(AnimTime * BobFreq * 0.5f) * FMath::Lerp(1.5f, 6.f, SpeedA);

	// Attack: lunge forward + lean into the swing.
	AttackBlend = FMath::FInterpTo(AttackBlend, bAttacking ? 1.f : 0.f, DeltaSeconds, bAttacking ? 20.f : 9.f);
	Loc.X += AttackBlend * 28.f;
	Rot.Pitch += AttackBlend * -32.f;

	// Rose Drift tumble.
	if (DodgeRollTime > 0.f)
	{
		DodgeRollTime = FMath::Max(0.f, DodgeRollTime - DeltaSeconds);
		const float Frac = 1.f - (DodgeRollTime / FMath::Max(0.01f, DodgeRollDur));
		Rot.Roll += Frac * 360.f;
		Loc.Z -= FMath::Sin(Frac * PI) * 18.f;
	}

	// Hit recoil.
	if (HitRecoil > 0.f)
	{
		HitRecoil = FMath::Max(0.f, HitRecoil - DeltaSeconds * 3.f);
		Rot.Pitch += HitRecoil * 24.f;
		Loc.X -= HitRecoil * 12.f;
	}

	VisualMesh->SetRelativeLocation(Loc);
	VisualMesh->SetRelativeRotation(Rot);
}

void ACombatCharacter::OnConstruction(const FTransform& Transform)
{
	Super::OnConstruction(Transform);
	if (VisualMesh && VisualMeshAsset)
	{
		VisualMesh->SetStaticMesh(VisualMeshAsset);
		VisualMesh->SetRelativeScale3D(FVector(VisualMeshScale));
	}
}

void ACombatCharacter::Attack()
{
	if (bDead || bGroggy)
	{
		return;
	}
	if (!AttackCombo)
	{
		// Static-mesh fallback: code-driven timed swing, no montage required.
		if (bAttacking) return;
		if (!Stats || !Stats->SpendStamina(AttackStaminaCost)) return;
		bAttacking = true;
		if (Hitbox) { Hitbox->BeginWindow(); }
		GetWorldTimerManager().SetTimer(NoAnimAttackTimer, this, &ACombatCharacter::EndNoAnimAttack, AttackNoAnimDuration, false);
		return;
	}
	if (bAttacking)
	{
		if (bComboWindowOpen)
		{
			bAttackQueued = true;
		}
		return;
	}
	if (!Stats || !Stats->SpendStamina(AttackStaminaCost))
	{
		return;
	}
	bAttacking = true;
	ComboIndex = 0;
	PlayComboSection(ComboIndex);
}

void ACombatCharacter::PlayComboSection(int32 Index)
{
	UAnimInstance* AnimInst = GetMesh() ? GetMesh()->GetAnimInstance() : nullptr;
	if (!AnimInst || !AttackCombo)
	{
		bAttacking = false;
		return;
	}

	if (!AnimInst->Montage_IsPlaying(AttackCombo))
	{
		AnimInst->Montage_Play(AttackCombo);
		FOnMontageEnded EndDel;
		EndDel.BindUObject(this, &ACombatCharacter::OnAttackMontageEnded);
		AnimInst->Montage_SetEndDelegate(EndDel, AttackCombo);
	}

	const FName Section(*FString::Printf(TEXT("Combo%d"), Index));
	AnimInst->Montage_JumpToSection(Section, AttackCombo);
}

void ACombatCharacter::CloseComboWindow()
{
	bComboWindowOpen = false;
	if (bAttackQueued && bAttacking)
	{
		bAttackQueued = false;
		if (Stats && Stats->SpendStamina(AttackStaminaCost))
		{
			ComboIndex = (ComboIndex + 1) % FMath::Max(1, NumComboSections);
			PlayComboSection(ComboIndex);
		}
	}
}

void ACombatCharacter::OnAttackMontageEnded(UAnimMontage* Montage, bool bInterrupted)
{
	bAttacking = false;
	bComboWindowOpen = false;
	bAttackQueued = false;
	ComboIndex = 0;
}

void ACombatCharacter::Dodge(const FVector& WorldDir)
{
	if (bDead || bGroggy)
	{
		return;
	}
	if (GetCharacterMovement()->IsFalling())
	{
		return;
	}
	if (!Stats || !Stats->SpendStamina(DodgeStaminaCost))
	{
		return;
	}

	DodgeRollTime = DodgeRollDur;

	const FVector Dir = WorldDir.GetSafeNormal();
	if (!Dir.IsNearlyZero())
	{
		SetActorRotation(Dir.Rotation());
	}
	if (DodgeMontage)
	{
		PlayAnimMontage(DodgeMontage);
	}
	else
	{
		// No dodge animation — launch + timed i-frames (Rose Drift perfect-dodge still procs).
		bInvulnerable = true;
		LaunchCharacter(Dir * DodgeImpulse, true, false);
		GetWorldTimerManager().SetTimer(DodgeIFrameTimer, this, &ACombatCharacter::EndDodgeIFrames, DodgeIFrameTime, false);
	}
}

void ACombatCharacter::ReceiveHit_Implementation(const FHitData& Hit)
{
	if (bDead || bInvulnerable)
	{
		return; // dodge i-frames / dead
	}
	if (bBlocking)
	{
		ResolveGuard(Hit);
		return;
	}

	if (Stats)
	{
		Stats->ApplyDamage(Hit.Damage, Hit.PostureDamage);
	}

	HitRecoil = 1.f;
	DoHitStop(HitStopSeconds);

	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (HitShake)
		{
			PC->ClientStartCameraShake(HitShake);
		}
	}

	if (!bHyperArmor && !(Stats && Stats->IsDead()))
	{
		PlayHitReact(Hit.ImpactDir, Hit.Strength);
	}
}

void ACombatCharacter::ResolveGuard(const FHitData& Hit)
{
	if (Hit.bUnblockable)
	{
		if (Stats) { Stats->ApplyDamage(Hit.Damage, Hit.PostureDamage); }
		PlayHitReact(Hit.ImpactDir, Hit.Strength);
		return;
	}

	const float Since = NowSeconds() - GuardPressTime;
	if (Since <= PerfectGuardWindow)
	{
		// PERFECT GUARD: no HP damage, reflect posture onto attacker, spark.
		if (Hit.Instigator)
		{
			if (UStatComponent* AttStats = Hit.Instigator->FindComponentByClass<UStatComponent>())
			{
				AttStats->ApplyDamage(0.f, Hit.PostureDamage * 1.5f);
			}
		}
		DoHitStop(0.05f);
	}
	else
	{
		// Normal block: chip + stamina drain; guard-break if stamina runs out.
		if (Stats)
		{
			Stats->ApplyDamage(Hit.Damage * 0.3f, Hit.PostureDamage * 0.5f);
			if (!Stats->SpendStamina(15.f))
			{
				bBlocking = false;
				PlayHitReact(Hit.ImpactDir, EHitStrength::Heavy); // guard broken
			}
		}
	}
}

void ACombatCharacter::DoHitStop(float Seconds)
{
	CustomTimeDilation = 0.01f;
	GetWorldTimerManager().SetTimer(HitStopTimer, this, &ACombatCharacter::EndHitStop, FMath::Max(0.01f, Seconds), false);
}

void ACombatCharacter::EndHitStop()
{
	CustomTimeDilation = 1.f;
}

void ACombatCharacter::EndNoAnimAttack()
{
	if (Hitbox) { Hitbox->EndWindow(); }
	bAttacking = false;
}

void ACombatCharacter::EndDodgeIFrames()
{
	bInvulnerable = false;
}

void ACombatCharacter::PlayHitReact(const FVector& FromDir, EHitStrength Strength)
{
	if (HitReactMontage)
	{
		PlayAnimMontage(HitReactMontage);
	}
}

void ACombatCharacter::EnterGroggy()
{
	bGroggy = true;
	GetWorldTimerManager().SetTimer(GroggyTimer, this, &ACombatCharacter::ClearGroggy, 3.0f, false);
}

void ACombatCharacter::HandlePostureBreak()
{
	EnterGroggy();
}

void ACombatCharacter::HandleDeath()
{
	Die();
}

void ACombatCharacter::Die()
{
	if (bDead)
	{
		return;
	}
	bDead = true;

	if (UCapsuleComponent* Cap = GetCapsuleComponent())
	{
		Cap->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
	if (UCharacterMovementComponent* Move = GetCharacterMovement())
	{
		Move->DisableMovement();
		Move->StopMovementImmediately();
	}

	if (DeathMontage)
	{
		PlayAnimMontage(DeathMontage);
	}
}

void ACombatCharacter::Revive()
{
	bDead = false;
	bGroggy = false;
	bInvulnerable = false;

	if (UCapsuleComponent* Cap = GetCapsuleComponent())
	{
		Cap->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	}
	if (UCharacterMovementComponent* Move = GetCharacterMovement())
	{
		Move->SetMovementMode(MOVE_Walking);
	}
	if (Stats)
	{
		Stats->RestoreFull();
	}
}
