"""Spawna um SkeletalMeshActor de teste no L_Arena com SK_AliceDressed e toca A_Walk em loop.
Se animar = SK ta bom (problema é runtime do AliceCharacter).
Se ficar parado = SK sem skin weights (precisa reimportar do FBX).
"""
import unreal
L = lambda s: unreal.log(f"[test] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
sk = unreal.load_asset("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
anim = unreal.load_asset("/Game/Alice/AnimM/A_Walk")
L(f"sk={'OK' if sk else 'MISS'}  A_Walk={'OK' if anim else 'MISS'}")

# remove test actor anterior se existir
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in eas.get_all_level_actors():
    if a.get_actor_label() == "TestAliceAnim":
        eas.destroy_actor(a); L("removido test actor anterior")

# spawn SkeletalMeshActor na frente do player spawn
loc = unreal.Vector(300, 0, 100)
rot = unreal.Rotator(0, 0, 0)
test_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
    unreal.SkeletalMeshActor, loc, rot)
test_actor.set_actor_label("TestAliceAnim")

comp = test_actor.skeletal_mesh_component
comp.set_skeletal_mesh_asset(sk)
comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
comp.set_animation(anim)
comp.play(True)  # loop
L(f"actor spawn em {loc} com mesh+anim+play(loop)")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L("save L_Arena")
L("--- AGORA DA PLAY E OLHA: a Alice de teste (em (300,0,100)) deveria estar andando in-place ---")
L("--- se animar = SK ok, problema runtime AliceCharacter ---")
L("--- se parar = SK sem skin weights (reimportar) ---")
L("END")
