#include "Enemy/ChapeleiroBoss.h"
#include "Combat/StatComponent.h"

AChapeleiroBoss::AChapeleiroBoss()
{
	BossName = FText::FromString(TEXT("Chapeleiro Maluco"));
	BossSubtitle = FText::FromString(TEXT("O Mestre do Chá Eterno"));

	if (Stats)
	{
		// roteiro lists ~38k HP; scaled to the slice's player damage band.
		Stats->MaxHP = 4200.f; Stats->HP = 4200.f;
		Stats->MaxPosture = 240.f;
	}
	PhaseHPThresholds = { 0.75f, 0.50f, 0.25f };
	RewardDress = EDressType::Chapeleiro;
	ErgoReward = 3200;
	AggroRadius = 2300.f;
	AttackRange = 250.f;
	AttackCooldown = 0.9f;

	AddMove("Bengalada",    0.f, 290.f, 0.50f, 0.25f, 0.65f, 100.f, 290.f, EBossAttackShape::ForwardArc, 0);
	AddMove("GolpeAlto",    0.f, 300.f, 0.80f, 0.30f, 0.85f, 135.f, 300.f, EBossAttackShape::ForwardArc, 0);
	AddMove("Investida",    350.f, 1000.f, 0.55f, 0.25f, 0.85f, 110.f, 280.f, EBossAttackShape::Lunge, 0);
	AddMove("ChaEterno",    0.f, 560.f, 1.0f, 0.0f, 1.1f, 115.f, 540.f, EBossAttackShape::RadialAoE, 1, true);
	AddMove("ColapsoFinal", 0.f, 650.f, 1.2f, 0.0f, 1.3f, 150.f, 640.f, EBossAttackShape::RadialAoE, 2, true);
}
