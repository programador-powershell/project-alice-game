#include "Game/AliceHUD.h"
#include "Player/AliceCharacter.h"
#include "Player/DressComponent.h"
#include "Combat/StatComponent.h"
#include "Enemy/BossCharacter.h"
#include "Engine/Canvas.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"

void AAliceHUD::Bar(float X, float Y, float W, float H, float Pct, const FLinearColor& Fill, const FLinearColor& Bg)
{
	DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.6f), X - 2.f, Y - 2.f, W + 4.f, H + 4.f);
	DrawRect(Bg, X, Y, W, H);
	DrawRect(Fill, X, Y, W * FMath::Clamp(Pct, 0.f, 1.f), H);
}

void AAliceHUD::DrawCentered(const FString& Text, float CenterX, float Y, float Scale, const FLinearColor& Color)
{
	float W = 0.f, H = 0.f;
	GetTextSize(Text, W, H, nullptr, Scale);
	DrawText(Text, Color, CenterX - W * 0.5f, Y, nullptr, Scale);
}

void AAliceHUD::DrawHUD()
{
	Super::DrawHUD();
	if (!Canvas)
	{
		return;
	}

	const float SW = Canvas->SizeX;
	const float SH = Canvas->SizeY;

	// Area title card (roteiro §4 scene names) — resolved once, fades in/out on entry.
	if (LevelStartTime < 0.f)
	{
		LevelStartTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
		const FString Map = GetWorld() ? GetWorld()->GetMapName() : FString();
		if      (Map.Contains(TEXT("MargemDoRio")))      { AreaTitle = TEXT("Margem do Rio");      AreaSubtitle = TEXT("O Despertar Falso"); }
		else if (Map.Contains(TEXT("Vortice")))          { AreaTitle = TEXT("Vórtice");            AreaSubtitle = TEXT("A Queda"); }
		else if (Map.Contains(TEXT("TocaMecanica")))     { AreaTitle = TEXT("Toca Mecânica");      AreaSubtitle = TEXT("O Mensageiro do Tempo"); }
		else if (Map.Contains(TEXT("Arena")))            { AreaTitle = TEXT("Arena Temporal");     AreaSubtitle = TEXT(""); }
		else if (Map.Contains(TEXT("FlorestaCheshire"))) { AreaTitle = TEXT("Floresta Cheshire");  AreaSubtitle = TEXT("O Sorriso na Escuridão"); }
		else if (Map.Contains(TEXT("InteriorDeCha")))    { AreaTitle = TEXT("Interior do Chá");    AreaSubtitle = TEXT(""); }
		else if (Map.Contains(TEXT("SalaoCha")))         { AreaTitle = TEXT("Salão do Chá");       AreaSubtitle = TEXT("O Chá Eterno"); }
		else if (Map.Contains(TEXT("NevoaCogumelos")))   { AreaTitle = TEXT("Névoa de Cogumelos"); AreaSubtitle = TEXT("A Guardiã do Sonho"); }
		else if (Map.Contains(TEXT("PatioReal")))        { AreaTitle = TEXT("Pátio Real");         AreaSubtitle = TEXT("A Soberana Escarlate"); }
		else if (Map.Contains(TEXT("Ruinas")))           { AreaTitle = TEXT("Ruínas da Coroa");    AreaSubtitle = TEXT("O Coração Partido"); }
		else if (Map.Contains(TEXT("CampoEtereo")))      { AreaTitle = TEXT("Campo Etéreo");       AreaSubtitle = TEXT("Reencontro"); }
		else                                             { AreaTitle = TEXT(""); AreaSubtitle = TEXT(""); }
	}
	{
		const float Tt = (GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f) - LevelStartTime;
		if (!AreaTitle.IsEmpty() && Tt >= 0.f && Tt < 6.0f)
		{
			float A = 1.f;
			if (Tt < 0.6f) A = Tt / 0.6f;
			else if (Tt > 4.5f) A = FMath::Max(0.f, 1.f - (Tt - 4.5f) / 1.5f);
			DrawCentered(AreaTitle, SW * 0.5f, SH * 0.30f, 2.6f, FLinearColor(0.96f, 0.93f, 0.86f, A));
			if (!AreaSubtitle.IsEmpty())
			{
				DrawCentered(AreaSubtitle, SW * 0.5f, SH * 0.30f + 44.f, 1.2f, FLinearColor(0.85f, 0.78f, 0.70f, A));
			}
		}
	}

	APawn* P = PlayerOwner ? PlayerOwner->GetPawn() : nullptr;
	if (AAliceCharacter* Alice = Cast<AAliceCharacter>(P))
	{
		if (UStatComponent* S = Alice->GetStats())
		{
			const float X = 48.f;
			const float Y = SH - 130.f;
			const float W = 420.f;

			Bar(X, Y, W, 20.f, S->GetHPPercent(), FLinearColor(0.80f, 0.10f, 0.12f), FLinearColor(0.12f, 0.02f, 0.02f));
			Bar(X, Y + 26.f, W * 0.82f, 12.f, S->GetStaminaPercent(), FLinearColor(0.25f, 0.80f, 0.32f), FLinearColor(0.03f, 0.07f, 0.03f));
			Bar(X, Y + 42.f, W * 0.82f, 8.f, S->GetPosturePercent(), FLinearColor(0.95f, 0.75f, 0.20f), FLinearColor(0.06f, 0.05f, 0.02f));
			Bar(X, Y + 54.f, W * 0.82f, 8.f, S->GetSanityPercent(), FLinearColor(0.30f, 0.62f, 1.0f), FLinearColor(0.02f, 0.04f, 0.09f));

			float Corr = Alice->Dresses ? Alice->Dresses->GetCurrentCorruption() / 100.f : 0.f;
			Bar(X, Y + 66.f, W * 0.82f, 8.f, Corr, FLinearColor(0.62f, 0.10f, 0.82f), FLinearColor(0.05f, 0.02f, 0.06f));

				// Active dress + its skill (so the player knows what the Sanity buys)
				FString DressName = TEXT("Vestido Base"), SkillName = TEXT("Faca");
				switch (Alice->Dresses ? Alice->Dresses->Current : EDressType::None)
				{
				case EDressType::Coelho:     DressName = TEXT("Coelho Branco");   SkillName = TEXT("Fratura do Tempo"); break;
				case EDressType::Cheshire:   DressName = TEXT("Cheshire");          SkillName = TEXT("Passo Sombrio");    break;
				case EDressType::Chapeleiro: DressName = TEXT("Chapeleiro");         SkillName = TEXT("Rabisco do Caos");  break;
				case EDressType::Lagarta:    DressName = TEXT("Lagarta Azul");       SkillName = TEXT("Fumaca do Sonho");  break;
				case EDressType::Rainha:     DressName = TEXT("Rainha de Copas");    SkillName = TEXT("Corte Real");       break;
				default: break;
				}
				DrawText(FString::Printf(TEXT("%s  -  %s"), *DressName, *SkillName), FLinearColor(0.85f, 0.80f, 0.96f), X, Y + 78.f);

				// Corrupção do Coração (Lídia's status build-up) — only while it is filling.
				const float Heart = Alice->GetHeartCorruptionPercent();
				if (Heart > 0.f)
				{
					Bar(X, Y + 94.f, W * 0.82f, 8.f, Heart, FLinearColor(0.88f, 0.06f, 0.36f), FLinearColor(0.09f, 0.0f, 0.03f));
				}

			DrawText(FString::Printf(TEXT("Chá (cura): %d"), Alice->FlaskCharges), FLinearColor(1.f, 0.95f, 0.85f), X, Y - 28.f);
			DrawText(FString::Printf(TEXT("Ergo: %d"), Alice->Ergo), FLinearColor(0.95f, 0.85f, 0.5f), SW - 220.f, 44.f);
		}
	}

	// Boss bar (first engaged, living boss)
	TArray<AActor*> Bosses;
	UGameplayStatics::GetAllActorsOfClass(this, ABossCharacter::StaticClass(), Bosses);
	for (AActor* BA : Bosses)
	{
		ABossCharacter* B = Cast<ABossCharacter>(BA);
		if (!B || B->IsDeadChar() || !B->IsAggro())
		{
			continue;
		}
		if (UStatComponent* BS = B->GetStats())
		{
			const float BW = SW * 0.5f;
			const float BX = (SW - BW) * 0.5f;
			const float BY = SH - 64.f;
			const FLinearColor PhaseColor = (B->Phase >= 2) ? FLinearColor(0.55f, 0.10f, 0.55f) : FLinearColor(0.78f, 0.12f, 0.12f);
			Bar(BX, BY, BW, 16.f, BS->GetHPPercent(), PhaseColor, FLinearColor(0.08f, 0.02f, 0.02f));
			DrawText(B->BossName.ToString(), FLinearColor(1.f, 0.92f, 0.92f), BX, BY - 28.f, nullptr, 1.2f);
			if (!B->BossSubtitle.IsEmpty())
			{
				DrawText(B->BossSubtitle.ToString(), FLinearColor(0.8f, 0.7f, 0.7f), BX, BY - 10.f);
			}
		}
		break;
	}
}
