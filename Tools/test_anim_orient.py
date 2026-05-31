"""Teste conclusivo: SK_AliceFull SEM anim vs COM A_Standing_Idle.
Le Z do bone Head. Se SEM=alto(em pe) e COM=baixo(deitado) => ANIM Mixamo Y-up deita o mesh Z-up."""
import unreal
L=lambda s:unreal.log(f"[TO] {s}")

unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
body=unreal.load_asset("/Game/Alice/Characters/AliceFull/SK_AliceFull")
idle=unreal.load_asset("/Game/Alice/AnimAlice/A_Standing_Idle")

def headZ(comp, label):
    try:
        names=[str(comp.get_bone_name(i)) for i in range(comp.get_num_bones())]
        hb=next((n for n in names if "Head" in n), names[0] if names else None)
        loc=comp.get_bone_transform(hb).translation if hb else None
        # nao tem get_bone_transform por nome em alguns; tenta socket
        L(f"  [{label}] head bone={hb}")
        return None
    except Exception as e:
        L(f"  [{label}] err {e}")

# SEM anim
a1=eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0,0,0))
c1=a1.skeletal_mesh_component
c1.set_skeletal_mesh_asset(body)
o,e1=a1.get_actor_bounds(False)
L(f"SEM anim: bounds origin_z={o.z:.1f} ext=({e1.x:.0f},{e1.y:.0f},{e1.z:.0f})")

# COM anim
a2=eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(300,0,0))
c2=a2.skeletal_mesh_component
c2.set_skeletal_mesh_asset(body)
c2.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
c2.set_animation(idle)
c2.set_position(0.1, False)
o2,e2=a2.get_actor_bounds(False)
L(f"COM anim: bounds origin_z={o2.z:.1f} ext=({e2.x:.0f},{e2.y:.0f},{e2.z:.0f})")

# ext.z alto = em pe; ext.y alto = deitado
L(f">>> SEM: {'EM PE' if e1.z>e1.y else 'DEITADO'} | COM: {'EM PE' if e2.z>e2.y else 'DEITADO'}")
L("END")
