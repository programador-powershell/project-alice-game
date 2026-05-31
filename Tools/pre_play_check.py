"""Garante L_Arena carregado, sem test actors, BP_Alice = SK_AliceVestido, e salva."""
import unreal
L = lambda s: unreal.log(f"[PRE] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
n=0
for a in eas.get_all_level_actors():
    if a.get_actor_label() in ("TestAliceAnim",):
        eas.destroy_actor(a); n+=1
L(f"test actors removidos: {n}")
unreal.EditorLoadingAndSavingUtils.save_current_level()

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
m = mc.get_editor_property("skeletal_mesh_asset")
L(f"BP_Alice.mesh = {m.get_name() if m else None}")
L(f"BP_Alice.rot  = {mc.get_editor_property('relative_rotation')}")
matname = None
sk = m
if sk and sk.materials:
    mi = sk.materials[0].material_interface
    matname = mi.get_name() if mi else None
L(f"mesh material[0] = {matname}")
L("PRONTO — pode dar Alt+P no L_Arena")
