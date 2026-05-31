"""Diagnostico unico e completo:
- Para cada mesh candidato: skeleton, materiais, e DEFORMACAO real (delta de bone hand_r entre 2 frames de A_Walk)
- Inventario de FBX/GLB no disco com data
"""
import unreal
L = lambda s: unreal.log(f"[D] {s}")

unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
ANIM = unreal.load_asset("/Game/Alice/AnimM/A_Walk")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

def probe(path):
    sk = unreal.load_asset(path)
    name = path.split('/')[-1]
    if not sk:
        L(f"{name}: MISS"); return
    skel = sk.skeleton.get_path_name().split('.')[-1] if sk.skeleton else "None"
    mats = []
    try:
        for m in sk.materials:
            mi = m.material_interface
            mats.append(mi.get_name() if mi else "None")
    except Exception as e: mats = [f"err:{e}"]
    # deformacao: bone hand_r em 2 tempos
    actor = eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0,0,0))
    comp = actor.skeletal_mesh_component
    comp.set_skeletal_mesh_asset(sk)
    comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    comp.set_animation(ANIM)
    locs = []
    bone_used = None
    for t in (0.0, 0.6):
        comp.set_position(t, False)
        comp.refresh_bone_transforms()
        for bn in ("hand_r","mixamorig:RightHand","RightHand","LeftHand","mixamorig:LeftHand"):
            try:
                loc = comp.get_socket_location(bn)
                if loc and (abs(loc.x)+abs(loc.y)+abs(loc.z))>0.01:
                    locs.append(loc); bone_used = bn; break
            except Exception: pass
    delta = (locs[0]-locs[1]).size() if len(locs)>=2 else -1
    verdict = "ANIMA" if delta>1.0 else ("PARADO/estatua" if delta>=0 else "bone N/A")
    eas.destroy_actor(actor)
    L(f"{name}:")
    L(f"   skeleton={skel}  mats={mats}")
    L(f"   bone={bone_used} delta={delta:.2f} -> {verdict}")

for p in ("/Game/Alice/Characters/Eve/SK_Eve",
          "/Game/Alice/Characters/EveM/SK_EveM",
          "/Game/Alice/Characters/AliceDressed/SK_AliceDressed",
          "/Game/Alice/Characters/AliceDressed_v2/SK_AliceDressed_v2"):
    probe(p)

L("END")
