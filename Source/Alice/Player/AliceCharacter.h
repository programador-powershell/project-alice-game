#pragma once

#include "CoreMinimal.h"
#include "Combat/CombatCharacter.h"
#include "Player/DressComponent.h"
#include "AliceCharacter.generated.h"

class USpringArmComponent;
class UCameraComponent;
class ULockOnComponent;
class UDressComponent;
class UWeaponComponent;
class USkeletalMeshComponent;
class UInputAction;
class UInputMappingContext;
class UNiagaraSystem;
class UAnimMontage;
class UAnimSequence;
class UMaterialInstanceDynamic;
struct FInputActionValue;
struct FHitResult;

/** Weapon grip style per dress (roteiro weapon spec). */
UENUM(BlueprintType)
enum class EWeaponGrip : uint8 { OneHand, TwoHand, Dual };

/** Per-weapon combat profile — drives combo length, reach, damage, cadence, grip. */
USTRUCT(BlueprintType)
struct FWeaponProfile
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere) EWeaponGrip Grip = EWeaponGrip::OneHand;
	UPROPERTY(EditAnywhere) int32 ComboHits = 3;
	UPROPERTY(EditAnywhere) float DamageMult = 1.f;
	UPROPERTY(EditAnywhere) float PostureMult = 1.f;
	UPROPERTY(EditAnywhere) float Reach = 200.f;
	UPROPERTY(EditAnywhere) float SpeedMult = 1.f;   // <1 fast, >1 heavy/slow
	UPROPERTY(EditAnywhere) bool bThrust = false;    // lunge forward (estocada)
	UPROPERTY(EditAnywhere) bool bExtends = false;   // cajado/staff stretches (Wukong)
};

/**
 * Alice Liddell — the player. Third-person soulslike pawn built on ACombatCharacter.
 * Adds camera, Enhanced Input, lock-on, the 5 power-dresses, weapon loadout, the
 * teacup heal flask, Ergo, and the signature Rose Drift dodge (petal i-frame dodge
 * with a perfect-dodge slow-mo, like Wukong's dodge).
 */
UCLASS()
class ALICE_API AAliceCharacter : public ACombatCharacter
{
	GENERATED_BODY()

public:
	AAliceCharacter();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera") TObjectPtr<USpringArmComponent> CameraBoom;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera") TObjectPtr<UCameraComponent> FollowCamera;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Alice") TObjectPtr<ULockOnComponent> LockOn;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Alice") TObjectPtr<UDressComponent> Dresses;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Alice") TObjectPtr<UWeaponComponent> Weapon;

	// Dress skeletal layer — same skeleton as body; follows via Leader Pose.
	// Component spawned in BeginPlay (NewObject) so it always exists even if BP didn't refresh.
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Alice|Dress") TObjectPtr<USkeletalMeshComponent> DressMesh;

	// Asset reference set in BP (the dress mesh to spawn on the body in BeginPlay).
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Alice|Dress") TObjectPtr<class USkeletalMesh> DressMeshAsset;

	// Enhanced Input assets (assigned on the BP).
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputMappingContext> DefaultMappingContext;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Move;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Look;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Jump;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Sprint;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Attack;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Dodge;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Guard;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_LockOn;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_CycleTarget;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Heal;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Skill;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_Interact;
	UPROPERTY(EditAnywhere, Category = "Input") TObjectPtr<UInputAction> IA_SwitchDress;

	// Heal flask (teacup)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Alice|Heal") int32 FlaskCharges = 4;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Alice|Heal") int32 MaxFlaskCharges = 4;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Alice|Heal") float FlaskHealAmount = 450.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Alice|Heal") TObjectPtr<UAnimMontage> HealMontage;

	// Progression
	UPROPERTY(BlueprintReadOnly, Category = "Alice|Progress") int32 Ergo = 0;
	UPROPERTY(BlueprintReadOnly, Category = "Alice|Progress") int32 SoulLevel = 1;

	// Rose Drift
	UPROPERTY(EditAnywhere, Category = "Alice|RoseDrift") TObjectPtr<UNiagaraSystem> RoseDriftPetals;
	UPROPERTY(EditAnywhere, Category = "Alice|RoseDrift") float PerfectDodgeWindow = 0.25f;
	UPROPERTY(EditAnywhere, Category = "Alice|RoseDrift") float PerfectDodgeTimeScale = 0.3f;
	UPROPERTY(EditAnywhere, Category = "Alice|RoseDrift") float PerfectDodgeDuration = 0.4f;
	UPROPERTY(EditAnywhere, Category = "Alice|Move") float WalkSpeed = 500.f;
	UPROPERTY(EditAnywhere, Category = "Alice|Move") float SprintSpeed = 760.f;

	// Skeletal anim clips (Eve/Mixamo), played via SingleNode from C++ state.
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Idle;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Walk;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Run;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Attack;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Dodge;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Hit;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Death;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Atk1;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Atk2;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Atk3;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Block;
	UPROPERTY(EditAnywhere, Category = "Alice|Anim") TObjectPtr<UAnimSequence> Anim_Parry;

	// Per-dress weapon stances (assigned on BP; swapped by dress)
	UPROPERTY(EditAnywhere, Category = "Alice|Stance") TObjectPtr<UAnimSequence> Anim_GS_Idle;
	UPROPERTY(EditAnywhere, Category = "Alice|Stance") TObjectPtr<UAnimSequence> Anim_GS_Run;
	UPROPERTY(EditAnywhere, Category = "Alice|Stance") TObjectPtr<UAnimSequence> Anim_GS_Atk;
	UPROPERTY(EditAnywhere, Category = "Alice|Stance") TObjectPtr<UAnimSequence> Anim_SS_Idle;
	UPROPERTY(EditAnywhere, Category = "Alice|Stance") TObjectPtr<UAnimSequence> Anim_SS_Atk;
	UPROPERTY(EditAnywhere, Category = "Alice|Stance") TObjectPtr<UAnimSequence> Anim_Dual_Atk;

	UFUNCTION(BlueprintCallable, Category = "Alice") void Heal();
	UFUNCTION(BlueprintCallable, Category = "Alice") void AddErgo(int32 Amount);
	UFUNCTION(BlueprintCallable, Category = "Alice") bool SpendErgo(int32 Amount);
	UFUNCTION(BlueprintCallable, Category = "Alice") void RestAtCheckpoint();

	/** Corrupção do Coração — status build-up inflicted by Lídia (roteiro §7). Procs at full. */
	UFUNCTION(BlueprintCallable, Category = "Alice") void AddHeartCorruption(float Amount);
	UFUNCTION(BlueprintPure, Category = "Alice") float GetHeartCorruptionPercent() const;

	/** Fired when a Rose Drift happens — BP spawns/colors the petal VFX + ghost. */
	UFUNCTION(BlueprintImplementableEvent, Category = "Alice|RoseDrift") void OnRoseDrift(const FVector& Dir, bool bPerfect);

	virtual void Dodge(const FVector& WorldDir) override;
	virtual void ReceiveHit_Implementation(const FHitData& Hit) override;

