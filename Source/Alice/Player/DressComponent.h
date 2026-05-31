#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "DressComponent.generated.h"

/** The five power-dresses, each tied to a defeated boss's power. */
UENUM(BlueprintType)
enum class EDressType : uint8
{
	None		UMETA(DisplayName = "Vestido Base"),
	Coelho		UMETA(DisplayName = "Coelho Branco (Tempo)"),
	Cheshire	UMETA(DisplayName = "Cheshire (Invisibilidade)"),
	Chapeleiro	UMETA(DisplayName = "Chapeleiro (Caos)"),
	Lagarta		UMETA(DisplayName = "Lagarta Azul (Alucinação)"),
	Rainha		UMETA(DisplayName = "Rainha de Copas (Dominação)")
};

USTRUCT(BlueprintType)
struct FDressState
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite) EDressType Type = EDressType::None;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bUnlocked = false;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) float Corruption = 0.f; // 0..100
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FLinearColor PetalColor = FLinearColor::White;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName SkillName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float SkillSanityCost = 20.f;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDressChanged, EDressType, NewDress);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnCorruptionChanged, EDressType, Dress, float, Corruption);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSkillUsed, EDressType, Dress);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDressTransform, EDressType, Dress);

/**
 * Alice's 5 power-dresses. Using a dress skill channels boss power, costs Sanity,
 * and raises that dress's Corruption (0->100 in stages). At 100% the dress fully
 * transforms (signature burst), then resets and restores partial sanity.
 * Petal color per dress feeds the Rose Drift VFX.
 */
UCLASS(ClassGroup = (Alice), meta = (BlueprintSpawnableComponent))
class ALICE_API UDressComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UDressComponent();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Dress") TArray<FDressState> Dresses;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dress") EDressType Current = EDressType::None;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dress") float CorruptionPerSkill = 20.f;

	UPROPERTY(BlueprintAssignable) FOnDressChanged OnDressChanged;
	UPROPERTY(BlueprintAssignable) FOnCorruptionChanged OnCorruptionChanged;
	UPROPERTY(BlueprintAssignable) FOnSkillUsed OnSkillUsed;
	UPROPERTY(BlueprintAssignable) FOnDressTransform OnDressTransform;

	UFUNCTION(BlueprintCallable, Category = "Dress") void EquipDress(EDressType Type);
	UFUNCTION(BlueprintCallable, Category = "Dress") void CycleDress(float Direction);
	UFUNCTION(BlueprintCallable, Category = "Dress") void UnlockDress(EDressType Type);
	UFUNCTION(BlueprintCallable, Category = "Dress") bool UseSkill();
	UFUNCTION(BlueprintPure, Category = "Dress") FLinearColor GetCurrentPetalColor() const;
	UFUNCTION(BlueprintPure, Category = "Dress") float GetCurrentCorruption() const;

	virtual void BeginPlay() override;

private:
	int32 IndexOf(EDressType Type) const;
	void AddCorruption(int32 DressIdx, float Amount);
};
