"""So importa corpo alice_RIGGED -> SK_AliceBody. Confirma skeleton."""
import unreal
L = lambda s: unreal.log(f"[B] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()
DSTB="/Game/Alice/Characters/AliceBody"
unreal.EditorAssetLibrary.make_directory(DSTB)
tb=unreal.AssetImportTask(); tb.filename=r"E:\References\3D\alice_RIGGED.fbx"
tb.destination_path=DSTB; tb.destination_name="SK_AliceBody"
tb.replace_existing=True; tb.automated=True; tb.save=True
ob=unreal.FbxImportUI()
ob.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
ob.import_mesh=True; ob.import_as_skeletal=True; ob.import_materials=True; ob.import_textures=True
ob.import_animations=False; ob.create_physics_asset=True
tb.options=ob
res=tools.import_asset_tasks([tb])
L(f"imported_paths={tb.imported_object_paths}")
# lista direto pelo path
for n in ["SK_AliceBody","SK_AliceBody_Skeleton","SK_AliceBody_PhysicsAsset"]:
    full=f"{DSTB}/{n}"
    ex=unreal.EditorAssetLibrary.does_asset_exist(full)
    L(f"  {n} exists={ex}")
sk=unreal.load_asset(f"{DSTB}/SK_AliceBody")
L(f"SK_AliceBody skel={sk.skeleton.get_name() if sk and sk.skeleton else 'NULL'}")
for i,m in enumerate(sk.materials):
    mi=m.material_interface
    L(f"  mat[{i}]={mi.get_name() if mi else None}")
L("END")
