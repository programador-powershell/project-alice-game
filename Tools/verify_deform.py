"""Verifica DEFORMACAO real (skin weights) sem precisar jogar:
poso o mesh em 2 tempos de A_Walk, comparo a bounding box do componente.
Se a box MUDAR = vertices seguem bones = pesos OK.
Se IGUAL = pesos quebrados (estatua).
Testa SK_AliceDressed (original) E SK_AliceDressed_v2.
Tambem lista materiais de cada um.
"""
import unreal
L = lambda s: unreal.log(f"[deform] {s}")

ANIM = unreal.load_asset("/Game/Alice/AnimM/A_Walk")
L(f"A_Walk = {'OK' if ANIM else 'MISS'}  len={ANIM.get_play_length() if ANIM else '?'}")

# mapa vazio temporario pra nao sujar L_Arena
unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

def test_mesh(path):
    sk = unreal.load_asset(path)
    if not sk:
        L(f"[{path}] MISS"); return
    L(f"=== {path.split('/')[-1]} ===")
    L(f"  skeleton = {sk.skeleton.get_path_name().split('.')[-1] if sk.skeleton else None}")
    # materiais
    try:
        mats = sk.materials
        for i,m in enumerate(mats):
            mi = m.material_interface if hasattr(m,'material_interface') else None
            L(f"  mat[{i}] = {mi.get_name() if mi else 'None'}")
    except Exception as e: L(f"  mat err: {e}")
    # spawn + pose
    actor = eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0,0,0))
    comp = actor.skeletal_mesh_component
    comp.set_skeletal_mesh_asset(sk)
    comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    comp.set_animation(ANIM)
    boxes = []
    for t in (0.0, 0.35, 0.7):
        comp.set_position(t, False)
        comp.tick_animation(0.0, False)
        comp.refresh_bone_transforms()
        b = comp.calc_bounds(comp.get_world_transform())
        ext = b.box_extent
        boxes.append((t, ext.x, ext.y, ext.z))
        L(f"  t={t:.2f}  extent=({ext.x:.1f},{ext.y:.1f},{ext.z:.1f})")
    # variacao
    dx = max(b[1] for b in boxes)-min(b[1] for b in boxes)
    dy = max(b[2] for b in boxes)-min(b[2] for b in boxes)
    dz = max(b[3] for b in boxes)-min(b[3] for b in boxes)
    moved = (dx+dy+dz)
    L(f"  >>> VARIACAO total bounds = {moved:.2f}  -> {'DEFORMA (pesos OK)' if moved>1.0 else 'ESTATUA (pesos QUEBRADOS)'}")
    eas.destroy_actor(actor)

test_mesh("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
test_mesh("/Game/Alice/Characters/AliceDressed_v2/SK_AliceDressed_v2")
L("END")
