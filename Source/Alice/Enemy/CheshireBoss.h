#pragma once

#include "CoreMinimal.h"
#include "Enemy/BossCharacter.h"
#include "CheshireBoss.generated.h"

/** Boss 2 — Gato Cheshire. Illusion/invisibility theme (teleport/clones = later hook).
 *  Grants the Cheshire (Invisibility) dress on defeat. */
UCLASS()
class ALICE_API ACheshireBoss : public ABossCharacter
{
	GENERATED_BODY()
public:
	ACheshireBoss();

protected:
	virtual void OnMoveExecuted(const FBossAttack& M) override;
	virtual void EnterPhase(int32 NewPhase) override;

	void TeleportBehindPlayer();
	void Vanish();   // invisible + untargetable briefly
	void Reveal();

	FTimerHandle CheshireRevealTimer;
};
