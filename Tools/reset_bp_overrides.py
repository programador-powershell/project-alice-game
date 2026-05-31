"""Reset overrides do BP_Alice nos componentes camera/mesh pros defaults do C++.
BP guarda valores set via Python que vencem o construtor. Limpa eles."""
import unreal
L=lambda s:unreal.log(f"[RST] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())

# CameraBoom: forca defaults C++
boom=cdo.get_editor_property("camera_boom")
if boom:
    boom.set_editor_property("target_arm_length", 400.0)
    boom.set_editor_property("do_collision_test", False)
    boom.set_editor_property("use_pawn_control_rotation", True)
    boom.set_editor_property("socket_offset", unreal.Vector(0,0,90))
    boom.set_editor_property("relative_location", unreal.Vector(0,0,0))
    boom.set_editor_property("relative_rotation", unreal.Rotator(0,0,0))
    L(f"boom armlen={boom.get_editor_property('target_arm_length')} collision={boom.get_editor_property('do_collision_test')}")

cam=cdo.get_editor_property("follow_camera")
if cam:
    cam.set_editor_property("use_pawn_control_rotation", False)
    cam.set_editor_property("relative_location", unreal.Vector(0,0,0))
    L("cam reset")

# Mesh
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_scale3d", unreal.Vector(1,1,1))
L(f"mesh rot={mc.get_editor_property('relative_rotation')}")

# Controller rotation flags no pawn
cdo.set_editor_property("use_controller_rotation_yaw", False)
cdo.set_editor_property("use_controller_rotation_pitch", False)
cdo.set_editor_property("use_controller_rotation_roll", False)

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP reset+salvo")
L("END")
