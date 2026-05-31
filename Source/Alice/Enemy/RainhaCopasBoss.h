#pragma once

#include "CoreMinimal.h"
#include "Enemy/BossCharacter.h"
#include "RainhaCopasBoss.generated.h"

/** Boss 5 — Rainha de Copas. Domination theme, Pátio Real arena.
 *  Grants the Rainha (Domination) dress + Guillotine on defeat. */
UCLASS()
class ALICE_API ARainhaCopasBoss : public ABossCharacter
{
	GENERATED_BODY()
public:
	ARainhaCopasBoss();

protected:
	virtual void EnterPhase(int32 NewPhase) override;
	void SummonCardSoldiers(int32 N);   // Dominação — call the deck to her side
};
