#include "Enemy/BossCharacter.h"
#include "Combat/StatComponent.h"
#include "Combat/HitboxComponent.h"
#include "Combat/HitTypes.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Pawn.h"
#include "TimerManager.h"
#include "Engine/World.h"
#include "Engine/StaticMeshActor.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/OverlapResult.h"
#include "Engine/PointLight.h"
#include "Components/PointLightComponent.h"
#include "Materials/MaterialInterface.h"

ABossCharacter::ABossCharacter()
{
	if (Stats)
	{
		Stats->MaxHP = 3500.f; Stats->HP = 3500.f;
		Stats->MaxPosture = 220.f;
	}
	ErgoReward = 2500;
	AttackCooldown = 1.8f;
	if (Hitbox)
	{
		Hitbox->HitTemplate.Damage = 95.f;
		Hitbox->HitTemplate.PostureDamage = 28.f;
		Hitbox->ForwardReach = 230.f;
	}
}

void ABossCharacter::BeginPlay()
{
	Super::BeginPlay();

	if (Stats)
	{
		Stats->OnStatsChanged.AddDynamic(this, &ABossCharacter::OnStatsChangedHandler);
	}
	if (Hitbox)
	{
		Hitbox->OnHitDealt.AddDynamic(this, &ABossCharacter::OnHitDealtHandler);
	}
	Phase = 0;
}

void ABossCharacter::OnStatsChangedHandler(UStatComponent* InStats)
{
	if (!InStats) return;
	const float Pct = InStats->GetHPPercent();
	if (PhaseHPThresholds.IsValidIndex(Phase) && Pct <= PhaseHPThresholds[Phase])
	{
		EnterPhase(Phase + 1);
	}
}

void ABossCharacter::EnterPhase(int32 NewPhase)
{
	Phase = NewPhase;

	// Escalation: faster, harder-hitting, brief hyper-armor on transition.
	AttackCooldown = FMath::Max(0.8f, AttackCooldown - 0.35f);
	bHyperArmor = true;
	if (Stats)
	{
		Stats->Posture = 0.f; // reset stagger meter on phase change
	}

	SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 110.f), FLinearColor(1.f, 0.3f, 0.6f), 45000.f, 1500.f, 0.7f);
	OnPhaseChanged.Broadcast(Phase);
}

void ABossCharacter::OnHitDealtHandler(AActor* Target, const FHitData& Hit)
{
	if (bLifesteal && Stats && Target)
	{
		Stats->Heal(Hit.Damage * LifestealFraction);
	}
}

void ABossCharacter::Die()
{
	if (bDead) return;

	if (RewardDress != EDressType::None)
	{
		if (APawn* P = UGameplayStatics::GetPlayerPawn(this, 0))
		{
			if (UDressComponent* D = P->FindComponentByClass<UDressComponent>())
			{
				D->UnlockDress(RewardDress);
			}
		}
	}

	OnDefeated.Broadcast();
	Super::Die();

	if (!NextLevelName.IsNone())
	{
		GetWorldTimerManager().SetTimer(LevelTransitionTimer,
			FTimerDelegate::CreateLambda([this]() { UGameplayStatics::OpenLevel(this, NextLevelName); }),
			5.0f, false);
	}
}

void ABossCharacter::AddMove(FName N, float Mn, float Mx, float Wu, float Act, float Rec, float Dmg, float Reach, EBossAttackShape Sh, int32 Ph, bool Unb, float Corr)
{
	FBossAttack A;
	A.Name = N; A.MinRange = Mn; A.MaxRange = Mx; A.Windup = Wu; A.ActiveTime = Act; A.Recover = Rec;
	A.Damage = Dmg; A.Posture = Dmg * 0.32f; A.Reach = Reach; A.Shape = Sh; A.MinPhase = Ph; A.bUnblockable = Unb;
	A.CorruptionBuildup = Corr;
	Moveset.Add(A);
}

void ABossCharacter::PerformAttack()
{
	if (bBusy) return;
	if (Moveset.Num() == 0) { Super::PerformAttack(); return; }

	APawn* P = UGameplayStatics::GetPlayerPawn(this, 0);
	if (!P) return;
	const float Dist = FVector::Dist(GetActorLocation(), P->GetActorLocation());

	TArray<int32> Valid;
	for (int32 i = 0; i < Moveset.Num(); ++i)
	{
		const FBossAttack& M = Moveset[i];
		if (Phase >= M.MinPhase && Dist >= M.MinRange && Dist <= M.MaxRange)
		{
			Valid.Add(i);
		}
	}
	if (Valid.Num() == 0) return;
	StartMove(Valid[FMath::RandRange(0, Valid.Num() - 1)]);
}

