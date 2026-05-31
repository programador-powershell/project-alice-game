#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Combat/HitTypes.h"
#include "WeaponComponent.generated.h"

class UStaticMesh;
class UStaticMeshComponent;

/** One weapon: a mesh + hit profile, with a second "transformed" form (roteiro §6.3). */
USTRUCT(BlueprintType)
struct FWeaponDef
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Id = "Faca";
	UPROPERTY(EditAnywhere, BlueprintReadWrite) TObjectPtr<UStaticMesh> Mesh = nullptr;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) TObjectPtr<UStaticMesh> TransformedMesh = nullptr;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FHitData BaseHit;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FHitData TransformedHit;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName AttachSocket = "weapon_r";
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeaponChanged, FName, WeaponId);

/**
 * Holds Alice's weapon loadout (kitchen knife + 5 boss-soul weapons), spawns the
 * equipped mesh on the character's hand socket, and pushes the active FHitData into
 * the shared UHitboxComponent. Toggling form swaps mesh + hit profile.
 */
UCLASS(ClassGroup = (Alice), meta = (BlueprintSpawnableComponent))
class ALICE_API UWeaponComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UWeaponComponent();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon") TArray<FWeaponDef> Loadout;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Weapon") int32 CurrentIndex = 0;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Weapon") bool bTransformed = false;

	UPROPERTY(BlueprintAssignable) FOnWeaponChanged OnWeaponChanged;

	UFUNCTION(BlueprintCallable, Category = "Weapon") void Equip(int32 Index);
	UFUNCTION(BlueprintCallable, Category = "Weapon") void NextWeapon();
	UFUNCTION(BlueprintCallable, Category = "Weapon") void ToggleForm();

	virtual void BeginPlay() override;

private:
	void ApplyCurrent();

	UPROPERTY() TObjectPtr<UStaticMeshComponent> WeaponMeshComp = nullptr;
};
