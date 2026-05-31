#include "Player/WeaponComponent.h"
#include "Combat/HitboxComponent.h"
#include "GameFramework/Character.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"

UWeaponComponent::UWeaponComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UWeaponComponent::BeginPlay()
{
	Super::BeginPlay();
	if (Loadout.Num() > 0)
	{
		Equip(0);
	}
}

void UWeaponComponent::Equip(int32 Index)
{
	if (!Loadout.IsValidIndex(Index)) return;

	CurrentIndex = Index;
	bTransformed = false;

	ACharacter* C = Cast<ACharacter>(GetOwner());
	if (!C || !C->GetMesh()) return;

	if (!WeaponMeshComp)
	{
		WeaponMeshComp = NewObject<UStaticMeshComponent>(C);
		WeaponMeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		WeaponMeshComp->RegisterComponent();
	}
	WeaponMeshComp->AttachToComponent(
		C->GetMesh(),
		FAttachmentTransformRules::SnapToTargetIncludingScale,
		Loadout[Index].AttachSocket);

	ApplyCurrent();
}

void UWeaponComponent::NextWeapon()
{
	if (Loadout.Num() == 0) return;
	Equip((CurrentIndex + 1) % Loadout.Num());
}

void UWeaponComponent::ToggleForm()
{
	bTransformed = !bTransformed;
	ApplyCurrent();
}

void UWeaponComponent::ApplyCurrent()
{
	if (!Loadout.IsValidIndex(CurrentIndex)) return;
	const FWeaponDef& Def = Loadout[CurrentIndex];

	if (WeaponMeshComp)
	{
		UStaticMesh* M = (bTransformed && Def.TransformedMesh) ? Def.TransformedMesh : Def.Mesh;
		WeaponMeshComp->SetStaticMesh(M);
	}

	if (UHitboxComponent* H = GetOwner()->FindComponentByClass<UHitboxComponent>())
	{
		H->HitTemplate = bTransformed ? Def.TransformedHit : Def.BaseHit;
	}

	OnWeaponChanged.Broadcast(Def.Id);
}