void ABossCharacter::StartMove(int32 Idx)
{
	if (!Moveset.IsValidIndex(Idx)) return;
	bBusy = true;
	CurrentMove = Idx;
	bAttacking = true; // procedural wind/lean = part of the telegraph

	const FBossAttack& M = Moveset[Idx];
	if (APawn* P = UGameplayStatics::GetPlayerPawn(this, 0))
	{
		FVector D = P->GetActorLocation() - GetActorLocation(); D.Z = 0.f;
		if (!D.IsNearlyZero()) SetActorRotation(D.Rotation());
	}
	if (M.Shape == EBossAttackShape::RadialAoE)
	{
		SpawnTelegraph(M.Reach);
	}
	GetWorldTimerManager().SetTimer(MoveWindupTimer, this, &ABossCharacter::MoveExecute, FMath::Max(0.05f, M.Windup), false);
}

void ABossCharacter::MoveExecute()
{
	if (!Moveset.IsValidIndex(CurrentMove)) { MoveRecovered(); return; }
	const FBossAttack M = Moveset[CurrentMove];

	if (TelegraphActor) { TelegraphActor->Destroy(); TelegraphActor = nullptr; }

	APawn* P = UGameplayStatics::GetPlayerPawn(this, 0);
	if (P)
	{
		FVector D = P->GetActorLocation() - GetActorLocation(); D.Z = 0.f;
		if (!D.IsNearlyZero()) SetActorRotation(D.Rotation());
	}

	OnMoveExecuted(M);

	if (M.Shape == EBossAttackShape::RadialAoE)
	{
		DoRadialHit(M);
		SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 80.f), FLinearColor(1.f, 0.25f, 0.4f), 30000.f, M.Reach * 2.f, 0.40f);
		bAttacking = false;
		GetWorldTimerManager().SetTimer(MoveRecoverTimer, this, &ABossCharacter::MoveRecovered, FMath::Max(0.05f, M.Recover), false);
		return;
	}

	if (Hitbox)
	{
		Hitbox->HitTemplate.Damage = M.Damage;
		Hitbox->HitTemplate.PostureDamage = M.Posture;
		Hitbox->HitTemplate.bUnblockable = M.bUnblockable;
		Hitbox->HitTemplate.CorruptionBuildup = M.CorruptionBuildup;
		Hitbox->ForwardReach = M.Reach;
		Hitbox->bForceForwardArc = true;
		Hitbox->BeginWindow();
	}
	if (M.Shape == EBossAttackShape::Lunge && P)
	{
		FVector Dir = P->GetActorLocation() - GetActorLocation(); Dir.Z = 0.f; Dir = Dir.GetSafeNormal();
		LaunchCharacter(Dir * 1400.f + FVector(0.f, 0.f, 150.f), true, false);
	}
	GetWorldTimerManager().SetTimer(MoveActiveTimer, this, &ABossCharacter::MoveEndActive, FMath::Max(0.05f, M.ActiveTime), false);
}

void ABossCharacter::MoveEndActive()
{
	if (Hitbox) Hitbox->EndWindow();
	bAttacking = false;
	const float Rec = Moveset.IsValidIndex(CurrentMove) ? Moveset[CurrentMove].Recover : 0.8f;
	GetWorldTimerManager().SetTimer(MoveRecoverTimer, this, &ABossCharacter::MoveRecovered, FMath::Max(0.05f, Rec), false);
}

void ABossCharacter::MoveRecovered()
{
	bBusy = false;
	CurrentMove = -1;
}

void ABossCharacter::DoRadialHit(const FBossAttack& M)
{
	if (!GetWorld()) return;
	TArray<FOverlapResult> Ov;
	FCollisionQueryParams Q(SCENE_QUERY_STAT(BossAoE), false, this);
	GetWorld()->OverlapMultiByChannel(Ov, GetActorLocation(), FQuat::Identity, ECC_Pawn, FCollisionShape::MakeSphere(M.Reach), Q);
	for (const FOverlapResult& O : Ov)
	{
		AActor* A = O.GetActor();
		if (!A || A == this || !A->Implements<UDamageable>()) continue;
		FHitData H;
		H.Damage = M.Damage; H.PostureDamage = M.Posture; H.bUnblockable = M.bUnblockable; H.Instigator = this;
		H.CorruptionBuildup = M.CorruptionBuildup;
		H.ImpactPoint = A->GetActorLocation();
		H.ImpactDir = (A->GetActorLocation() - GetActorLocation()).GetSafeNormal();
		IDamageable::Execute_ReceiveHit(A, H);
		if (bLifesteal && Stats) Stats->Heal(M.Damage * LifestealFraction);
	}
}

