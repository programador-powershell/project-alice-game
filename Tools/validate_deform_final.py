"""Valida deformacao do SK_AliceVestido posando em 2 frames de A_Walk e
medindo bounding box (sem APIs de bone). Se box muda = pesos OK = anima."""
import unreal
L = lambda s: unreal.log(f"[VD] {s}")

unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
ANIM = unreal.load_asset("/Game/Alice/AnimM/A_Walk")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

sk = unreal.load_asset("/Game/Alice/Characters/AliceVestido/SK_AliceVestido")
actor = eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0,0,0))
comp = actor.skeletal_mesh_component
comp.set_skeletal_mesh_asset(sk)
comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
comp.set_animation(ANIM)

boxes = []
for t in (0.0, 0.35, 0.7, 1.0):
    comp.set_position(t, False)
    origin, ext = actor.get_actor_bounds(False)
    boxes.append((ext.x, ext.y, ext.z))
    L(f"  t={t:.2f} extent=({ext.x:.1f},{ext.y:.1f},{ext.z:.1f})")

dx = max(b[0] for b in boxes)-min(b[0] for b in boxes)
dy = max(b[1] for b in boxes)-min(b[1] for b in boxes)
dz = max(b[2] for b in boxes)-min(b[2] for b in boxes)
total = dx+dy+dz
L(f">>> variacao bounds = {total:.2f}")
L(f">>> {'DEFORMA (pesos OK, vai animar!)' if total>2.0 else 'ESTATUA (pesos quebrados)'}")
eas.destroy_actor(actor)
L("END")
