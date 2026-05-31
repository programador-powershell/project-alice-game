#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "AlicePlayerController.generated.h"

class UUserWidget;

/** Creates the in-game HUD widget and sets game input mode. */
UCLASS()
class ALICE_API AAlicePlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UI") TSubclassOf<UUserWidget> HUDWidgetClass;
	UPROPERTY(BlueprintReadOnly, Category = "UI") TObjectPtr<UUserWidget> HUDWidget;

protected:
	virtual void BeginPlay() override;
};
