#include "Combat/HitboxComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/World.h"
#include "DrawDebugHelpers.h"

UHitboxComponent::UHitboxComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.bStartWithTickEnabled = false;
}

void UHitboxComponent::BeginWindow()
{
	AlreadyHit.Reset();
	if (!Mesh)
	{
		if (AActor* Owner = GetOwner())
		{
			Mesh = Owner->FindComponentByClass<USkeletalMeshComponent>();
		}
	}
	SetComponentTickEnabled(true);
}

void UHitboxComponent::EndWindow()
{
	SetComponentTickEnabled(false);
}

void UHitboxComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	AActor* Owner = GetOwner();
	if (!Owner)
	{
		return;
	}

	FVector A, B;
	if (!bForceForwardArc && Mesh && Mesh->GetSkeletalMeshAsset())
	{
		A = Mesh->GetSocketLocation(StartSocket);
		B = Mesh->GetSocketLocation(EndSocket);
	}
	else
	{
		// Static-mesh character fallback: sweep an arc in front of the owner.
		const FVector Loc = Owner->GetActorLocation();
		const FVector Fwd = Owner->GetActorForwardVector();
		A = Loc + FVector(0.f, 0.f, ArcZOffset);
		B = A + Fwd * ForwardReach;
	}

	const FCollisionShape Sphere = FCollisionShape::MakeSphere(Radius);
	FCollisionQueryParams Params(SCENE_QUERY_STAT(HitboxSweep), false, GetOwner());

	TArray<FHitResult> Hits;
	GetWorld()->SweepMultiByChannel(Hits, A, B, FQuat::Identity, ECC_Pawn, Sphere, Params);

	for (const FHitResult& H : Hits)
	{
		AActor* Tgt = H.GetActor();
		if (!Tgt || AlreadyHit.Contains(Tgt))
		{
			continue;
		}
		if (Tgt->Implements<UDamageable>())
		{
			AlreadyHit.Add(Tgt);

			FHitData Hit = HitTemplate;
			Hit.ImpactPoint = H.ImpactPoint;
			Hit.Instigator = GetOwner();
			Hit.ImpactDir = (Tgt->GetActorLocation() - GetOwner()->GetActorLocation()).GetSafeNormal();

			IDamageable::Execute_ReceiveHit(Tgt, Hit);
			OnHitDealt.Broadcast(Tgt, Hit);
		}
	}

	if (bDrawDebug)
	{
		DrawDebugCapsule(GetWorld(), (A + B) * 0.5f, (B - A).Size() * 0.5f + Radius, Radius,
			FRotationMatrix::MakeFromZ(B - A).ToQuat(), FColor::Red, false, 0.5f);
	}
}
