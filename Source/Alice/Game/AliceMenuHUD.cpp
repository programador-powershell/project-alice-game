#include "Game/AliceMenuHUD.h"
#include "Game/AliceMenuController.h"
#include "Engine/Canvas.h"
#include "Engine/Texture2D.h"

void AAliceMenuHUD::DrawHUD()
{
	Super::DrawHUD();
	if (!Canvas) return;

	const float W = Canvas->SizeX;
	const float H = Canvas->SizeY;
	T += GetWorld() ? GetWorld()->GetDeltaSeconds() : 0.016f;

	// Cheshire art background (cena18) — load once, draw full-screen.
	if (!BgTexture && !bTriedLoad)
	{
		BgTexture = LoadObject<UTexture2D>(nullptr, TEXT("/Game/UI/MainMenu/menu_cheshire_clean.menu_cheshire_clean"));
		bTriedLoad = true;
	}
	if (BgTexture)
	{
		DrawTexture(BgTexture, 0.f, 0.f, W, H, 0.f, 0.f, 1.f, 1.f, FLinearColor(0.92f, 0.9f, 0.96f, 1.f));
	}
	else
	{
		DrawRect(FLinearColor(0.02f, 0.02f, 0.03f, 1.f), 0, 0, W, H); // fallback void
	}

	// Dark scrim (left column) so the options stay legible over the art.
	DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.5f), 0.f, H * 0.56f, W * 0.46f, H * 0.44f);

	const float cx = W * 0.5f;
	// Title
	DrawText(TEXT("PROJECT ALICE"), FLinearColor(0.97f, 0.93f, 0.97f, 1.f), cx - W * 0.135f, H * 0.10f, nullptr, 3.2f);
	DrawText(TEXT("Coração Partido"), FLinearColor(0.78f, 0.18f, 0.30f, 1.f), cx - W * 0.072f, H * 0.185f, nullptr, 1.3f);

	// Options (functional — handled by AAliceMenuController)
	const AAliceMenuController* PC = Cast<AAliceMenuController>(PlayerOwner);
	const int32 Sel = PC ? PC->Selected : 0;
	const float ox = W * 0.06f;
	float oy = H * 0.64f;
	if (PC)
	{
		for (int32 i = 0; i < PC->Options.Num(); ++i)
		{
			const bool bSel = (i == Sel);
			const float pulse = bSel ? (0.7f + 0.3f * FMath::Sin(T * 4.f)) : 1.f;
			const FLinearColor col = bSel
				? FLinearColor(1.f * pulse, 0.85f * pulse, 0.45f * pulse, 1.f)
				: FLinearColor(0.62f, 0.62f, 0.68f, 1.f);
			DrawText((bSel ? TEXT("> ") : TEXT("   ")) + PC->Options[i], col, ox, oy, nullptr, bSel ? 2.0f : 1.5f);
			oy += H * 0.075f;
		}
	}

	DrawText(TEXT("\"Ou talvez... nunca tenha saído.\""), FLinearColor(0.4f, 0.55f, 0.55f, 0.9f), cx - W * 0.12f, H * 0.93f, nullptr, 1.0f);
}
