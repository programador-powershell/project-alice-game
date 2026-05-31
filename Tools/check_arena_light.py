"""Diagnostica L_Arena: luzes, PlayerStart, e confirma BP_Alice usa coelho.
'Tudo escuro' = provavel falta de luz ou PlayerStart em lugar ruim."""
import unreal
L = lambda s: unreal.log(f"[AL] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()

lights=0; dirlight=0; skylight=0; ps_loc=None
for a in actors:
    cn = a.get_class().get_name()
    if "Light" in cn:
        lights+=1
        if "Directional" in cn: dirlight+=1
        if "Sky" in cn: skylight+=1
        L(f"  luz: {cn} '{a.get_actor_label()}'")
    if "PlayerStart" in cn:
        ps_loc = a.get_actor_location()
        L(f"  PlayerStart em {ps_loc}")
L(f"TOTAL luzes={lights} (directional={dirlight} sky={skylight})")

# confirma player mesh
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
m = cdo.get_editor_property("mesh").get_editor_property("skeletal_mesh_asset")
L(f"BP_Alice.mesh = {m.get_name() if m else None}")
L("END")
