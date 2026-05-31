"""Prova visual: spawna SK_AliceOficial, update_in_editor ON, poe Walk frame 0.6,
enquadra camera, screenshot. Se na imagem a perna estiver a frente = PESOS OK.
"""
import unreal
L = lambda s: unreal.log(f"[RPP] {s}")

OUT = r"E:\Alice\_PREVIEWS\alice_walk_proof.png"
unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,300), unreal.Rotator(-40,35,0))
unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,200))

sk = unreal.load_asset("/Game/Alice/Characters/AliceOficial/SK_AliceOficial")
walk = unreal.load_asset("/Game/Alice/AnimAlice/Alice_Walk")
actor = eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
comp = actor.skeletal_mesh_component
comp.set_skeletal_mesh_asset(sk)
comp.set_editor_property("update_animation_in_editor", True)
comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
comp.set_animation(walk)
comp.set_position(0.55, True)
L(f"walk len={walk.get_play_length() if walk else '?'} posed @0.55")

# camera lateral (perfil mostra perna a frente melhor)
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(280,0,95), unreal.Rotator(-5,180,0))
unreal.AutomationLibrary.take_high_res_screenshot(800, 1000, OUT)
L(f"shot -> {OUT}")
L("END")
