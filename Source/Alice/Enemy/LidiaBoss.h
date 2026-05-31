#pragma once

#include "CoreMinimal.h"
#include "Enemy/BossCharacter.h"
#include "LidiaBoss.generated.h"

/**
 * FINAL BOSS — Lídia, Rainha do Coração Partido. Malenia-grade (roteiro §7).
 * 4 phases, lifesteal (heals on every hit landed), high posture.
 * Signature "Dança das Lâminas Partidas" (Waterfowl analog) + phase-2 aerial
 * transform + "Corrupção do Coração" status are scaffolded hooks for later passes.
 */
UCLASS()
class ALICE_API ALidiaBoss : public ABossCharacter
{
	GENERATED_BODY()

public:
	ALidiaBoss();

	/** Build-up status applied by Lídia's hits (Scarlet-Rot analog). Scaffold. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Lidia") float CorruptionPerHit = 6.f;

	/** Where the rescue (Cena 17, "Estenda a mão") sends the player. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Lidia") FName EndingLevelName = "L_CampoEtereo";

protected:
	virtual void EnterPhase(int32 NewPhase) override;
	virtual void OnMoveExecuted(const FBossAttack& M) override;
	virtual void Die() override;            // "Não executar" — non-lethal rescue
	void DanceWave();                       // staggered waves of Dança das Lâminas Partidas

	bool bRescued = false;
	int32 DanceWavesLeft = 0;
	float DanceDamage = 0.f;
	float DanceReach = 0.f;
	float DanceCorr = 0.f;
	FTimerHandle DanceTimer;
};
