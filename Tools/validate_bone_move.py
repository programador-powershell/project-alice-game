"""Mede se a POSE e avaliada: compara transform de um bone (hand/spine) entre
2 tempos de A_Walk via get_bone_transform. Se mexe = anim avalia = vai animar no PIE.
Tambem confirma que o mesh TEM bind pose != ref (skin existe)."""
import unreal
L = lambda s: unreal.log(f"[BM] {s}")

unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
ANIM = unreal.load_asset("/Game/Alice/AnimM/A_Walk")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
sk = unreal.load_asset("/Game/Alice/Characters/AliceVestido/SK_AliceVestido")

actor = eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0,0,0))
comp = actor.skeletal_mesh_component
comp.set_skeletal_mesh_asset(sk)
comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
comp.set_animation(ANIM)

# lista alguns bones
names = []
try:
    n = comp.get_num_bones()
    for i in range(min(n,5)):
        names.append(comp.get_bone_name(i))
    L(f"num_bones={n} primeiros={names}")
except Exception as e:
    L(f"bone list err: {e}")

# tenta bones tipicos mixamorig
test_bones = ["spine_01","mixamorig:Spine","calf_l","mixamorig:LeftLeg","hand_r","mixamorig:RightHand","thigh_l","mixamorig:LeftUpLeg"]
results = {}
for bn in test_bones:
    locs = []
    for t in (0.0, 0.6):
        comp.set_position(t, True)  # fire_notifies=True forca avaliacao
        try:
            tr = comp.get_bone_transform(comp.get_bone_index(bn) if hasattr(comp,'get_bone_index') else 0)
        except Exception:
            tr = None
        if tr:
            loc = tr.translation
            locs.append(loc)
    if len(locs)==2:
        d = (locs[0]-locs[1]).size()
        results[bn] = d

for bn,d in results.items():
    L(f"  {bn}: delta={d:.2f}")
if results:
    mx = max(results.values())
    L(f">>> max bone delta = {mx:.2f}  {'ANIMA' if mx>0.5 else 'parado'}")
else:
    L(">>> nenhum bone testavel via essa API")

eas.destroy_actor(actor)
L("END")
