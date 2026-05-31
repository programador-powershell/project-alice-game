"""Spawn SK_AliceBody no L_Arena pra ver TAMANHO REAL visivel.
Cria 3 versoes lado a lado: scale 1, 100, 0.01 — voce ve qual e."""
import unreal
L = lambda s: unreal.log(f"[T] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
# limpa tests anteriores
for a in eas.get_all_level_actors():
    if a.get_actor_label().startswith("TestSize"): eas.destroy_actor(a)

body=unreal.load_asset("/Game/Alice/Characters/AliceBody/SK_AliceBody")
L(f"body asset = {body}")

# spawn 3 lados
for label, x, scale in [("TestSize_x1", 0, 1.0), ("TestSize_x100", 300, 100.0), ("TestSize_x0.01", -300, 0.01)]:
    actor=eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(x, 0, 200))
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(scale,scale,scale))
    comp=actor.skeletal_mesh_component
    comp.set_skeletal_mesh_asset(body)
    L(f"spawned {label} x={x} scale={scale}")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L("salvo. abra L_Arena no editor (viewport), procura os 3. ME DIZ qual tamanho parece humano.")
L("END")
