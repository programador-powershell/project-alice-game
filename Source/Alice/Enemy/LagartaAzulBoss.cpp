#include "Enemy/LagartaAzulBoss.h"
#include "Combat/StatComponent.h"

ALagartaAzulBoss::ALagartaAzulBoss()
{
	BossName = FText::FromString(TEXT("Lagarta Azul"));
	BossSubtitle = FText::FromString(TEXT("A Guardiã do Sonho"));

	if (Stats)
	{
		Stats->MaxHP = 3000.f; Stats->HP = 3000.f;
		Stats->MaxPosture = 200.f;
	}
	PhaseHPThresholds = { 0.66f, 0.33f };
	RewardDress = EDressType::Lagarta;
	ErgoReward = 2800;
	AggroRadius = 2200.f;
	AttackRange = 300.f; // large column-bodied
	AttackCooldown = 1.0f;

	AddMove("VarreduraCauda",  0.f, 360.f, 0.60f, 0.30f, 0.70f, 95.f, 360.f, EBossAttackShape::ForwardArc, 0);
	AddMove("BotePeconha",     300.f, 1100.f, 0.55f, 0.25f, 0.85f, 100.f, 300.f, EBossAttackShape::Lunge, 0);
	AddMove("NuvemDoSonho",    0.f, 520.f, 0.95f, 0.0f, 1.0f, 90.f, 500.f, EBossAttackShape::RadialAoE, 0, true);
	AddMove("AlucinacaoTotal", 0.f, 640.f, 1.15f, 0.0f, 1.2f, 110.f, 620.f, EBossAttackShape::RadialAoE, 1, true);
}

void ALagartaAzulBoss::OnMoveExecuted(const FBossAttack& M)
{
	Super::OnMoveExecuted(M);
	if (M.Name == FName("AlucinacaoTotal"))
	{
		SpawnClones(4, 2.5f); // hallucinated copies — which one is real?
		SpawnBurst(GetActorLocation() + FVector(0.f, 0.f, 90.f), FLinearColor(0.2f, 0.55f, 1.0f), 42000.f, 1500.f, 0.9f);
	}
	else if (M.Name == FName("NuvemDoSonho"))
	{
		SpawnShards(20, ShardMaterialPath, 1.2f); // dream-smoke cloud
	}
}
