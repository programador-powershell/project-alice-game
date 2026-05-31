#include "Game/AlicePlayerController.h"
#include "Blueprint/UserWidget.h"

void AAlicePlayerController::BeginPlay()
{
	Super::BeginPlay();

	if (HUDWidgetClass)
	{
		HUDWidget = CreateWidget<UUserWidget>(this, HUDWidgetClass);
		if (HUDWidget)
		{
			HUDWidget->AddToViewport();
		}
	}

	FInputModeGameOnly Mode;
	SetInputMode(Mode);
	bShowMouseCursor = false;
}