protected:
	virtual void BeginPlay() override;
	virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;
	virtual void HandleDeath() override;
	virtual void Tick(float DeltaSeconds) override;

	void OnMove(const FInputActionValue& V);
	void OnLook(const FInputActionValue& V);
	void OnSprintStart();
	void OnSprintStop();
	void OnAttackInput();
	void OnDodgeInput();
	void OnGuardStart();
	void OnGuardStop();
	void OnLockOnInput();
	void OnCycleInput(const FInputActionValue& V);
	void OnHealInput();
	void OnSkillInput();
	void OnInteractInput();
	void OnSwitchDressInput(const FInputActionValue& V);

	void MoveForward(float Value);
	void MoveRight(float Value);
	void AxisCycleDress(float Value);

	UFUNCTION() void OnDressChangedHandler(EDressType NewDress);
	void SetWeaponProfile(EDressType D);   // grip + combo style per weapon
	void PerformCombo();
	void DoComboStep(int32 Step);
	void EndComboWindow();
	void AdvanceCombo();
	void EndCombo();
	void SpawnPetals(int32 N);
	FString PetalMatPath() const;

	// Dress magic-shader drive (M_AliceDress params via MID) + VFX
	void InitDressMID();
	void ApplyDressLook(EDressType D);   // BaseTint + EmissiveColor + power per dress
	void RefreshDressMaterial(EDressType D, float CorruptFrac); // recolor + corruption darken
	void TriggerDressShift();            // dissolve-reform shimmer (skill / dress swap)
	void SpawnTrailPetal();              // single trailing petal when running
	virtual void Landed(const FHitResult& Hit) override;  // landing petal puff

	// Power-dress skills + corruption/sanity feedback (roteiro §6.1)
	void CastDressSkill(EDressType D);   // the 5 boss-power skills
	void DamageEnemiesInRadius(const FVector& Center, float Radius, float Dmg, float Posture, bool bCone, float ConeDot);
	UFUNCTION() void OnCorruptionChangedHandler(EDressType D, float Corruption);
	UFUNCTION() void OnDressTransformHandler(EDressType D);
	void EndSkillState();                // clears skill i-frames / invis
	void PoisonTick();                   // Lagarta dream-poison DoT tick
	void RestoreSlowedEnemies();         // undo Fracture-do-Tempo dilation

	float InputF = 0.f;
	float InputR = 0.f;
	FVector LastMoveWorldDir = FVector::ZeroVector;
	UPROPERTY() TObjectPtr<UAnimSequence> CurrentClip = nullptr;
	float LastDodgeTime = -100.f;
	FTimerHandle PerfectTimer;

	int32 ComboStep = 0;
	FWeaponProfile WeaponProfile;   // active weapon's combat profile (set per dress)
	bool bComboQueued = false;
	UPROPERTY() TObjectPtr<UAnimSequence> ActiveAttackClip = nullptr;
	FTimerHandle ComboActiveTimer;
	FTimerHandle ComboStepTimer;

	UPROPERTY() TObjectPtr<UAnimSequence> Base_Idle;
	UPROPERTY() TObjectPtr<UAnimSequence> Base_Run;
	UPROPERTY() TObjectPtr<UAnimSequence> Base_Atk1;
	UPROPERTY() TObjectPtr<UAnimSequence> Base_Atk2;
	UPROPERTY() TObjectPtr<UAnimSequence> Base_Atk3;

	// Dress shader / VFX runtime state
	UPROPERTY() TArray<TObjectPtr<UMaterialInstanceDynamic>> DressMIDs;
	float BaseEmissivePower = 2.0f;
	float DissolveTime = -1.f;   // counts down while a shift plays
	float DissolveDur = 0.55f;
	float DissolvePeak = 0.6f;   // max dissolve (stay partly visible)
	float TrailAccum = 0.f;

	// Skill runtime state
	FTimerHandle SkillStateTimer;
	FTimerHandle TimeFractureTimer;
	FTimerHandle PoisonTimer;
	int32 PoisonTicksLeft = 0;
	FVector PoisonLoc = FVector::ZeroVector;
	UPROPERTY() TArray<TWeakObjectPtr<AActor>> SlowedEnemies;

	// Heart Corruption status (Lídia)
	float HeartCorruption = 0.f;
	float HeartCorruptionMax = 100.f;
	float HeartDecayPerSec = 5.f;
};
