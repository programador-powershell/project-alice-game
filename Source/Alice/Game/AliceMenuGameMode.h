#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "AliceMenuGameMode.generated.h"

/** Front-door GameMode: menu controller + Canvas menu HUD, no player pawn. */
UCLASS()
class ALICE_API AAliceMenuGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AAliceMenuGameMode();
};
