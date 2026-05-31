using UnrealBuildTool;

public class Alice : ModuleRules
{
	public Alice(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		// Flat module layout (no Public/Private split) — let headers be included as "Combat/Foo.h".
		PublicIncludePaths.AddRange(new string[] { ModuleDirectory });

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"GameplayTags",
			"AIModule",
			"GameplayTasks",
			"UMG",
			"Slate",
			"SlateCore",
			"Niagara",
			"MotionWarping"
		});

		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
