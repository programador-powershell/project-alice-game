#pragma once

#include "CoreMinimal.h"
#include "Enemy/EnemyCharacter.h"
#include "Player/DressComponent.h"
#include "BossCharacter.generated.h"

class UStatComponent;
struct FHitData;

UENUM(BlueprintType)
enum class EBossAttackShape : uint8
{
	ForwardArc,  // sweep in front
	Lunge,       // gap-close + sweep
	RadialAoE    // ring around the boss (telegraphed disc)
};

USTRUCT(BlueprintType)
struct FBossAttack
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere) FName Name = "Attack";
	UPROPERTY(EditAnywhere) float MinRange = 0.f;
	UPROPERTY(EditAnywhere) float MaxRange = 300.f;
	UPROPERTY(EditAnywhere) float Windup = 0.6f;     // telegraph
	UPROPERTY(EditAnywhere) float ActiveTime = 0.25f;
	UPROPERTY(EditAnywhere) float Recover = 0.8f;
	UPROPERTY(EditAnywhere) float Damage = 90.f;
	UPROPERTY(EditAnywhere) float Posture = 25.f;
	UPROPERTY(EditAnywhere) float Reach = 220.f;     // arc reach / aoe radius / lunge sweep
	UPROPERTY(EditAnywhere) EBossAttackShape Shape = EBossAttackShape::ForwardArc;
	UPROPERTY(EditAnywhere) int32 MinPhase = 0;
	UPROPERTY(EditAnywhere) bool bUnblockable = false;
	UPROPERTY(EditAnywhere) float CorruptionBuildup = 0.f; // status applied to the player on hit
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnBossPhase, int32, Phase);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnBossDefeated);

/**
 * Multi-phase boss. HP-fraction thresholds trigger phase changes (buff + montage hook).
 * Optional lifesteal (heal on dealing damage) — the Malenia-grade mechanic for Lídia.
 * Grants a power-dress to the player on defeat.
 */
UCLASS()
class ALICE_API ABossCharacter : public AEnemyCharacter
{
	GENERATED_BODY()

public:
	ABossCharacter();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss") FText BossName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss") FText BossSubtitle;

	/** HP fractions (descending) at which to advance a phase, e.g. {0.66, 0.33}. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss") TArray<float> PhaseHPThresholds;
	UPROPERTY(BlueprintReadOnly, Category = "Boss") int32 Phase = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss") bool bLifesteal = false;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss") float LifestealFraction = 0.25f;

	/** Dress unlocked on the player when this boss dies. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss") EDressType RewardDress = EDressType::None;

	/** If set, defeating this boss loads this level after a short beat (arena progression). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss") FName NextLevelName = NAME_None;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Boss|Moveset") TArray<FBossAttack> Moveset;

	UPROPERTY(BlueprintAssignable) FOnBossPhase OnPhaseChanged;
	UPROPERTY(BlueprintAssignable) FOnBossDefeated OnDefeated;

	virtual void BeginPlay() override;

protected:
	UFUNCTION() void OnStatsChangedHandler(UStatComponent* InStats);
	UFUNCTION() void OnHitDealtHandler(AActor* Target, const FHitData& Hit);

	virtual void EnterPhase(int32 NewPhase);
	virtual void Die() override;

	virtual void PerformAttack() override;
	virtual bool CanAct() const override { return !bBusy; }
	void AddMove(FName N, float Mn, float Mx, float Wu, float Act, float Rec, float Dmg, float Reach, EBossAttackShape Sh, int32 Ph, bool Unb = false, float Corr = 0.f);
	void StartMove(int32 Idx);
	void MoveExecute();
	void MoveEndActive();
	void MoveRecovered();
	void DoRadialHit(const FBossAttack& M);
	void SpawnTelegraph(float Radius);
	virtual void OnMoveExecuted(const FBossAttack& M);  // per-boss special FX hook
	void SpawnBurst(const FVector& Loc, const FLinearColor& Color, float Intensity, float Radius, float Life);
	void SpawnClones(int32 N, float Life);
	void SpawnShards(int32 N, const FString& MatPath, float Life);
	UPROPERTY(EditAnywhere, Category = "Boss|FX") FString ShardMaterialPath = TEXT("/Game/Alice/Materials/M_GlowMagenta");

	bool bBusy = false;
	int32 CurrentMove = -1;
	FTimerHandle MoveWindupTimer;
	FTimerHandle MoveActiveTimer;
	FTimerHandle MoveRecoverTimer;
	UPROPERTY() TObjectPtr<AActor> TelegraphActor = nullptr;

	FTimerHandle LevelTransitionTimer;
};
