#include "Game/AliceMenuGameMode.h"
#include "Game/AliceMenuController.h"
#include "Game/AliceMenuHUD.h"
#include "GameFramework/SpectatorPawn.h"

AAliceMenuGameMode::AAliceMenuGameMode()
{
	PlayerControllerClass = AAliceMenuController::StaticClass();
	HUDClass = AAliceMenuHUD::StaticClass();
	DefaultPawnClass = ASpectatorPawn::StaticClass();
}
