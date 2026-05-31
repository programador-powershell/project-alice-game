#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PortalActor.generated.h"

class UBoxComponent;
class UStaticMeshComponent;
class UParticleSystemComponent;

/**
 * Vortex portal: walk into the trigger -> short fade -> OpenLevel(TargetLevel).
 * One per area, wired to the next area per the roteiro chain.
 */
UCLASS()
class ALICE_API APortalActor : public AActor
{
	GENERATED_BODY()

public:
	APortalActor();

	/** Level to open when the player enters (e.g. "L_Vortice"). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Portal") FName TargetLevel;

	/** Delay before travel (lets the fade play). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Portal") float Delay = 1.0f;

	/** Optional spawn-tag at destination (where player appears). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Portal") FName TargetTag;

protected:
	virtual void BeginPlay() override;

	UFUNCTION()
	void OnOverlap(UPrimitiveComponent* OverlappedComp, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex,
		bool bFromSweep, const FHitResult& Sweep);

	UPROPERTY(VisibleAnywhere, Category = "Portal") TObjectPtr<USceneComponent> Root;
	UPROPERTY(VisibleAnywhere, Category = "Portal") TObjectPtr<UBoxComponent> Trigger;
	UPROPERTY(VisibleAnywhere, Category = "Portal") TObjectPtr<UStaticMeshComponent> VortexMesh;

private:
	bool bTriggered = false;
};
