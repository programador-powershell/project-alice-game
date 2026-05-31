#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "AliceMenuHUD.generated.h"

class UTexture2D;

/** Canvas main menu: Cheshire art background (cena18) + PROJECT ALICE title + options. */
UCLASS()
class ALICE_API AAliceMenuHUD : public AHUD
{
	GENERATED_BODY()

public:
	virtual void DrawHUD() override;

private:
	float T = 0.f;
	bool bTriedLoad = false;
	UPROPERTY() TObjectPtr<UTexture2D> BgTexture = nullptr;
};
