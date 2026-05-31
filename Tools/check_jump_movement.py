"""Checa CharacterMovement do BP_Alice: JumpZVelocity, MaxWalkSpeed, gravity,
e se Jump bind existe. 'Pulo nao funciona' costuma ser JumpZVelocity=0 ou
bOrientRotationToMovement / can-jump."""
import unreal
L = lambda s: unreal.log(f"[JM] {s}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())

cm = cdo.get_component_by_class(unreal.CharacterMovementComponent)
if cm:
    L(f"JumpZVelocity = {cm.get_editor_property('jump_z_velocity')}")
    L(f"MaxWalkSpeed = {cm.get_editor_property('max_walk_speed')}")
    L(f"GravityScale = {cm.get_editor_property('gravity_scale')}")
    L(f"AirControl = {cm.get_editor_property('air_control')}")
    L(f"bOrientRotationToMovement = {cm.get_editor_property('orient_rotation_to_movement')}")
else:
    L("sem CharacterMovementComponent")

# Character can jump?
try:
    L(f"JumpMaxCount = {cdo.get_editor_property('jump_max_count')}")
except Exception as e: L(f"jump_max_count err {e}")

# bUseControllerRotationYaw (afeta orientacao)
L(f"bUseControllerRotationYaw = {cdo.get_editor_property('use_controller_rotation_yaw')}")
L("END")
