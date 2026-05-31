"""Importa os 8 anims essenciais de E:\References\model\anims no SK_AliceOficial_Skeleton.
UE mapeia por nome de bone (anims=65, alice=49 subconjunto) -> funcionam.
Renomeia pros nomes que o AliceCharacter C++ espera (Anim_Idle/Walk/Run/Atk1-3/Dodge/Death).
"""
import unreal, os
L = lambda s: unreal.log(f"[AN] {s}")

SKEL = unreal.load_asset("/Game/Alice/Characters/AliceOficial/SK_AliceOficial_Skeleton")
if not SKEL:
    L("ABORT sem skeleton"); raise SystemExit
L(f"skeleton OK = {SKEL.get_name()}")

DST = "/Game/Alice/AnimAlice"
unreal.EditorAssetLibrary.make_directory(DST)

ANIM_DIR = r"E:\References\model\anims"
# (arquivo fonte, nome destino que o C++ usa)
clips = [
    ("Standing Idle.fbx",                    "Alice_Idle"),
    ("Walking.fbx",                          "Alice_Walk"),
    ("Fast Run.fbx",                         "Alice_Run"),
    ("Standing Melee Attack Horizontal.fbx", "Alice_Atk1"),
    ("Standing Melee Attack Backhand.fbx",   "Alice_Atk2"),
    ("Standing Melee Attack Downward.fbx",   "Alice_Atk3"),
    ("Sprinting Forward Roll.fbx",           "Alice_Dodge"),
    ("Standing React Death Forward.fbx",     "Alice_Death"),
]

tools = unreal.AssetToolsHelpers.get_asset_tools()
imported = {}
for src, dst in clips:
    p = os.path.join(ANIM_DIR, src)
    if not os.path.exists(p):
        L(f"  MISS {src}"); continue
    task = unreal.AssetImportTask()
    task.filename = p
    task.destination_path = DST
    task.destination_name = dst
    task.replace_existing = True
    task.automated = True
    task.save = True
    opt = unreal.FbxImportUI()
    opt.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
    opt.import_mesh = False
    opt.import_as_skeletal = True
    opt.import_animations = True
    opt.import_materials = False
    opt.import_textures = False
    opt.skeleton = SKEL
    opt.set_editor_property("automated_import_should_detect_type", False)
    task.options = opt
    tools.import_asset_tasks([task])
    ok = task.imported_object_paths
    imported[dst] = ok[0] if ok else None
    L(f"  {dst} <- {src}  {'OK' if ok else 'FALHOU'}")

L(f"TOTAL importados = {sum(1 for v in imported.values() if v)}/{len(clips)}")
L("DONE")
