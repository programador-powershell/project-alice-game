#include "Player/DressComponent.h"
#include "Combat/StatComponent.h"

UDressComponent::UDressComponent()
{
	PrimaryComponentTick.bCanEverTick = false;

	// Seed the 5 dresses with canonical petal colors (from art briefs / roteiro §6.1).
	auto Make = [](EDressType T, const FLinearColor& C, const FName& Skill)
	{
		FDressState S; S.Type = T; S.PetalColor = C; S.SkillName = Skill; S.bUnlocked = false; return S;
	};
	Dresses.Add(Make(EDressType::Coelho,     FLinearColor(0.30f, 0.45f, 1.0f), "FracturaDoTempo"));
	Dresses.Add(Make(EDressType::Cheshire,   FLinearColor(0.55f, 0.20f, 0.85f), "PassoSombrio"));
	Dresses.Add(Make(EDressType::Chapeleiro, FLinearColor(0.25f, 0.85f, 0.35f), "RabiscoDoCaos"));
	Dresses.Add(Make(EDressType::Lagarta,    FLinearColor(0.20f, 0.55f, 1.0f), "FumacaDoSonho"));
	Dresses.Add(Make(EDressType::Rainha,     FLinearColor(0.90f, 0.12f, 0.18f), "CorteReal"));
}

void UDressComponent::BeginPlay()
{
	Super::BeginPlay();
}

int32 UDressComponent::IndexOf(EDressType Type) const
{
	for (int32 i = 0; i < Dresses.Num(); ++i)
	{
		if (Dresses[i].Type == Type) return i;
	}
	return INDEX_NONE;
}

void UDressComponent::UnlockDress(EDressType Type)
{
	const int32 Idx = IndexOf(Type);
	if (Idx != INDEX_NONE)
	{
		Dresses[Idx].bUnlocked = true;
		EquipDress(Type);
	}
}

void UDressComponent::EquipDress(EDressType Type)
{
	if (Type == EDressType::None)
	{
		Current = EDressType::None;
		OnDressChanged.Broadcast(Current);
		return;
	}
	const int32 Idx = IndexOf(Type);
	if (Idx != INDEX_NONE && Dresses[Idx].bUnlocked)
	{
		Current = Type;
		OnDressChanged.Broadcast(Current);
	}
}

void UDressComponent::CycleDress(float Direction)
{
	// Build the list of unlocked dresses (+ base) and step through it.
	TArray<EDressType> Avail;
	Avail.Add(EDressType::None);
	for (const FDressState& S : Dresses)
	{
		if (S.bUnlocked) Avail.Add(S.Type);
	}
	if (Avail.Num() <= 1) return;

	int32 Cur = Avail.IndexOfByKey(Current);
	if (Cur == INDEX_NONE) Cur = 0;
	const int32 Step = Direction >= 0.f ? 1 : -1;
	const int32 Next = (Cur + Step + Avail.Num()) % Avail.Num();
	EquipDress(Avail[Next]);
}

bool UDressComponent::UseSkill()
{
	if (Current == EDressType::None) return false;
	const int32 Idx = IndexOf(Current);
	if (Idx == INDEX_NONE || !Dresses[Idx].bUnlocked) return false;

	if (UStatComponent* Stats = GetOwner()->FindComponentByClass<UStatComponent>())
	{
		if (!Stats->SpendSanity(Dresses[Idx].SkillSanityCost))
		{
			return false; // not enough sanity
		}
	}

	OnSkillUsed.Broadcast(Current);
	AddCorruption(Idx, CorruptionPerSkill);
	return true;
}

void UDressComponent::AddCorruption(int32 DressIdx, float Amount)
{
	if (!Dresses.IsValidIndex(DressIdx)) return;

	Dresses[DressIdx].Corruption = FMath::Clamp(Dresses[DressIdx].Corruption + Amount, 0.f, 100.f);
	OnCorruptionChanged.Broadcast(Dresses[DressIdx].Type, Dresses[DressIdx].Corruption);

	if (Dresses[DressIdx].Corruption >= 100.f)
	{
		// Full transformation burst, then restore (roteiro §6.1).
		OnDressTransform.Broadcast(Dresses[DressIdx].Type);
		Dresses[DressIdx].Corruption = 0.f;
		OnCorruptionChanged.Broadcast(Dresses[DressIdx].Type, 0.f);

		if (UStatComponent* Stats = GetOwner()->FindComponentByClass<UStatComponent>())
		{
			Stats->RestoreSanity(Stats->MaxSanity * 0.4f);
		}
	}
}

FLinearColor UDressComponent::GetCurrentPetalColor() const
{
	const int32 Idx = IndexOf(Current);
	return Idx != INDEX_NONE ? Dresses[Idx].PetalColor : FLinearColor(0.82f, 0.80f, 0.91f); // default #D0CCE8
}

float UDressComponent::GetCurrentCorruption() const
{
	const int32 Idx = IndexOf(Current);
	return Idx != INDEX_NONE ? Dresses[Idx].Corruption : 0.f;
}
