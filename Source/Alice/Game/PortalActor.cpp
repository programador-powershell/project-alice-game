#include "Game/PortalActor.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/Character.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"

APortalActor::APortalActor()
{
	PrimaryActorTick.bCanEverTick = false;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	VortexMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VortexMesh"));
	VortexMesh->SetupAttachment(Root);
	VortexMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);

	Trigger = CreateDefaultSubobject<UBoxComponent>(TEXT("Trigger"));
	Trigger->SetupAttachment(Root);
	Trigger->SetBoxExtent(FVector(120.f, 120.f, 160.f));
	Trigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	Trigger->SetCollisionResponseToAllChannels(ECR_Overlap);
}

void APortalActor::BeginPlay()
{
	Super::BeginPlay();
	if (Trigger)
	{
		Trigger->OnComponentBeginOverlap.AddDynamic(this, &APortalActor::OnOverlap);
	}
}

void APortalActor::OnOverlap(UPrimitiveComponent* /*OverlappedComp*/, AActor* OtherActor,
	UPrimitiveComponent* /*OtherComp*/, int32 /*OtherBodyIndex*/,
	bool /*bFromSweep*/, const FHitResult& /*Sweep*/)
{
	if (bTriggered || TargetLevel.IsNone()) return;
	if (!Cast<ACharacter>(OtherActor)) return;          // only the player/characters
	if (OtherActor != UGameplayStatics::GetPlayerPawn(this, 0)) return;

	bTriggered = true;

	// Camera fade to black, then travel.
	if (APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0))
	{
		PC->PlayerCameraManager->StartCameraFade(0.f, 1.f, FMath::Max(0.1f, Delay), FLinearColor::Black, false, true);
	}

	FTimerHandle T;
	GetWorldTimerManager().SetTimer(
		T,
		FTimerDelegate::CreateLambda([this]() { UGameplayStatics::OpenLevel(this, TargetLevel); }),
		FMath::Max(0.1f, Delay), false);
}
