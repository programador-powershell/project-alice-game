"""Corrige movimento do BP_Alice:
- JumpZVelocity 0 -> 500 (pulo funciona)
- AirControl 0 -> 0.35 (controle no ar)
- bOrientRotationToMovement True (vira pra onde anda = fluidez)
- JumpMaxCount >= 1
Compila + salva.
"""
import unreal
L = lambda s: unreal.log(f"[MV] {s}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
cm = cdo.get_component_by_class(unreal.CharacterMovementComponent)

cm.set_editor_property("jump_z_velocity", 500.0)
cm.set_editor_property("air_control", 0.35)
cm.set_editor_property("orient_rotation_to_movement", True)
cm.set_editor_property("rotation_rate", unreal.Rotator(0, 540, 0))
cm.set_editor_property("max_walk_speed", 600.0)
cm.set_editor_property("max_acceleration", 2048.0)
try:
    cdo.set_editor_property("jump_max_count", 1)
except Exception as e: L(f"jumpcount err {e}")
# garante que o mesh roda anim no PIE
L("JumpZ=500 AirControl=0.35 OrientToMovement=True RotRate=540")

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("compilado+salvo")

# re-verifica
gc = bp.generated_class()
c2 = unreal.get_default_object(gc).get_component_by_class(unreal.CharacterMovementComponent)
L(f"pos-compile JumpZ={c2.get_editor_property('jump_z_velocity')} Orient={c2.get_editor_property('orient_rotation_to_movement')}")
L("END")
