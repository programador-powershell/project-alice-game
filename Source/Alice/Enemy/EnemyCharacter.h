#pragma once

#include "CoreMinimal.h"
#include "Combat/CombatCharacter.h"
#include "EnemyCharacter.generated.h"

/**
 * AI-driven combatant. Lightweight C++ state machine (no Behavior Tree asset needed
 * for the slice): aggro -> steer toward the player -> attack on cooldown in range.
 * Grants Ergo on death.
 */
UCLASS()
class ALICE_API AEnemyCharacter : public ACombatCharacter
{
	GENERATED_BODY()

public:
	AEnemyCharacter();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI") float AggroRadius = 1500.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI") float AttackRange = 220.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI") float AttackCooldown = 2.2f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI") float TurnSpeed = 7.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AI") int32 ErgoReward = 200;

	virtual void Tick(float DeltaSeconds) override;
	virtual void BeginPlay() override;

	UFUNCTION(BlueprintPure, Category = "AI") bool IsAggro() const { return bAggro; }

protected:
	virtual void Die() override;
	virtual void PerformAttack();              // overridable: bosses pick from a moveset
	virtual bool CanAct() const { return true; } // bosses return false mid-move

	UPROPERTY() TObjectPtr<APawn> TargetPawn = nullptr;
	float LastAttackTime = -100.f;
	bool bAggro = false;
};
