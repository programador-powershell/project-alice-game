import unreal
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
LES.load_level("/Game/Alice/Maps/L_MargemDoRio")
unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, "alice_margem.png")
unreal.log("[Alice] margem shot done")
