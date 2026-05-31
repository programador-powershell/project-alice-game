#include "Game/AliceMenuController.h"
#include "Components/InputComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"

AAliceMenuController::AAliceMenuController()
{
	Options = { TEXT("Novo Jogo"), TEXT("Continuar"), TEXT("Configurações"), TEXT("Sair") };
}

void AAliceMenuController::BeginPlay()
{
	Super::BeginPlay();
	bShowMouseCursor = false;
	FInputModeGameOnly Mode;
	SetInputMode(Mode);
}

void AAliceMenuController::SetupInputComponent()
{
	Super::SetupInputComponent();
	if (!InputComponent) return;

	InputComponent->BindKey(EKeys::Up, IE_Pressed, this, &AAliceMenuController::MoveUp);
	InputComponent->BindKey(EKeys::W, IE_Pressed, this, &AAliceMenuController::MoveUp);
	InputComponent->BindKey(EKeys::Gamepad_DPad_Up, IE_Pressed, this, &AAliceMenuController::MoveUp);
	InputComponent->BindKey(EKeys::Down, IE_Pressed, this, &AAliceMenuController::MoveDown);
	InputComponent->BindKey(EKeys::S, IE_Pressed, this, &AAliceMenuController::MoveDown);
	InputComponent->BindKey(EKeys::Gamepad_DPad_Down, IE_Pressed, this, &AAliceMenuController::MoveDown);
	InputComponent->BindKey(EKeys::Enter, IE_Pressed, this, &AAliceMenuController::Confirm);
	InputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &AAliceMenuController::Confirm);
	InputComponent->BindKey(EKeys::LeftMouseButton, IE_Pressed, this, &AAliceMenuController::Confirm);
	InputComponent->BindKey(EKeys::Gamepad_FaceButton_Bottom, IE_Pressed, this, &AAliceMenuController::Confirm);
}

void AAliceMenuController::MoveUp()
{
	const int32 N = FMath::Max(1, Options.Num());
	Selected = (Selected - 1 + N) % N;
}

void AAliceMenuController::MoveDown()
{
	const int32 N = FMath::Max(1, Options.Num());
	Selected = (Selected + 1) % N;
}

void AAliceMenuController::Confirm()
{
	switch (Selected)
	{
	case 0: // Novo Jogo
	case 1: // Continuar (save is loaded by the GameMode on level start)
		UGameplayStatics::OpenLevel(this, FirstLevel);
		break;
	case 2: // Configurações — TODO
		break;
	case 3: // Sair
		UKismetSystemLibrary::QuitGame(this, this, EQuitPreference::Quit, false);
		break;
	default:
		break;
	}
}
