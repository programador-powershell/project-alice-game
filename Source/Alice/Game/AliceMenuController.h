#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "AliceMenuController.generated.h"

/** Keyboard/gamepad-driven main-menu controller (no UMG). Up/Down to move, Enter to confirm. */
UCLASS()
class ALICE_API AAliceMenuController : public APlayerController
{
	GENERATED_BODY()

public:
	AAliceMenuController();

	UPROPERTY(BlueprintReadOnly, Category = "Menu") int32 Selected = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Menu") TArray<FString> Options;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Menu") FName FirstLevel = "L_MargemDoRio";

protected:
	virtual void BeginPlay() override;
	virtual void SetupInputComponent() override;

	void MoveUp();
	void MoveDown();
	void Confirm();
};
