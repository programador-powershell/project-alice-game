import unreal
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
MP = unreal.MaterialProperty
ST = unreal.MaterialSamplerType
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")

# ---- import Mixamo-rigged Lídia ----
t = unreal.AssetImportTask()
t.set_editor_property("filename", r"E:\References\3D\Lidia-T-Pose.fbx")
t.set_editor_property("destination_path", "/Game/Alice/Characters/LidiaReal")
t.set_editor_property("destination_name", "SK_LidiaReal")
t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
ui = unreal.FbxImportUI()
ui.set_editor_property("import_as_skeletal", True); ui.set_editor_property("import_mesh", True)
ui.set_editor_property("import_animations", False); ui.set_editor_property("import_materials", False); ui.set_editor_property("import_textures", False)
ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
if skel: ui.set_editor_property("skeleton", skel)
t.set_editor_property("options", ui)
AT.import_asset_tasks([t]); EAL.save_directory("/Game/Alice/Characters/LidiaReal", False, True)
sk = unreal.load_asset("/Game/Alice/Characters/LidiaReal/SK_LidiaReal")
print("SK_LidiaReal", sk is not None, "height~", round(sk.get_bounds().box_extent.z*2,1) if sk else 0)

# ---- M_LidiaReal (straight PBR) ----
MATDIR="/Game/Alice/Materials"; PATH=MATDIR+"/M_LidiaReal"
base=unreal.load_asset("/Game/Alice/Textures/Lidia/T_Lidia_Base")
norm=unreal.load_asset("/Game/Alice/Textures/Lidia/T_Lidia_Normal")
met=unreal.load_asset("/Game/Alice/Textures/Lidia/T_Lidia_Metallic")
rough=unreal.load_asset("/Game/Alice/Textures/Lidia/T_Lidia_Roughness")
if EAL.does_asset_exist(PATH): EAL.delete_asset(PATH)
mat=AT.create_asset("M_LidiaReal", MATDIR, unreal.Material, unreal.MaterialFactoryNew())
def tex(t,stype,x,y):
    n=MEL.create_material_expression(mat, unreal.MaterialExpressionTextureSample, x, y)
    if t: n.set_editor_property("texture", t)
    n.set_editor_property("sampler_type", stype); return n
tb=tex(base, ST.SAMPLERTYPE_COLOR, -500,-200); MEL.connect_material_property(tb,"RGB",MP.MP_BASE_COLOR)
tn=tex(norm, ST.SAMPLERTYPE_NORMAL, -500,100); MEL.connect_material_property(tn,"RGB",MP.MP_NORMAL)
tm=tex(met, ST.SAMPLERTYPE_MASKS, -500,360); MEL.connect_material_property(tm,"R",MP.MP_METALLIC)
tr=tex(rough, ST.SAMPLERTYPE_MASKS, -500,620); MEL.connect_material_property(tr,"R",MP.MP_ROUGHNESS)
MEL.recompile_material(mat); EAL.save_asset(PATH)
M=unreal.load_asset(PATH)
if sk and M:
    mats=sk.get_editor_property("materials")
    for sm in mats: sm.set_editor_property("material_interface", M)
    sk.set_editor_property("materials", mats); EAL.save_asset("/Game/Alice/Characters/LidiaReal/SK_LidiaReal")
    print("applied M_LidiaReal to", len(mats), "slots")
print("LIDIA_REAL_DONE")
