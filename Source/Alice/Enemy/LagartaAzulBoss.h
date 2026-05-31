#pragma once

#include "CoreMinimal.h"
#include "Enemy/BossCharacter.h"
#include "LagartaAzulBoss.generated.h"

/** Boss 4 — Lagarta Azul. Hallucination theme (mandatory boss, Névoa de Cogumelos).
 *  Grants the Lagarta (Hallucination) dress + Foice on defeat. */
UCLASS()
class ALICE_API ALagartaAzulBoss : public ABossCharacter
{
	GENERATED_BODY()
public:
	ALagartaAzulBoss();

protected:
	virtual void OnMoveExecuted(const FBossAttack& M) override;
};