void ABossCharacter::SpawnTelegraph(float Radius)
{
	UStaticMesh* Cyl = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	if (!Cyl || !GetWorld()) return;
	FActorSpawnParameters Sp;
	Sp.Owner = this;
	Sp.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AStaticMeshActor* A = GetWorld()->SpawnActor<AStaticMeshActor>(GetActorLocation() + FVector(0.f, 0.f, 6.f), FRotator::ZeroRotator, Sp);
	if (!A) return;
	A->SetActorEnableCollision(false);
	if (UStaticMeshComponent* MC = A->GetStaticMeshComponent())
	{
		MC->SetMobility(EComponentMobility::Movable);
		MC->SetStaticMesh(Cyl);
		MC->SetWorldScale3D(FVector(Radius / 50.f, Radius / 50.f, 0.05f));
		MC->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
	TelegraphActor = A;
}

void ABossCharacter::OnMoveExecuted(const FBossAttack& M)
{
	if (M.Shape == EBossAttackShape::RadialAoE)
	{
		SpawnShards(22, ShardMaterialPath, 1.1f); // card/petal burst
	}
}

void ABossCharacter::SpawnBurst(const FVector& Loc, const FLinearColor& Color, float Intensity, float Radius, float Life)
{
	if (!GetWorld()) return;
	APointLight* L = GetWorld()->SpawnActor<APointLight>(Loc, FRotator::ZeroRotator);
	if (!L) return;
	if (UPointLightComponent* C = Cast<UPointLightComponent>(L->GetLightComponent()))
	{
		C->SetMobility(EComponentMobility::Movable);
		C->SetIntensity(Intensity);
		C->SetLightColor(Color);
		C->SetAttenuationRadius(Radius);
	}
	L->SetLifeSpan(Life);
}

void ABossCharacter::SpawnClones(int32 N, float Life)
{
	if (!GetWorld() || !VisualMesh) return;
	UStaticMesh* SrcMesh = VisualMesh->GetStaticMesh();
	if (!SrcMesh) return;
	for (int32 i = 0; i < N; ++i)
	{
		const float Ang = (360.f / FMath::Max(1, N)) * i;
		const FVector Off = FRotator(0.f, Ang, 0.f).Vector() * 240.f;
		FActorSpawnParameters Sp;
		Sp.Owner = this;
		Sp.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* C = GetWorld()->SpawnActor<AStaticMeshActor>(GetActorLocation() + Off, GetActorRotation(), Sp);
		if (!C) continue;
		C->SetActorEnableCollision(false);
		if (UStaticMeshComponent* MC = C->GetStaticMeshComponent())
		{
			MC->SetMobility(EComponentMobility::Movable);
			MC->SetStaticMesh(SrcMesh);
			MC->SetWorldScale3D(FVector(VisualMeshScale));
		}
		C->SetLifeSpan(Life);
	}
}

void ABossCharacter::SpawnShards(int32 N, const FString& MatPath, float Life)
{
	if (!GetWorld()) return;
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (!Cube) return;
	UMaterialInterface* Mat = MatPath.IsEmpty() ? nullptr : LoadObject<UMaterialInterface>(nullptr, *MatPath);
	for (int32 i = 0; i < N; ++i)
	{
		const FVector Dir = FVector(FMath::FRandRange(-1.f, 1.f), FMath::FRandRange(-1.f, 1.f), FMath::FRandRange(0.2f, 1.f)).GetSafeNormal();
		const FVector Loc = GetActorLocation() + FVector(0.f, 0.f, 120.f) + Dir * FMath::FRandRange(40.f, 260.f);
		FActorSpawnParameters Sp;
		Sp.Owner = this;
		Sp.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* A = GetWorld()->SpawnActor<AStaticMeshActor>(Loc, FRotator(FMath::FRandRange(0.f, 360.f), FMath::FRandRange(0.f, 360.f), FMath::FRandRange(0.f, 360.f)), Sp);
		if (!A) continue;
		A->SetActorEnableCollision(false);
		if (UStaticMeshComponent* MC = A->GetStaticMeshComponent())
		{
			MC->SetMobility(EComponentMobility::Movable);
			MC->SetStaticMesh(Cube);
			MC->SetWorldScale3D(FVector(0.12f, 0.22f, 0.02f));
			if (Mat) MC->SetMaterial(0, Mat);
			MC->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		}
		A->SetLifeSpan(Life);
	}
}
