#include "Game/CheckpointActor.h"
#include "Game/AliceGameMode.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "Components/PointLightComponent.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"

ACheckpointActor::ACheckpointActor()
{
	PrimaryActorTick.bCanEverTick = false;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	TableMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TableMesh"));
	TableMesh->SetupAttachment(Root);
	TableMesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);

	Range = CreateDefaultSubobject<USphereComponent>(TEXT("Range"));
	Range->SetupAttachment(Root);
	Range->SetSphereRadius(280.f);
	Range->SetCollisionProfileName(TEXT("Trigger"));

	Beacon = CreateDefaultSubobject<UPointLightComponent>(TEXT("Beacon"));
	Beacon->SetupAttachment(Root);
	Beacon->SetRelativeLocation(FVector(0.f, 0.f, 120.f));
	Beacon->SetIntensity(4000.f);
	Beacon->SetAttenuationRadius(900.f);
	Beacon->SetSourceRadius(8.f);
}

void ACheckpointActor::BeginPlay()
{
	Super::BeginPlay();

	if (Beacon)
	{
		Beacon->SetLightColor(BeaconColor);
	}
	if (Range)
	{
		Range->OnComponentBeginOverlap.AddDynamic(this, &ACheckpointActor::OnRangeBeginOverlap);
		Range->OnComponentEndOverlap.AddDynamic(this, &ACheckpointActor::OnRangeEndOverlap);
	}
}

void ACheckpointActor::OnRangeBeginOverlap(UPrimitiveComponent*, AActor* OtherActor, UPrimitiveComponent*, int32, bool, const FHitResult&)
{
	APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	if (OtherActor != Player) return;

	if (AAliceGameMode* GM = Cast<AAliceGameMode>(UGameplayStatics::GetGameMode(this)))
	{
		GM->RegisterCheckpoint(GetActorTransform());
		GM->SetPlayerInCheckpoint(true);
	}
}

void ACheckpointActor::OnRangeEndOverlap(UPrimitiveComponent*, AActor* OtherActor, UPrimitiveComponent*, int32)
{
	APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	if (OtherActor != Player) return;

	if (AAliceGameMode* GM = Cast<AAliceGameMode>(UGameplayStatics::GetGameMode(this)))
	{
		GM->SetPlayerInCheckpoint(false);
	}
}
