"""Importa alice_vestido_FINAL.fbx no skel SK_AliceBody_Skeleton + wire BP."""
import unreal
L = lambda s: unreal.log(f"[F] {s}")

bskel=unreal.load_asset("/Game/Alice/Characters/AliceBody/SK_AliceBody_Skeleton")
L(f"bskel={'OK' if bskel else 'NULL'}")
if not bskel: raise SystemExit

# delete vestido velho
DSTD="/Game/Alice/Characters/AliceDress2"
for n in ["SK_AliceDress","SK_AliceDress_PhysicsAsset"]:
    p=f"{DSTD}/{n}"
    if unreal.EditorAssetLibrary.does_asset_exist(p): unreal.EditorAssetLibrary.delete_asset(p)
L("vestido velho deletado")

tools=unreal.AssetToolsHelpers.get_asset_tools()
td=unreal.AssetImportTask()
td.filename=r"E:\References\3D\alice_vestido_FINAL.fbx"
td.destination_path=DSTD; td.destination_name="SK_AliceDress"
td.replace_existing=True; td.automated=True; td.save=True
od=unreal.FbxImportUI()
od.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
od.import_mesh=True; od.import_as_skeletal=True; od.import_materials=True; od.import_textures=True
od.import_animations=False; od.create_physics_asset=False; od.skeleton=bskel
td.options=od
tools.import_asset_tasks([td])
dress=unreal.load_asset(f"{DSTD}/SK_AliceDress")
L(f"dress={'OK' if dress else 'NULL'} skel={dress.skeleton.get_name() if dress and dress.skeleton else 'NULL'}")
for i,m in enumerate(dress.materials):
    mi=m.material_interface
    L(f"  mat[{i}]={mi.get_name() if mi else None}")

# wire BP
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
cdo.set_editor_property("dress_mesh_asset", dress)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP wired+compiled")
L("END")
