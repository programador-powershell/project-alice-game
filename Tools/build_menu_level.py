"""Build L_MainMenu (empty level + MenuGameMode); the Canvas HUD draws the menu over black."""
import unreal

LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

LES.new_level("/Game/Alice/Maps/L_MainMenu")

# A faint light so the world isn't pure error-black behind the HUD (HUD covers it anyway).
sun = EAS.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 500),
                                 unreal.Rotator(roll=0, pitch=-45, yaw=0))
if sun:
    sun.set_actor_label("MenuLight")

try:
    ws = unreal.EditorLevelLibrary.get_editor_world().get_world_settings()
    ws.set_editor_property("default_game_mode", unreal.AliceMenuGameMode)
    unreal.log("[Alice] MENU gamemode set")
except Exception as e:
    unreal.log_warning("[Alice] MENU gm: %s" % e)

LES.save_current_level()
unreal.EditorAssetLibrary.save_directory("/Game/Alice/Maps", False, True)
unreal.log("[Alice] MENU LEVEL DONE")
