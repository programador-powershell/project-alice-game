"""Importa TODOS anims da pasta com try/except por arquivo (nao para no erro).
Mesh SK_AliceFull ja importado. So anims + wire."""
import unreal, os
L=lambda s:unreal.log(f"[AS] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()

bskel=unreal.load_asset("/Game/Alice/Characters/AliceFull/SK_AliceFull_Skeleton")
if not bskel: L("ABORT sem skel"); raise SystemExit
DSTA="/Game/Alice/AnimAlice"
unreal.EditorAssetLibrary.make_directory(DSTA)
AD=r"E:\References\model\anims"

ok=[]; fail=[]
for f in sorted(os.listdir(AD)):
    if not f.lower().endswith(".fbx"): continue
    if f=="Eve_Skel.fbx": continue
    name="A_"+os.path.splitext(f)[0].replace(" ","_").replace(".","_").replace("-","_")
    full=f"{DSTA}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(full):
        ok.append(name); continue
    try:
        t=unreal.AssetImportTask(); t.filename=os.path.join(AD,f)
        t.destination_path=DSTA; t.destination_name=name
        t.replace_existing=True; t.automated=True; t.save=True
        o=unreal.FbxImportUI()
        o.mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION
        o.import_mesh=False; o.import_as_skeletal=True; o.import_animations=True
        o.import_materials=False; o.import_textures=False; o.skeleton=bskel
        t.options=o
        tools.import_asset_tasks([t])
        a=unreal.load_asset(full)
        if a and a.get_skeleton(): ok.append(name)
        else: fail.append(f)
    except Exception as e:
        fail.append(f"{f}:{type(e).__name__}")
L(f"OK={len(ok)} FAIL={len(fail)}")
for x in fail: L(f"  FAIL {x}")
L("END")
