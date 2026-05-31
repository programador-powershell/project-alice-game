#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "HitTypes.generated.h"

/** Strength bucket of an incoming hit — drives hit-react selection. */
UENUM(BlueprintType)
enum class EHitStrength : uint8
{
	Light,
	Heavy,
	Knockdown
};

/** Self-contained description of one melee hit. Built from a UHitboxComponent's template. */
USTRUCT(BlueprintType)
struct FHitData
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hit")
	float Damage = 10.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hit")
	float PostureDamage = 10.f;

	UPROPERTY(BlueprintReadWrite, Category = "Hit")
	FVector ImpactPoint = FVector::ZeroVector;

	UPROPERTY(BlueprintReadWrite, Category = "Hit")
	FVector ImpactDir = FVector::ForwardVector;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hit")
	EHitStrength Strength = EHitStrength::Light;

	/** Unblockable "fury"/red attack — pierces guard. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hit")
	bool bUnblockable = false;

	/** Status build-up dealt to the victim (Lídia's Corrupção do Coração — Scarlet-Rot analog). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Hit")
	float CorruptionBuildup = 0.f;

	UPROPERTY(BlueprintReadWrite, Category = "Hit")
	TObjectPtr<AActor> Instigator = nullptr;
};

UINTERFACE(MinimalAPI, Blueprintable)
class UDamageable : public UInterface
{
	GENERATED_BODY()
};

/** Anything that can take a hit. Implemented by player, enemies, bosses, breakables. */
class IDamageable
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Combat")
	void ReceiveHit(const FHitData& Hit);
};
