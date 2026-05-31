#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "AliceGameMode.generated.h"

class APawn;

/**
 * Soulslike loop owner: tracks the active checkpoint, respawns the player on death,
 * gates resting to checkpoints, and saves/loads progress.
 */
UCLASS()
class ALICE_API AAliceGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AAliceGameMode();

	UPROPERTY(EditAnywhere, Category = "Alice") float RespawnDelay = 3.0f;
	UPROPERTY(EditAnywhere, Category = "Alice") FString SaveSlot = TEXT("AliceSave");

	/** Set the respawn point (called by a checkpoint on overlap). */
	void RegisterCheckpoint(const FTransform& Xf);
	void SetPlayerInCheckpoint(bool bIn) { bPlayerInCheckpoint = bIn; }
	UFUNCTION(BlueprintPure, Category = "Alice") bool CanRest() const { return bPlayerInCheckpoint; }

	void OnPlayerRested();
	void OnPlayerDied(APawn* Pawn);

	UFUNCTION(BlueprintCallable, Category = "Alice") void SaveProgress();
	UFUNCTION(BlueprintCallable, Category = "Alice") void LoadProgress();

	virtual void BeginPlay() override;

protected:
	void RespawnPlayer();
	void ApplyLoadedToPlayer();

	FTransform CheckpointTransform = FTransform::Identity;
	bool bHasCheckpoint = false;
	bool bPlayerInCheckpoint = false;

	// Pending loaded values applied to the player once it exists.
	int32 PendingErgo = 0;
	int32 PendingLevel = 1;
	TArray<uint8> PendingDresses;
	bool bHasPendingLoad = false;

	FTimerHandle RespawnTimer;
	FTimerHandle ApplyLoadTimer;
	TWeakObjectPtr<APawn> DeadPawn;
};
