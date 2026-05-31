#include "Combat/StatComponent.h"
#include "Engine/World.h"

UStatComponent::UStatComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

float UStatComponent::Now() const
{
	const UWorld* W = GetWorld();
	return W ? W->GetTimeSeconds() : 0.f;
}

bool UStatComponent::SpendStamina(float Cost)
{
	if (Stamina < Cost)
	{
		return false;
	}
	Stamina -= Cost;
	LastSpendTime = Now();
	OnStatsChanged.Broadcast(this);
	return true;
}

void UStatComponent::ApplyDamage(float Dmg, float PostureDmg)
{
	if (bDeathBroadcast)
	{
		return;
	}

	HP = FMath::Max(0.f, HP - Dmg);
	Posture = FMath::Min(MaxPosture, Posture + PostureDmg);
	LastPostureHitTime = Now();

	OnStatsChanged.Broadcast(this);

	if (HP <= 0.f)
	{
		bDeathBroadcast = true;
		OnDeath.Broadcast();
	}
	else if (Posture >= MaxPosture)
	{
		OnPostureBreak.Broadcast();
	}
}

void UStatComponent::Heal(float Amount)
{
	HP = FMath::Min(MaxHP, HP + Amount);
	OnStatsChanged.Broadcast(this);
}

bool UStatComponent::SpendSanity(float Cost)
{
	if (Sanity < Cost)
	{
		return false;
	}
	Sanity -= Cost;
	OnStatsChanged.Broadcast(this);
	return true;
}

void UStatComponent::RestoreSanity(float Amount)
{
	Sanity = FMath::Min(MaxSanity, Sanity + Amount);
	OnStatsChanged.Broadcast(this);
}

void UStatComponent::RestoreFull()
{
	HP = MaxHP;
	Stamina = MaxStamina;
	Posture = 0.f;
	Sanity = MaxSanity;
	bDeathBroadcast = false;
	OnStatsChanged.Broadcast(this);
}

void UStatComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	if (bDeathBroadcast)
	{
		return;
	}

	const float t = Now();
	bool bChanged = false;

	if (Stamina < MaxStamina && t - LastSpendTime > StaminaRegenDelay)
	{
		Stamina = FMath::Min(MaxStamina, Stamina + StaminaRegen * DeltaTime);
		bChanged = true;
	}

	if (Posture > 0.f && !IsPostureBroken() && t - LastPostureHitTime > PostureRegenDelay)
	{
		Posture = FMath::Max(0.f, Posture - PostureRegen * DeltaTime);
		bChanged = true;
	}

	if (bChanged)
	{
		OnStatsChanged.Broadcast(this);
	}
}
