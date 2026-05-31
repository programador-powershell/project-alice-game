#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Combat/HitTypes.h"
#include "CombatCharacter.generated.h"

class UStatComponent;
class UHitboxComponent;
class UAnimMontage;
class UCameraShakeBase;
class UStaticMeshComponent;
class UStaticMesh;

/**
 * Shared base for every combatant (player, enemies, bosses).
 * Owns stats + a melee hitbox, runs a section-based attack combo, a dodge with
 * animation-driven i-frames, guard/perfect-guard resolution, posture-break groggy,
 * hit-stop and camera-shake juice. Custom — no GAS (matches Lies of P / Wukong).
 */
UCLASS()
class ALICE_API ACombatCharacter : public ACharacter, public IDamageable
{
	GENERATED_BODY()

public:
	ACombatCharacter();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat") TObjectPtr<UStatComponent> Stats;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat") TObjectPtr<UHitboxComponent> Hitbox;

	/** Visible body. Since the provided character GLBs are static meshes, every combatant
	 *  shows a static VisualMesh (no skeleton/anim). Set VisualMeshAsset per character. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Visual") TObjectPtr<UStaticMeshComponent> VisualMesh;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Visual") TObjectPtr<UStaticMesh> VisualMeshAsset;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Visual") float VisualMeshScale = 1.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Anim") TObjectPtr<UAnimMontage> AttackCombo;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Anim") TObjectPtr<UAnimMontage> DodgeMontage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Anim") TObjectPtr<UAnimMontage> HitReactMontage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Anim") TObjectPtr<UAnimMontage> DeathMontage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Anim") int32 NumComboSections = 3;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Juice") TSubclassOf<UCameraShakeBase> HitShake;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Juice") float HitStopSeconds = 0.08f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Cost") float AttackStaminaCost = 15.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Cost") float DodgeStaminaCost = 25.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Cost") float AttackNoAnimDuration = 0.35f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Dodge") float DodgeImpulse = 950.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Dodge") float DodgeIFrameTime = 0.45f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Guard") float PerfectGuardWindow = 0.2f;

	UPROPERTY(BlueprintReadWrite, Category = "Combat|State") bool bInvulnerable = false;
	UPROPERTY(BlueprintReadWrite, Category = "Combat|State") bool bBlocking = false;
	UPROPERTY(BlueprintReadWrite, Category = "Combat|State") bool bHyperArmor = false;
	UPROPERTY(BlueprintReadOnly, Category = "Combat|State") bool bDead = false;
	UPROPERTY(BlueprintReadOnly, Category = "Combat|State") bool bGroggy = false;

	UFUNCTION(BlueprintCallable, Category = "Combat") virtual void Attack();
	UFUNCTION(BlueprintCallable, Category = "Combat") virtual void Dodge(const FVector& WorldDir);
	UFUNCTION(BlueprintCallable, Category = "Combat") void StartBlock() { bBlocking = true; GuardPressTime = NowSeconds(); }
	UFUNCTION(BlueprintCallable, Category = "Combat") void StopBlock() { bBlocking = false; }

	/** Reset a dead/disabled character back to a live, controllable state (respawn). */
	UFUNCTION(BlueprintCallable, Category = "Combat") virtual void Revive();

	/** Called from anim notifies on the attack montage. */
	UFUNCTION(BlueprintCallable, Category = "Combat") void OpenComboWindow() { bComboWindowOpen = true; }
	UFUNCTION(BlueprintCallable, Category = "Combat") void CloseComboWindow();

	// IDamageable
	virtual void ReceiveHit_Implementation(const FHitData& Hit) override;

	UFUNCTION(BlueprintPure, Category = "Combat") UStatComponent* GetStats() const { return Stats; }
	UFUNCTION(BlueprintPure, Category = "Combat") bool IsDeadChar() const { return bDead; }

	virtual void BeginPlay() override;
	virtual void OnConstruction(const FTransform& Transform) override;
	virtual void Tick(float DeltaSeconds) override;

protected:
	UFUNCTION() virtual void HandleDeath();
	UFUNCTION() virtual void HandlePostureBreak();

	void OnAttackMontageEnded(UAnimMontage* Montage, bool bInterrupted);
	void PlayComboSection(int32 Index);

	void DoHitStop(float Seconds);
	void EndHitStop();
	void EndNoAnimAttack();
	void EndDodgeIFrames();
	void ResolveGuard(const FHitData& Hit);
	virtual void PlayHitReact(const FVector& FromDir, EHitStrength Strength);
	virtual void EnterGroggy();
	void ClearGroggy() { bGroggy = false; }
	virtual void Die();

	float NowSeconds() const;

	float GuardPressTime = 0.f;
	int32 ComboIndex = 0;
	bool bComboWindowOpen = false;
	bool bAttackQueued = false;
	bool bAttacking = false;

	FTimerHandle HitStopTimer;
	FTimerHandle GroggyTimer;
	FTimerHandle NoAnimAttackTimer;
	FTimerHandle DodgeIFrameTimer;

	// Procedural rigid animation — gives the static-mesh proxy life until skeletal anim lands.
	float AnimTime = 0.f;
	float AttackBlend = 0.f;
	float DodgeRollTime = 0.f;
	float DodgeRollDur = 0.45f;
	float HitRecoil = 0.f;
	float DeathLean = 0.f;
	FVector VisualBaseLoc = FVector(0.f, 0.f, -90.f);
};
