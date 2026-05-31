#include "Enemy/LidiaBoss.h"
#include "Combat/StatComponent.h"
#include "Combat/HitboxComponent.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"

ALidiaBoss::ALidiaBoss()
{
	BossName = FText::FromString(TEXT("Lídia"));
	BossSubtitle = FText::FromString(TEXT("Rainha do Coração Partido"));

	if (Stats)
	{
		Stats->MaxHP = 9000.f; Stats->HP = 9000.f;
		Stats->MaxPosture = 320.f;
	}

	// 4 phases (Julgamento -> Cheshire -> Coração Partido aérea -> Ruptura/Resgate).
	PhaseHPThresholds = { 0.75f, 0.50f, 0.25f };
	bLifesteal = true;
	LifestealFraction = 0.30f;
	RewardDress = EDressType::None; // narrative boss — no dress drop
	ErgoReward = 13205; // matches HUD currency in lidia-boss.png
	AggroRadius = 3000.f;
	AttackRange = 280.f;
	AttackCooldown = 0.7f; // aggressive, Malenia-grade

	// Moves now seed Corrupção do Coração build-up (last param), ramping on the signatures.
	AddMove("EstocadaOdachi",   0.f, 300.f, 0.45f, 0.20f, 0.50f, 90.f, 290.f, EBossAttackShape::ForwardArc, 0, false, 4.f);
	AddMove("CorteHorizontal",  0.f, 320.f, 0.60f, 0.30f, 0.60f, 105.f, 320.f, EBossAttackShape::ForwardArc, 0, false, 4.f);
	AddMove("RajadaDeCartas",   0.f, 700.f, 0.70f, 0.0f, 0.80f, 80.f, 650.f, EBossAttackShape::RadialAoE, 0, false, 6.f);
	AddMove("Investida",        350.f, 1200.f, 0.45f, 0.25f, 0.70f, 100.f, 300.f, EBossAttackShape::Lunge, 0, false, 5.f);
	AddMove("DancaLaminasPartidas", 0.f, 800.f, 1.1f, 0.0f, 1.3f, 140.f, 780.f, EBossAttackShape::RadialAoE, 1, true, 14.f); // signature (Waterfowl analog)
	AddMove("CorrupcaoDoCoracao", 0.f, 700.f, 1.0f, 0.0f, 1.1f, 120.f, 680.f, EBossAttackShape::RadialAoE, 2, true, 22.f);
}

void ALidiaBoss::EnterPhase(int32 NewPhase)
{
	Super::EnterPhase(NewPhase);

	if (NewPhase >= 2)
	{
		// Coração Partido — she lifts off the ground (aerial, roteiro §7 fase 3).
		VisualBaseLoc.Z += 60.f;
	}
	// Phase 4 = emotional rescue setup: she stops fighting to the death (roteiro §7).
	if (NewPhase >= 3)
	{
		bLifesteal = false;
		AttackCooldown = 3.0f; // animations grow tired / openings widen
	}
}

void ALidiaBoss::OnMoveExecuted(const FBossAttack& M)
{
	Super::OnMoveExecuted(M);
	if (M.Name == FName("DancaLaminasPartidas"))
	{
		SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 120.f), FLinearColor(0.7f, 0.15f, 0.9f), 55000.f, 1800.f, 1.0f);
		SpawnClones(3, 1.4f); // petal/card after-images of the blade dance
		// Teleguided multi-wave: 2 more delayed bursts (only Rose-Drift-perfect chains survive).
		DanceWavesLeft = 2;
		DanceDamage = M.Damage * 0.7f;
		DanceReach = M.Reach;
		DanceCorr = M.CorruptionBuildup;
		GetWorldTimerManager().SetTimer(DanceTimer, this, &ALidiaBoss::DanceWave, 0.45f, true, 0.45f);
	}
	else if (M.Name == FName("CorrupcaoDoCoracao"))
	{
		SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 90.f), FLinearColor(0.5f, 0.1f, 0.7f), 40000.f, 1500.f, 0.9f);
	}
}

void ALidiaBoss::DanceWave()
{
	if (DanceWavesLeft <= 0 || bRescued)
	{
		GetWorldTimerManager().ClearTimer(DanceTimer);
		return;
	}
	FBossAttack W;
	W.Name = "DancaWave";
	W.Damage = DanceDamage;
	W.Posture = DanceDamage * 0.3f;
	W.Reach = DanceReach;
	W.Shape = EBossAttackShape::RadialAoE;
	W.bUnblockable = true;
	W.CorruptionBuildup = DanceCorr;
	DoRadialHit(W);
	SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 140.f), FLinearColor(0.8f, 0.2f, 1.0f), 45000.f, DanceReach * 2.f, 0.5f);
	SpawnShards(16, ShardMaterialPath, 0.9f);

	if (--DanceWavesLeft <= 0)
	{
		GetWorldTimerManager().ClearTimer(DanceTimer);
	}
}

void ALidiaBoss::Die()
{
	// "Não executar" (roteiro B.5): Alice does NOT kill Lídia. When her body would fall,
	// the Cheshire control breaks, she kneels, and the player is taken to the reunion.
	if (bRescued || bDead) return;
	bRescued = true;

	bLifesteal = false;
	bBusy = true;     // blocks PerformAttack
	bAggro = false;   // hides the boss bar
	GetWorldTimerManager().ClearTimer(MoveWindupTimer);
	GetWorldTimerManager().ClearTimer(MoveActiveTimer);
	GetWorldTimerManager().ClearTimer(MoveRecoverTimer);
	GetWorldTimerManager().ClearTimer(DanceTimer);
	if (Hitbox) Hitbox->EndWindow();
	if (Stats) Stats->HP = 1.f; // she survives; the stat already flagged death so no further hit lands

	SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 90.f), FLinearColor(0.85f, 0.78f, 1.0f), 30000.f, 1600.f, 3.0f);
	OnDefeated.Broadcast();

	const FName Lvl = NextLevelName.IsNone() ? EndingLevelName : NextLevelName;
	if (!Lvl.IsNone())
	{
		GetWorldTimerManager().SetTimer(LevelTransitionTimer,
			FTimerDelegate::CreateLambda([this, Lvl]() { UGameplayStatics::OpenLevel(this, Lvl); }),
			6.0f, false);
	}
}
