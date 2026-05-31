#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "LockOnComponent.generated.h"

class ACharacter;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLockTargetChanged, AActor*, NewTarget);

/**
 * Soulslike lock-on: sphere search forward of the camera, filter to live IDamageable
 * pawns in view with line-of-sight, pick the smallest screen-angle. While locked,
 * drives the controller rotation to frame the target. Cycle with left/right.
 */
UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class ALICE_API ULockOnComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	ULockOnComponent();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LockOn") float MaxRange = 1600.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LockOn") float MaxAngleDeg = 65.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LockOn") float RotationInterpSpeed = 10.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LockOn") float PitchOffsetDeg = -8.f;

	UPROPERTY(BlueprintReadOnly, Category = "LockOn") TObjectPtr<AActor> Target = nullptr;
	UPROPERTY(BlueprintAssignable, Category = "LockOn") FOnLockTargetChanged OnTargetChanged;

	UFUNCTION(BlueprintCallable, Category = "LockOn") void Toggle();
	UFUNCTION(BlueprintCallable, Category = "LockOn") void CycleTarget(float Direction);
	UFUNCTION(BlueprintCallable, Category = "LockOn") void ClearTarget();
	UFUNCTION(BlueprintPure, Category = "LockOn") bool HasTarget() const { return Target != nullptr; }

	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	void SetTarget(AActor* NewTarget);
	AActor* FindBestTarget(float SideBias) const;
	bool IsValidTarget(AActor* Actor) const;

	TWeakObjectPtr<ACharacter> OwnerChar;
};
