#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "StatComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnDeath);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnPostureBreak);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnStatsChanged, class UStatComponent*, Stats);

/**
 * Core vitals for any combatant (no GAS): HP, stamina, posture, and sanity.
 * Stamina & posture self-regen after a delay. Posture-break opens a Fatal/critical window.
 * Sanity is generic here (enemies ignore it); Alice uses it for dress/skill costs.
 */
UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class ALICE_API UStatComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UStatComponent();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|HP") float MaxHP = 1000.f;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats|HP") float HP = 1000.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Stamina") float MaxStamina = 100.f;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats|Stamina") float Stamina = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Stamina") float StaminaRegen = 25.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Stamina") float StaminaRegenDelay = 1.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Posture") float MaxPosture = 100.f;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats|Posture") float Posture = 0.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Posture") float PostureRegen = 15.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Posture") float PostureRegenDelay = 2.0f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Sanity") float MaxSanity = 100.f;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stats|Sanity") float Sanity = 100.f;

	UPROPERTY(BlueprintAssignable, Category = "Stats") FOnDeath OnDeath;
	UPROPERTY(BlueprintAssignable, Category = "Stats") FOnPostureBreak OnPostureBreak;
	UPROPERTY(BlueprintAssignable, Category = "Stats") FOnStatsChanged OnStatsChanged;

	UFUNCTION(BlueprintCallable, Category = "Stats") bool SpendStamina(float Cost);
	UFUNCTION(BlueprintCallable, Category = "Stats") void ApplyDamage(float Dmg, float PostureDmg);
	UFUNCTION(BlueprintCallable, Category = "Stats") void Heal(float Amount);
	UFUNCTION(BlueprintCallable, Category = "Stats") bool SpendSanity(float Cost);
	UFUNCTION(BlueprintCallable, Category = "Stats") void RestoreSanity(float Amount);
	UFUNCTION(BlueprintCallable, Category = "Stats") void RestoreFull();

	UFUNCTION(BlueprintPure, Category = "Stats") bool IsPostureBroken() const { return Posture >= MaxPosture; }
	UFUNCTION(BlueprintPure, Category = "Stats") bool IsDead() const { return HP <= 0.f; }
	UFUNCTION(BlueprintPure, Category = "Stats") float GetHPPercent() const { return MaxHP > 0.f ? HP / MaxHP : 0.f; }
	UFUNCTION(BlueprintPure, Category = "Stats") float GetStaminaPercent() const { return MaxStamina > 0.f ? Stamina / MaxStamina : 0.f; }
	UFUNCTION(BlueprintPure, Category = "Stats") float GetPosturePercent() const { return MaxPosture > 0.f ? Posture / MaxPosture : 0.f; }
	UFUNCTION(BlueprintPure, Category = "Stats") float GetSanityPercent() const { return MaxSanity > 0.f ? Sanity / MaxSanity : 0.f; }

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	float Now() const;
	float LastSpendTime = 0.f;
	float LastPostureHitTime = 0.f;
	bool bDeathBroadcast = false;
};
