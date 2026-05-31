#include "Combat/CombatNotifies.h"
#include "Combat/HitboxComponent.h"
#include "Combat/CombatCharacter.h"
#include "Components/SkeletalMeshComponent.h"

void UAnimNotifyState_Hitbox::NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase*, float, const FAnimNotifyEventReference&)
{
	if (!MeshComp || !MeshComp->GetOwner()) return;
	if (UHitboxComponent* H = MeshComp->GetOwner()->FindComponentByClass<UHitboxComponent>())
	{
		H->Mesh = MeshComp;
		H->BeginWindow();
	}
}

void UAnimNotifyState_Hitbox::NotifyEnd(USkeletalMeshComponent* MeshComp, UAnimSequenceBase*, const FAnimNotifyEventReference&)
{
	if (!MeshComp || !MeshComp->GetOwner()) return;
	if (UHitboxComponent* H = MeshComp->GetOwner()->FindComponentByClass<UHitboxComponent>())
	{
		H->EndWindow();
	}
}

void UAnimNotifyState_Invuln::NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase*, float, const FAnimNotifyEventReference&)
{
	if (MeshComp)
	{
		if (ACombatCharacter* C = Cast<ACombatCharacter>(MeshComp->GetOwner()))
		{
			C->bInvulnerable = true;
		}
	}
}

void UAnimNotifyState_Invuln::NotifyEnd(USkeletalMeshComponent* MeshComp, UAnimSequenceBase*, const FAnimNotifyEventReference&)
{
	if (MeshComp)
	{
		if (ACombatCharacter* C = Cast<ACombatCharacter>(MeshComp->GetOwner()))
		{
			C->bInvulnerable = false;
		}
	}
}

void UAnimNotifyState_ComboWindow::NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase*, float, const FAnimNotifyEventReference&)
{
	if (MeshComp)
	{
		if (ACombatCharacter* C = Cast<ACombatCharacter>(MeshComp->GetOwner()))
		{
			C->OpenComboWindow();
		}
	}
}

void UAnimNotifyState_ComboWindow::NotifyEnd(USkeletalMeshComponent* MeshComp, UAnimSequenceBase*, const FAnimNotifyEventReference&)
{
	if (MeshComp)
	{
		if (ACombatCharacter* C = Cast<ACombatCharacter>(MeshComp->GetOwner()))
		{
			C->CloseComboWindow();
		}
	}
}
