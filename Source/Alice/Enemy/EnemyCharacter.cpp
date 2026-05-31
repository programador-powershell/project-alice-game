#include "Enemy/EnemyCharacter.h"
#include "Player/AliceCharacter.h"
#include "Combat/StatComponent.h"
#include "Combat/HitboxComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "AIController.h"
#include "Kismet/GameplayStatics.h"

AEnemyCharacter::AEnemyCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
	AIControllerClass = AAIController::StaticClass();

	if (Stats)
	{
		Stats->MaxHP = 800.f; Stats->HP = 800.f;
	}
	Tags.Add(FName("Enemy"));
	if (Hitbox)
	{
		Hitbox->HitTemplate.Damage = 40.f;
		Hitbox->HitTemplate.PostureDamage = 18.f;
		Hitbox->ForwardReach = 190.f;
	}
	GetCharacterMovement()->bOrientRotationToMovement = false;
}

void AEnemyCharacter::BeginPlay()
{
	Super::BeginPlay();
	TargetPawn = UGameplayStatics::GetPlayerPawn(this, 0);
}

void AEnemyCharacter::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);

	if (bDead) return;

	if (!TargetPawn)
	{
		TargetPawn = UGameplayStatics::GetPlayerPawn(this, 0);
		if (!TargetPawn) return;
	}

	const float Dist = FVector::Dist(GetActorLocation(), TargetPawn->GetActorLocation());
	if (!bAggro && Dist > AggroRadius)
	{
		return;
	}
	bAggro = true;

	if (!CanAct())
	{
		return; // committed to a move (boss) — don't steer or re-attack
	}

	FVector ToTarget = TargetPawn->GetActorLocation() - GetActorLocation();
	ToTarget.Z = 0.f;
	if (!ToTarget.IsNearlyZero())
	{
		const FRotator Want(0.f, ToTarget.Rotation().Yaw, 0.f);
		SetActorRotation(FMath::RInterpTo(GetActorRotation(), Want, DeltaSeconds, TurnSpeed));
	}

	if (Dist <= AttackRange)
	{
		if (!bGroggy && NowSeconds() - LastAttackTime >= AttackCooldown)
		{
			LastAttackTime = NowSeconds();
			PerformAttack();
		}
	}
	else if (!bGroggy)
	{
		AddMovementInput(ToTarget.GetSafeNormal(), 1.f);
	}
}

void AEnemyCharacter::PerformAttack()
{
	Attack();
}

void AEnemyCharacter::Die()
{
	if (bDead) return;

	if (APawn* P = UGameplayStatics::GetPlayerPawn(this, 0))
	{
		if (AAliceCharacter* Alice = Cast<AAliceCharacter>(P))
		{
			Alice->AddErgo(ErgoReward);
		}
	}

	Super::Die();
	SetActorTickEnabled(false);
}
