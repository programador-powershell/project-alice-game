#pragma once

#include "CoreMinimal.h"
#include "Enemy/BossCharacter.h"
#include "ChapeleiroBoss.generated.h"

/** Boss 3 — Chapeleiro Maluco. Chaos theme, 3 phases, parry-heavy (roteiro §2).
 *  Grants the Chapeleiro (Chaos) dress on defeat. */
UCLASS()
class ALICE_API AChapeleiroBoss : public ABossCharacter
{
	GENERATED_BODY()
public:
	AChapeleiroBoss();
};
