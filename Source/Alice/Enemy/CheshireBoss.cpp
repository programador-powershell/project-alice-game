#include "Enemy/CheshireBoss.h"
#include "Combat/StatComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Pawn.h"
#include "TimerManager.h"

ACheshireBoss::ACheshireBoss()
{
	BossName = FText::FromString(TEXT("Gato Cheshire"));
	BossSubtitle = FText::FromString(TEXT("O Sorriso na Escuridão"));

	if (Stats)
	{
		Stats->MaxHP = 2600.f; Stats->HP = 2600.f;
		Stats->MaxPosture = 170.f;
	}
	PhaseHPThresholds = { 0.66f, 0.33f };
	RewardDress = EDressType::Cheshire;
	ErgoReward = 2600;
	AggroRadius = 2400.f;
	AttackRange = 230.f;
	AttackCooldown = 0.85f;

	AddMove("Garra",        0.f, 250.f, 0.35f, 0.18f, 0.50f, 75.f, 235.f, EBossAttackShape::ForwardArc, 0);
	AddMove("CorteDuplo",   0.f, 260.f, 0.50f, 0.28f, 0.65f, 95.f, 245.f, EBossAttackShape::ForwardArc, 0);
	AddMove("PassoSombrio", 350.f, 1100.f, 0.45f, 0.22f, 0.70f, 95.f, 250.f, EBossAttackShape::Lunge, 0);
	AddMove("RisoCortante", 0.f, 500.f, 0.85f, 0.0f, 1.0f, 90.f, 480.f, EBossAttackShape::RadialAoE, 1, true);
}

void ACheshireBoss::OnMoveExecuted(const FBossAttack& M)
{
	Super::OnMoveExecuted(M);
	if (M.Name == FName("PassoSombrio"))
	{
		// Signature: blink behind the player through invisibility, then strike.
		TeleportBehindPlayer();
		Vanish();
		SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 90.f), FLinearColor(0.55f, 0.20f, 0.85f), 35000.f, 1100.f, 0.5f);
	}
}

void ACheshireBoss::EnterPhase(int32 NewPhase)
{
	Super::EnterPhase(NewPhase);
	// Each phase shift, the cat dissolves into its grin and reappears elsewhere.
	TeleportBehindPlayer();
	Vanish();
}

void ACheshireBoss::TeleportBehindPlayer()
{
	APawn* P = UGameplayStatics::GetPlayerPawn(this, 0);
	if (!P) return;
	FVector Behind = P->GetActorLocation() - P->GetActorForwardVector() * 190.f;
	Behind.Z = GetActorLocation().Z;
	SetActorLocation(Behind, false, nullptr, ETeleportType::TeleportPhysics);
	FVector D = P->GetActorLocation() - Behind; D.Z = 0.f;
	if (!D.IsNearlyZero()) SetActorRotation(D.Rotation());
}

void ACheshireBoss::Vanish()
{
	if (VisualMesh) VisualMesh->SetVisibility(false);
	bInvulnerable = true; // untargetable while a ghost
	GetWorldTimerManager().SetTimer(CheshireRevealTimer, this, &ACheshireBoss::Reveal, 0.55f, false);
}

void ACheshireBoss::Reveal()
{
	if (VisualMesh) VisualMesh->SetVisibility(true);
	bInvulnerable = false;
	SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 90.f), FLinearColor(0.7f, 0.25f, 0.95f), 30000.f, 1000.f, 0.4f);
}
