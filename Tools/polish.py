"""Tune L_Arena lighting/exposure down + reframe + re-screenshot."""
import unreal

LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
UES = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

LES.load_level("/Game/Alice/Maps/L_Arena")

for a in EAS.get_all_level_actors():
    try:
        if isinstance(a, unreal.DirectionalLight):
            a.get_component_by_class(unreal.DirectionalLightComponent).set_intensity(2.2)
        elif isinstance(a, unreal.SkyLight):
            a.get_component_by_class(unreal.SkyLightComponent).set_intensity(0.7)
        elif isinstance(a, unreal.PointLight):
            a.get_component_by_class(unreal.PointLightComponent).set_intensity(4500.0)
        elif isinstance(a, unreal.PostProcessVolume):
            s = a.get_editor_property("settings")
            s.set_editor_property("override_auto_exposure_bias", True)
            s.set_editor_property("auto_exposure_bias", -1.0)
            s.set_editor_property("override_bloom_intensity", True)
            s.set_editor_property("bloom_intensity", 0.4)
            a.set_editor_property("settings", s)
    except Exception as e:
        unreal.log_warning("polish %s: %s" % (a, e))

# Frame the boss end of the arena from the player-start side.
try:
    UES.set_level_viewport_camera_info(unreal.Vector(0.0, -1400.0, 380.0), unreal.Rotator(roll=0.0, pitch=-12.0, yaw=90.0))
except Exception as e:
    unreal.log_warning("camera: %s" % e)

LES.save_current_level()
unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, "alice_arena2.png")
unreal.log("[Alice] POLISH DONE")
