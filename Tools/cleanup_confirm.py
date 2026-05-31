import unreal
L = lambda s: unreal.log(f"[CF] {s}")
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
n=0
for a in eas.get_all_level_actors():
    if a.get_actor_label() in ("TestAliceAnim",):
        eas.destroy_actor(a); n+=1
L(f"removidos test actors: {n}")
unreal.EditorLoadingAndSavingUtils.save_current_level()
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
m = mc.get_editor_property("skeletal_mesh_asset")
L(f"BP_Alice.mesh = {m.get_name() if m else None}")
L(f"BP_Alice.rot  = {mc.get_editor_property('relative_rotation')}")
L("READY_TO_PLAY")
