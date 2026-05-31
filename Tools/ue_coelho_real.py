import unreal, os
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
MP = unreal.MaterialProperty
ST = unreal.MaterialSamplerType
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")

def imp_tex(png, name, kind):
    if not os.path.exists(png):
        print("MISSING", png); return None
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", png); t.set_editor_property("destination_path", "/Game/Alice/Textures/Coelho")
    t.set_editor_property("destination_name", name); t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
    AT.import_asset_tasks([t])
    tex = unreal.load_asset("/Game/Alice/Textures/Coelho/" + name)
    if tex and kind == "normal":
        tex.set_editor_property("srgb", False); tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP); EAL.save_asset("/Game/Alice/Textures/Coelho/"+name)
    elif tex and kind == "linear":
        tex.set_editor_property("srgb", False); tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS); EAL.save_asset("/Game/Alice/Textures/Coelho/"+name)
    return tex

base = imp_tex(r"E:\References\3D\coelho_tex\coelho_base.png", "T_Coelho_Base", "base")
norm = imp_tex(r"E:\References\3D\coelho_tex\coelho_normal.png", "T_Coelho_Normal", "normal")
mr   = imp_tex(r"E:\References\3D\coelho_tex\coelho_mr.png", "T_Coelho_MR", "linear")

# import rigged mesh
t = unreal.AssetImportTask()
t.set_editor_property("filename", r"E:\References\3D\coelho-t-pose.fbx")
t.set_editor_property("destination_path", "/Game/Alice/Characters/CoelhoReal")
t.set_editor_property("destination_name", "SK_CoelhoReal")
t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
ui = unreal.FbxImportUI()
ui.set_editor_property("import_as_skeletal", True); ui.set_editor_property("import_mesh", True)
ui.set_editor_property("import_animations", False); ui.set_editor_property("import_materials", False); ui.set_editor_property("import_textures", False)
ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
if skel: ui.set_editor_property("skeleton", skel)
t.set_editor_property("options", ui)
AT.import_asset_tasks([t]); EAL.save_directory("/Game/Alice/Characters/CoelhoReal", False, True)
sk = unreal.load_asset("/Game/Alice/Characters/CoelhoReal/SK_CoelhoReal")
print("SK_CoelhoReal", sk is not None, "h~", round(sk.get_bounds().box_extent.z*2,1) if sk else 0)

# material
MATDIR="/Game/Alice/Materials"; PATH=MATDIR+"/M_CoelhoReal"
if EAL.does_asset_exist(PATH): EAL.delete_asset(PATH)
mat=AT.create_asset("M_CoelhoReal", MATDIR, unreal.Material, unreal.MaterialFactoryNew())
def tx(t,stype,x,y):
    n=MEL.create_material_expression(mat, unreal.MaterialExpressionTextureSample, x, y)
    if t: n.set_editor_property("texture", t)
    n.set_editor_property("sampler_type", stype); return n
if base: MEL.connect_material_property(tx(base, ST.SAMPLERTYPE_COLOR, -500,-200), "RGB", MP.MP_BASE_COLOR)
if norm: MEL.connect_material_property(tx(norm, ST.SAMPLERTYPE_NORMAL, -500,100), "RGB", MP.MP_NORMAL)
if mr:
    m=tx(mr, ST.SAMPLERTYPE_MASKS, -500,360); MEL.connect_material_property(m,"B",MP.MP_METALLIC); MEL.connect_material_property(m,"G",MP.MP_ROUGHNESS)
MEL.recompile_material(mat); EAL.save_asset(PATH)
M=unreal.load_asset(PATH)
if sk and M:
    mats=sk.get_editor_property("materials")
    for sm in mats: sm.set_editor_property("material_interface", M)
    sk.set_editor_property("materials", mats); EAL.save_asset("/Game/Alice/Characters/CoelhoReal/SK_CoelhoReal")
    print("applied M_CoelhoReal", len(mats))
print("COELHO_REAL_DONE")
