#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Combat/HitTypes.h"
#include "HitboxComponent.generated.h"

class USkeletalMeshComponent;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHitDealt, AActor*, Target, const FHitData&, Hit);

/**
 * Sweeps a sphere between two weapon sockets during an active animation window.
 * Each target is hit at most once per swing. Driven by UAnimNotifyState_Hitbox.
 */
UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class ALICE_API UHitboxComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHitboxComponent();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") FName StartSocket = "weapon_base";
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") FName EndSocket = "weapon_tip";
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") float Radius = 12.f;
	/** Static-mesh fallback (no skeleton): sweep an arc this far in front of the owner. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") float ForwardReach = 190.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") float ArcZOffset = 60.f;
	/** Force the forward-arc sweep even when a skeletal mesh exists (mesh has no weapon sockets). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") bool bForceForwardArc = false;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") FHitData HitTemplate;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hitbox") bool bDrawDebug = false;

	/** The mesh whose sockets we sweep between (set by the notify, or auto-found). */
	UPROPERTY(BlueprintReadWrite, Category = "Hitbox") TObjectPtr<USkeletalMeshComponent> Mesh = nullptr;

	UFUNCTION(BlueprintCallable, Category = "Hitbox") void BeginWindow();
	UFUNCTION(BlueprintCallable, Category = "Hitbox") void EndWindow();

	/** Broadcast each time this hitbox deals a hit (drives boss lifesteal, etc.). */
	UPROPERTY(BlueprintAssignable, Category = "Hitbox") FOnHitDealt OnHitDealt;

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	UPROPERTY() TSet<TObjectPtr<AActor>> AlreadyHit;
};
