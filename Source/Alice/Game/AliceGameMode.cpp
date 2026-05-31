#include "Game/AliceGameMode.h"
#include "Game/AliceSaveGame.h"
#include "Game/AliceHUD.h"
#include "Game/AlicePlayerController.h"
#include "Player/AliceCharacter.h"
#include "Player/DressComponent.h"
#include "Combat/CombatCharacter.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"
#include "Engine/World.h"

AAliceGameMode::AAliceGameMode()
{
	DefaultPawnClass = AAliceCharacter::StaticClass();
	PlayerControllerClass = AAlicePlayerController::StaticClass();
	HUDClass = AAliceHUD::StaticClass();
}

void AAliceGameMode::BeginPlay()
{
	Super::BeginPlay();
	LoadProgress();
}

void AAliceGameMode::RegisterCheckpoint(const FTransform& Xf)
{
	CheckpointTransform = Xf;
	bHasCheckpoint = true;
}

void AAliceGameMode::OnPlayerRested()
{
	// Heal/flask refill is done by the player; here we persist and (TODO) reset weak mobs.
	SaveProgress();
}

void AAliceGameMode::OnPlayerDied(APawn* Pawn)
{
	DeadPawn = Pawn;
	SaveProgress(); // soulslike: progress (minus dropped Ergo) persists
	GetWorldTimerManager().SetTimer(RespawnTimer, this, &AAliceGameMode::RespawnPlayer, RespawnDelay, false);
}

void AAliceGameMode::RespawnPlayer()
{
	APawn* Pawn = DeadPawn.Get();
	if (!Pawn)
	{
		Pawn = UGameplayStatics::GetPlayerPawn(this, 0);
	}
	if (!Pawn) return;

	if (bHasCheckpoint)
	{
		Pawn->SetActorTransform(CheckpointTransform, false, nullptr, ETeleportType::TeleportPhysics);
	}
	if (ACombatCharacter* C = Cast<ACombatCharacter>(Pawn))
	{
		C->Revive();
	}
	if (AAliceCharacter* Alice = Cast<AAliceCharacter>(Pawn))
	{
		Alice->FlaskCharges = Alice->MaxFlaskCharges;
	}
}

void AAliceGameMode::SaveProgress()
{
	UAliceSaveGame* Save = Cast<UAliceSaveGame>(UGameplayStatics::CreateSaveGameObject(UAliceSaveGame::StaticClass()));
	if (!Save) return;

	Save->bHasCheckpoint = bHasCheckpoint;
	Save->CheckpointTransform = CheckpointTransform;

	if (AAliceCharacter* Alice = Cast<AAliceCharacter>(UGameplayStatics::GetPlayerPawn(this, 0)))
	{
		Save->Ergo = Alice->Ergo;
		Save->SoulLevel = Alice->SoulLevel;
		if (Alice->Dresses)
		{
			for (const FDressState& D : Alice->Dresses->Dresses)
			{
				if (D.bUnlocked)
				{
					Save->UnlockedDresses.Add(static_cast<uint8>(D.Type));
				}
			}
		}
	}

	UGameplayStatics::SaveGameToSlot(Save, SaveSlot, 0);
}

void AAliceGameMode::LoadProgress()
{
	if (!UGameplayStatics::DoesSaveGameExist(SaveSlot, 0)) return;

	UAliceSaveGame* Save = Cast<UAliceSaveGame>(UGameplayStatics::LoadGameFromSlot(SaveSlot, 0));
	if (!Save) return;

	bHasCheckpoint = Save->bHasCheckpoint;
	CheckpointTransform = Save->CheckpointTransform;
	PendingErgo = Save->Ergo;
	PendingLevel = Save->SoulLevel;
	PendingDresses = Save->UnlockedDresses;
	bHasPendingLoad = true;

	GetWorldTimerManager().SetTimer(ApplyLoadTimer, this, &AAliceGameMode::ApplyLoadedToPlayer, 0.3f, false);
}

void AAliceGameMode::ApplyLoadedToPlayer()
{
	if (!bHasPendingLoad) return;

	AAliceCharacter* Alice = Cast<AAliceCharacter>(UGameplayStatics::GetPlayerPawn(this, 0));
	if (!Alice)
	{
		// player not spawned yet — retry shortly
		GetWorldTimerManager().SetTimer(ApplyLoadTimer, this, &AAliceGameMode::ApplyLoadedToPlayer, 0.3f, false);
		return;
	}

	Alice->AddErgo(PendingErgo);
	Alice->SoulLevel = PendingLevel;
	if (Alice->Dresses)
	{
		for (uint8 D : PendingDresses)
		{
			Alice->Dresses->UnlockDress(static_cast<EDressType>(D));
		}
		Alice->Dresses->EquipDress(EDressType::None);
	}
	if (bHasCheckpoint)
	{
		Alice->SetActorTransform(CheckpointTransform, false, nullptr, ETeleportType::TeleportPhysics);
	}
	bHasPendingLoad = false;
}
