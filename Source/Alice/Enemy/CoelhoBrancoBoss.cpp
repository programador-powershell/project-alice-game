#include "Enemy/CoelhoBrancoBoss.h"
#include "Combat/StatComponent.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Pawn.h"
#include "TimerManager.h"

ACoelhoBrancoBoss::ACoelhoBrancoBoss()
{
	BossName = FText::FromString(TEXT("Coelho Branco"));
	BossSubtitle = FText::FromString(TEXT("O Mensageiro do Tempo"));

	if (Stats)
	{
		Stats->MaxHP = 3200.f; Stats->HP = 3200.f;
		Stats->MaxPosture = 180.f;
	}

	PhaseHPThresholds = { 0.75f, 0.50f, 0.25f };
	RewardDress = EDressType::Coelho;
	ErgoReward = 2400;
	AggroRadius = 2200.f;
	AttackRange = 240.f;
	AttackCooldown = 0.9f; // gap between move selections (moves have own recover)

	AddMove("Jab",            0.f, 260.f, 0.40f, 0.18f, 0.55f,  70.f, 230.f, EBossAttackShape::ForwardArc, 0);
	AddMove("DuploCorte",     0.f, 270.f, 0.55f, 0.30f, 0.70f,  95.f, 245.f, EBossAttackShape::ForwardArc, 0);
	AddMove("Investida",    300.f, 950.f, 0.55f, 0.25f, 0.85f, 100.f, 260.f, EBossAttackShape::Lunge,      0);
	AddMove("RupturaDoTempo", 0.f, 460.f, 0.95f, 0.00f, 1.05f,  90.f, 440.f, EBossAttackShape::RadialAoE,  1, true);
}

void ACoelhoBrancoBoss::OnMoveExecuted(const FBossAttack& M)
{
	Super::OnMoveExecuted(M);
	if (M.Name == FName("RupturaDoTempo"))
	{
		SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 90.f), FLinearColor(0.3f, 0.5f, 1.0f), 45000.f, 1500.f, 0.8f);
		SpawnClones(3, 2.0f); // time-clones
		// Signature: fracture time around the player — they slow for a beat.
		if (APawn* P = UGameplayStatics::GetPlayerPawn(this, 0))
		{
			P->CustomTimeDilation = 0.5f;
			TWeakObjectPtr<APawn> WP = P;
			GetWorldTimerManager().SetTimer(TimeSlowTimer,
				FTimerDelegate::CreateLambda([WP]() { if (APawn* Q = WP.Get()) { Q->CustomTimeDilation = 1.f; } }),
				1.6f, false);
		}
	}
}
