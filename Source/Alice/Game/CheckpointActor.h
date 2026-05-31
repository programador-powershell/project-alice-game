#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "CheckpointActor.generated.h"

class UStaticMeshComponent;
class USphereComponent;
class UPointLightComponent;

/**
 * "Mesa de Chá" checkpoint (bonfire). On player overlap it becomes the respawn point
 * and enables resting (heal + flask refill via the player's Interact). A colored
 * beacon light marks the chapter (roteiro §8).
 */
UCLASS()
class ALICE_API ACheckpointActor : public AActor
{
	GENERATED_BODY()

public:
	ACheckpointActor();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USceneComponent> Root;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> TableMesh;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USphereComponent> Range;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UPointLightComponent> Beacon;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Checkpoint") FName CheckpointId = "cp_default";
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Checkpoint") FLinearColor BeaconColor = FLinearColor(1.f, 0.7f, 0.25f);

protected:
	virtual void BeginPlay() override;

	UFUNCTION()
	void OnRangeBeginOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void OnRangeEndOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
};
