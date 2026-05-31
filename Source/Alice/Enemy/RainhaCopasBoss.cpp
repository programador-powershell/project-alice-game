#include "Enemy/RainhaCopasBoss.h"
#include "Enemy/EnemyCharacter.h"
#include "Combat/StatComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"

ARainhaCopasBoss::ARainhaCopasBoss()
{
	BossName = FText::FromString(TEXT("Rainha de Copas"));
	BossSubtitle = FText::FromString(TEXT("A Soberana Escarlate"));

	if (Stats)
	{
		Stats->MaxHP = 4600.f; Stats->HP = 4600.f;
		Stats->MaxPosture = 260.f;
	}
	PhaseHPThresholds = { 0.75f, 0.50f, 0.25f };
	RewardDress = EDressType::Rainha;
	ErgoReward = 3600;
	AggroRadius = 2500.f;
	AttackRange = 260.f;
	AttackCooldown = 0.9f;

	AddMove("CetroReal",      0.f, 290.f, 0.50f, 0.25f, 0.65f, 100.f, 285.f, EBossAttackShape::ForwardArc, 0);
	AddMove("CorteDuplo",     0.f, 300.f, 0.70f, 0.30f, 0.80f, 120.f, 295.f, EBossAttackShape::ForwardArc, 0);
	AddMove("Investida",      350.f, 1000.f, 0.55f, 0.25f, 0.85f, 110.f, 275.f, EBossAttackShape::Lunge, 0);
	AddMove("ChuvaDeCartas",  0.f, 600.f, 0.90f, 0.0f, 1.0f, 105.f, 600.f, EBossAttackShape::RadialAoE, 1);
	AddMove("CortemAsCabecas", 0.f, 680.f, 1.2f, 0.0f, 1.3f, 150.f, 660.f, EBossAttackShape::RadialAoE, 2, true);
}

void ARainhaCopasBoss::EnterPhase(int32 NewPhase)
{
	Super::EnterPhase(NewPhase);
	if (NewPhase == 2)
	{
		SummonCardSoldiers(2); // "Súditos, a mim!" — domination summons adds
	}
}

void ARainhaCopasBoss::SummonCardSoldiers(int32 N)
{
	if (!GetWorld()) return;
	UStaticMesh* SoldierMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Alice/Characters/SM_mob_soldado/StaticMeshes/SM_mob_soldado"));
	for (int32 i = 0; i < N; ++i)
	{
		const float Ang = (360.f / FMath::Max(1, N)) * i + 45.f;
		const FVector Loc = GetActorLocation() + FRotator(0.f, Ang, 0.f).Vector() * 340.f;
		FActorSpawnParameters Sp;
		Sp.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;
		AEnemyCharacter* Add = GetWorld()->SpawnActor<AEnemyCharacter>(Loc, GetActorRotation(), Sp);
		if (!Add) continue;
		Add->ErgoReward = 120;
		if (SoldierMesh && Add->VisualMesh)
		{
			Add->VisualMeshAsset = SoldierMesh;
			Add->VisualMesh->SetStaticMesh(SoldierMesh);
		}
		if (Add->Stats) { Add->Stats->MaxHP = 350.f; Add->Stats->HP = 350.f; }
		SpawnBurst(Loc + FVector(0.f, 0.f, 80.f), FLinearColor(0.9f, 0.1f, 0.15f), 25000.f, 900.f, 0.5f);
	}
}
