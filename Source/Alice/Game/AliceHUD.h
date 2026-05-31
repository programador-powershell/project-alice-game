#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "AliceHUD.generated.h"

/**
 * Canvas-drawn HUD (no UMG asset needed): player HP / stamina / posture / sanity /
 * dress-corruption bars + Ergo + teacup flask count, and a centered boss bar with
 * the boss name when a boss is engaged. Styled after lidia-boss.png.
 */
UCLASS()
class ALICE_API AAliceHUD : public AHUD
{
	GENERATED_BODY()

public:
	virtual void DrawHUD() override;

private:
	void Bar(float X, float Y, float W, float H, float Pct, const FLinearColor& Fill, const FLinearColor& Bg);
	void DrawCentered(const FString& Text, float CenterX, float Y, float Scale, const FLinearColor& Color);

	// Area title card (soulslike scene-name intro, roteiro §4)
	float LevelStartTime = -1.f;
	FString AreaTitle;
	FString AreaSubtitle;
};
