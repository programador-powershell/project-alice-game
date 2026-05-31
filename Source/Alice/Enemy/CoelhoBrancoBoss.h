#pragma once

#include "CoreMinimal.h"
#include "Enemy/BossCharacter.h"
#include "CoelhoBrancoBoss.generated.h"

/**
 * Boss 1 — White Rabbit (Coelho Branco). Clockwork arena, time theme.
 * 3 phase triggers by HP. Grants the Coelho (Time) dress on defeat.
 * Time-clone summon left as a hook for later (montage/Niagara).
 */
UCLASS()
class ALICE_API ACoelhoBrancoBoss : public ABossCharacter
{
	GENERATED_BODY()

public:
	ACoelhoBrancoBoss();

protected:
	virtual void OnMoveExecuted(const FBossAttack& M) override;

	FTimerHandle TimeSlowTimer;
};
