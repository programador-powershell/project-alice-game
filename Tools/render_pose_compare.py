"""Renderiza cada mesh candidato POSADO em A_Walk (frame 0.6) -> PNG.
Olho-no-olho: se a pose nao for T-pose = anima. Tambem mostra se tem cor.
Usa thumbnail rendering que respeita o pose atual do componente.
"""
import unreal, os
L = lambda s: unreal.log(f"[R] {s}")
OUT = r"E:\Alice\_PREVIEWS"
os.makedirs(OUT, exist_ok=True)

ANIM = unreal.load_asset("/Game/Alice/AnimM/A_Walk")

# cena limpa com luz
unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,400), unreal.Rotator(-45,45,0))
unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,300))

candidates = [
    ("/Game/Alice/Characters/AliceDressed/SK_AliceDressed", "ad_orig"),
    ("/Game/Alice/Characters/AliceDressed_v2/SK_AliceDressed_v2", "ad_v2"),
]

# spawn todos lado a lado, posados
x = -200
for path, tag in candidates:
    sk = unreal.load_asset(path)
    if not sk:
        L(f"{tag}: MISS"); continue
    a = eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(x,0,0), unreal.Rotator(0,0,0))
    a.set_actor_label(tag)
    c = a.skeletal_mesh_component
    c.set_skeletal_mesh_asset(sk)
    c.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    c.set_animation(ANIM)
    c.set_position(0.6, False)  # poso no meio do passo
    mats = [ (m.material_interface.get_name() if m.material_interface else "None") for m in sk.materials ]
    L(f"{tag} @x={x}: mats={mats}")
    x += 200

# posiciona viewport e tira screenshot
unreal.EditorLevelLibrary.editor_set_camera_look_at_location(unreal.Vector(0,0,90))
L("posed. screenshot via console HighResShot")
# screenshot do viewport ativo
try:
    unreal.SystemLibrary.execute_console_command(None, "HighResShot 1000x1100 filename=" + os.path.join(OUT,"pose_compare.png"))
    L("HighResShot disparado -> _PREVIEWS/pose_compare.png")
except Exception as e:
    L(f"shot err: {e}")
L("END")
