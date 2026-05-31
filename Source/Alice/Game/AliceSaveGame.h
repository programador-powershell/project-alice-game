#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "AliceSaveGame.generated.h"

/** Persistent progress: currency, level, last checkpoint, unlocked dresses. */
UCLASS()
class ALICE_API UAliceSaveGame : public USaveGame
{
	GENERATED_BODY()

public:
	UPROPERTY() int32 Ergo = 0;
	UPROPERTY() int32 SoulLevel = 1;
	UPROPERTY() bool bHasCheckpoint = false;
	UPROPERTY() FTransform CheckpointTransform = FTransform::Identity;
	UPROPERTY() TArray<uint8> UnlockedDresses;
	UPROPERTY() FString SaveSlot = TEXT("AliceSave");
};
