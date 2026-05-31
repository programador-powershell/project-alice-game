#include "Combat/LockOnComponent.h"
#include "Combat/StatComponent.h"
#include "Combat/HitTypes.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Engine/OverlapResult.h"
#include "Camera/PlayerCameraManager.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "CollisionQueryParams.h"

ULockOnComponent::ULockOnComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.bStartWithTickEnabled = false;
}

void ULockOnComponent::BeginPlay()
{
	Super::BeginPlay();
	OwnerChar = Cast<ACharacter>(GetOwner());
}

void ULockOnComponent::Toggle()
{
	if (Target)
	{
		ClearTarget();
	}
	else
	{
		SetTarget(FindBestTarget(0.f));
	}
}

void ULockOnComponent::CycleTarget(float Direction)
{
	if (!Target) return;
	if (AActor* Next = FindBestTarget(Direction))
	{
		if (Next != Target)
		{
			SetTarget(Next);
		}
	}
}

void ULockOnComponent::ClearTarget()
{
	SetTarget(nullptr);
}

void ULockOnComponent::SetTarget(AActor* NewTarget)
{
	Target = NewTarget;
	SetComponentTickEnabled(Target != nullptr);

	if (ACharacter* OC = OwnerChar.Get())
	{
		OC->bUseControllerRotationYaw = (Target != nullptr);
		if (UCharacterMovementComponent* Move = OC->GetCharacterMovement())
		{
			Move->bOrientRotationToMovement = (Target == nullptr);
		}
	}
	OnTargetChanged.Broadcast(Target);
}

bool ULockOnComponent::IsValidTarget(AActor* Actor) const
{
	if (!Actor || Actor == GetOwner()) return false;
	if (!Actor->Implements<UDamageable>()) return false;
	if (UStatComponent* S = Actor->FindComponentByClass<UStatComponent>())
	{
		if (S->IsDead()) return false;
	}
	return true;
}

AActor* ULockOnComponent::FindBestTarget(float SideBias) const
{
	const ACharacter* OC = OwnerChar.Get();
	if (!OC) return nullptr;

	const APlayerController* PC = Cast<APlayerController>(OC->GetController());
	const FVector ViewLoc = PC && PC->PlayerCameraManager ? PC->PlayerCameraManager->GetCameraLocation() : OC->GetActorLocation();
	const FRotator ViewRot = PC && PC->PlayerCameraManager ? PC->PlayerCameraManager->GetCameraRotation() : OC->GetActorRotation();
	const FVector ViewFwd = ViewRot.Vector();
	const FVector RightVec = FRotationMatrix(ViewRot).GetScaledAxis(EAxis::Y);

	TArray<FOverlapResult> Overlaps;
	const FCollisionShape Sphere = FCollisionShape::MakeSphere(MaxRange);
	FCollisionQueryParams Params(SCENE_QUERY_STAT(LockOnScan), false, GetOwner());

	GetWorld()->OverlapMultiByChannel(Overlaps, OC->GetActorLocation(), FQuat::Identity, ECC_Pawn, Sphere, Params);

	AActor* Best = nullptr;
	float BestScore = TNumericLimits<float>::Max();

	for (const FOverlapResult& O : Overlaps)
	{
		AActor* A = O.GetActor();
		if (!IsValidTarget(A) || A == Target) continue;

		const FVector ToTarget = (A->GetActorLocation() - ViewLoc).GetSafeNormal();
		const float AngleDeg = FMath::RadiansToDegrees(FMath::Acos(FVector::DotProduct(ViewFwd, ToTarget)));
		if (AngleDeg > MaxAngleDeg) continue;

		// Cycling: only accept targets on the requested side.
		if (!FMath::IsNearlyZero(SideBias))
		{
			const float Side = FVector::DotProduct(ToTarget, RightVec);
			if (FMath::Sign(Side) != FMath::Sign(SideBias)) continue;
		}

		// Line of sight.
		FHitResult Block;
		FCollisionQueryParams LOS(SCENE_QUERY_STAT(LockOnLOS), false, GetOwner());
		LOS.AddIgnoredActor(A);
		const bool bBlocked = GetWorld()->LineTraceSingleByChannel(Block, ViewLoc, A->GetActorLocation(), ECC_Visibility, LOS);
		if (bBlocked) continue;

		const float Score = AngleDeg; // smallest screen angle wins
		if (Score < BestScore)
		{
			BestScore = Score;
			Best = A;
		}
	}
	return Best;
}

void ULockOnComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	ACharacter* OC = OwnerChar.Get();
	if (!OC) return;

	if (!IsValidTarget(Target) || FVector::Dist(OC->GetActorLocation(), Target->GetActorLocation()) > MaxRange * 1.2f)
	{
		ClearTarget();
		return;
	}

	AController* Ctrl = OC->GetController();
	if (!Ctrl) return;

	const FVector EyeLoc = OC->GetActorLocation() + FVector(0, 0, OC->BaseEyeHeight);
	FRotator Desired = (Target->GetActorLocation() - EyeLoc).Rotation();
	Desired.Pitch = FMath::Clamp(Desired.Pitch + PitchOffsetDeg, -50.f, 20.f);

	const FRotator Smoothed = FMath::RInterpTo(Ctrl->GetControlRotation(), Desired, DeltaTime, RotationInterpSpeed);
	Ctrl->SetControlRotation(Smoothed);
}
