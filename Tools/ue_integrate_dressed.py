import unreal, os
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")

def imp_tex(png, name, kind):
    if not os.path.exists(png): print("MISS", png); return
    t=unreal.AssetImportTask(); t.set_editor_property("filename", png)
    t.set_editor_property("destination_path", "/Game/Alice/Textures/Alice"); t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
    AT.import_asset_tasks([t]); tex=unreal.load_asset("/Game/Alice/Textures/Alice/"+name)
    if tex and kind=="normal": tex.set_editor_property("srgb",False); tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP); EAL.save_asset("/Game/Alice/Textures/Alice/"+name)
    elif tex and kind=="linear": tex.set_editor_property("srgb",False); tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS); EAL.save_asset("/Game/Alice/Textures/Alice/"+name)
    print("TEX", name, tex is not None)

# dress textures REPLACE the nude T_Alice_* (so M_AliceDress rebuild uses the dress)
imp_tex(r"E:\References\3D\alice_vestido_tex\adress_base.png", "T_Alice_Base", "base")
imp_tex(r"E:\References\3D\alice_vestido_tex\adress_normal.png", "T_Alice_Normal", "normal")
imp_tex(r"E:\References\3D\alice_vestido_tex\adress_mr.png", "T_Alice_MR", "linear")

# dressed mesh -> SK_AliceReal (replace; BP_Alice already points here)
full = "/Game/Alice/Characters/AliceReal/SK_AliceReal"
if EAL.does_asset_exist(full): EAL.delete_asset(full)
t = unreal.AssetImportTask()
t.set_editor_property("filename", r"E:\References\3D\SK_AliceDress.fbx")
t.set_editor_property("destination_path", "/Game/Alice/Characters/AliceReal"); t.set_editor_property("destination_name", "SK_AliceReal")
t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
ui = unreal.FbxImportUI()
ui.set_editor_property("import_as_skeletal", True); ui.set_editor_property("import_mesh", True)
ui.set_editor_property("import_animations", False); ui.set_editor_property("import_materials", False); ui.set_editor_property("import_textures", False)
ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
if skel: ui.set_editor_property("skeleton", skel)
t.set_editor_property("options", ui)
AT.import_asset_tasks([t]); EAL.save_directory("/Game/Alice/Characters/AliceReal", False, True)
sk = unreal.load_asset(full)
print("SK_AliceReal(dressed)", sk.get_class().get_name() if sk else None, "h~", round(sk.get_bounds().box_extent.z*2,1) if sk and sk.get_class().get_name()=="SkeletalMesh" else "?")
print("INTEGRATE_DRESSED_DONE")
