"""Import the rigged Alice (SK_Alice.fbx) onto SK_EveM_Skeleton, swap the player to her,
auto-scale to ~175cm. Reuses all existing AnimM clips (same skeleton)."""
import os
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
FBX = r"E:\model\SK_Alice.fbx"
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")

if not os.path.exists(FBX):
    print("ALICEIMP missing SK_Alice.fbx"); raise SystemExit

if EAL.does_directory_exist("/Game/Alice/Characters/AliceRig"):
    EAL.delete_directory("/Game/Alice/Characters/AliceRig")

t = unreal.AssetImportTask()
t.set_editor_property("filename", FBX)
t.set_editor_property("destination_path", "/Game/Alice/Characters/AliceRig")
t.set_editor_property("destination_name", "SK_Alice")
t.set_editor_property("automated", True)
t.set_editor_property("replace_existing", True)
t.set_editor_property("save", True)
ui = unreal.FbxImportUI()
ui.set_editor_property("import_as_skeletal", True)
ui.set_editor_property("import_mesh", True)
ui.set_editor_property("import_materials", True)
ui.set_editor_property("import_textures", True)
ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
if skel:
    ui.set_editor_property("skeleton", skel)  # reuse Eve skeleton -> clips work
t.set_editor_property("options", ui)
AT.import_asset_tasks([t])
EAL.save_directory("/Game/Alice/Characters/AliceRig", False, True)

sk = unreal.load_asset("/Game/Alice/Characters/AliceRig/SK_Alice")
print("ALICEIMP SK_Alice=%s" % (sk is not None))
if not sk:
    print("ALICEIMP FAILED"); raise SystemExit

# auto-scale to ~175 cm
scale = 1.0
try:
    b = sk.get_bounds()
    h = b.box_extent.z * 2.0
    if h > 1.0:
        scale = 175.0 / h
except Exception as e:
    print("ALICEIMP bounds", e)

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
if bp:
    cdo = unreal.get_default_object(bp.generated_class())
    try:
        mc = cdo.get_editor_property("mesh")
        mc.set_skeletal_mesh_asset(sk)
        mc.set_relative_scale3d(unreal.Vector(scale, scale, scale))
        cdo.set_editor_property("visual_mesh_asset", None)
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
        print("ALICEIMP player=Alice scale=%.3f" % scale)
    except Exception as e:
        print("ALICEIMP wire", e)
print("ALICEIMP DONE")
