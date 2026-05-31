"""Diag camera, mesh escala, bounds reais."""
import unreal
L = lambda s: unreal.log(f"[CD] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())

mc=cdo.get_editor_property("mesh")
sm=mc.get_editor_property("skeletal_mesh_asset")
L(f"mesh = {sm.get_name() if sm else None}")
L(f"  rel_loc = {mc.get_editor_property('relative_location')}")
L(f"  rel_rot = {mc.get_editor_property('relative_rotation')}")
L(f"  rel_scale = {mc.get_editor_property('relative_scale3d')}")

# bounds reais do skeletal mesh (cm)
if sm:
    try:
        bb = sm.get_bounds()
        L(f"  mesh bounds box_extent={bb.box_extent}")
    except Exception as e:
        L(f"  bounds err: {e}")

# camera
boom=cdo.get_editor_property("camera_boom")
if boom:
    L(f"Boom.armlen={boom.get_editor_property('target_arm_length')}")
    L(f"Boom.use_pawn_ctrl_rot={boom.get_editor_property('use_pawn_control_rotation')}")
    L(f"Boom.rel_loc={boom.get_editor_property('relative_location')}")

cam=cdo.get_editor_property("follow_camera")
if cam:
    L(f"Cam.rel_loc={cam.get_editor_property('relative_location')}")
    L(f"Cam.use_pawn_ctrl_rot={cam.get_editor_property('use_pawn_control_rotation')}")

# Player Controller view setting?
L("END")
