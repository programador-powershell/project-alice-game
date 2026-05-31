#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimNotifies/AnimNotifyState.h"
#include "CombatNotifies.generated.h"

/** Opens the weapon hitbox sweep for the active frames of an attack. */
UCLASS(meta = (DisplayName = "Combat Hitbox Window"))
class ALICE_API UAnimNotifyState_Hitbox : public UAnimNotifyState
{
	GENERATED_BODY()
public:
	virtual void NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, float TotalDuration, const FAnimNotifyEventReference& EventReference) override;
	virtual void NotifyEnd(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, const FAnimNotifyEventReference& EventReference) override;
};

/** Sets i-frames on a combat character for the duration (dodge roll / Rose Drift). */
UCLASS(meta = (DisplayName = "Combat Invulnerable"))
class ALICE_API UAnimNotifyState_Invuln : public UAnimNotifyState
{
	GENERATED_BODY()
public:
	virtual void NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, float TotalDuration, const FAnimNotifyEventReference& EventReference) override;
	virtual void NotifyEnd(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, const FAnimNotifyEventReference& EventReference) override;
};

/** Window during which the next attack press chains into the following combo section. */
UCLASS(meta = (DisplayName = "Combat Combo Window"))
class ALICE_API UAnimNotifyState_ComboWindow : public UAnimNotifyState
{
	GENERATED_BODY()
public:
	virtual void NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, float TotalDuration, const FAnimNotifyEventReference& EventReference) override;
	virtual void NotifyEnd(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, const FAnimNotifyEventReference& EventReference) override;
};
