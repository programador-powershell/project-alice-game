"""Escala o componente mesh (corpo) x100 no BP — mesh veio em metros (1.7u),
UE espera cm. x100 = 1.7m = bate com capsule 176cm.
DressMesh segue via Leader Pose (mesma escala herdada do parent)."""
import unreal
L = lambda s: unreal.log(f"[SC] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")

L(f"scale antes = {mc.get_editor_property('relative_scale3d')}")
mc.set_editor_property("relative_scale3d", unreal.Vector(100,100,100))
# loc tb escala: -88cm fica igual (capsule base)
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
L(f"scale depois = {mc.get_editor_property('relative_scale3d')}")

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP salvo com mesh scale=100")
L("END")
