using UnrealBuildTool;
using System.Collections.Generic;

public class AliceTarget : TargetRules
{
	public AliceTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("Alice");
	}
}
