"""Diag camera: TargetArmLength + CameraBoom + mesh location."""
import unreal
L = lambda s: unreal.log(f"[CM] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())

# CameraBoom (SpringArm)
boom=cdo.get_editor_property("camera_boom")
if boom:
    L(f"CameraBoom.TargetArmLength = {boom.get_editor_property('target_arm_length')}")
    L(f"CameraBoom.SocketOffset = {boom.get_editor_property('socket_offset')}")
    L(f"CameraBoom.RelativeLoc = {boom.get_editor_property('relative_location')}")

# Mesh
mc=cdo.get_editor_property("mesh")
sm=mc.get_editor_property("skeletal_mesh_asset")
L(f"mesh asset = {sm.get_name() if sm else None}")
L(f"mesh rel_loc = {mc.get_editor_property('relative_location')}")
L(f"mesh rel_rot = {mc.get_editor_property('relative_rotation')}")
L(f"mesh anim_mode = {mc.get_editor_property('animation_mode')}")

# Capsule
caps=cdo.get_component_by_class(unreal.CapsuleComponent)
if caps:
    L(f"Capsule HalfHeight = {caps.get_editor_property('capsule_half_height')}")
    L(f"Capsule Radius = {caps.get_editor_property('capsule_radius')}")
L("END")
