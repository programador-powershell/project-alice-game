import unreal, os
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
MP = unreal.MaterialProperty
ST = unreal.MaterialSamplerType
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")

def imp_mesh(fbx, dest, name):
    full = dest + "/" + name
    if EAL.does_asset_exist(full):
        EAL.delete_asset(full)
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", fbx); t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name); t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_as_skeletal", True); ui.set_editor_property("import_mesh", True)
    ui.set_editor_property("import_animations", False); ui.set_editor_property("import_materials", False); ui.set_editor_property("import_textures", False)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    if skel: ui.set_editor_property("skeleton", skel)
    t.set_editor_property("options", ui)
    AT.import_asset_tasks([t]); EAL.save_directory(dest, False, True)
    sk = unreal.load_asset(full)
    cls = sk.get_class().get_name() if sk else None
    print("  ", name, cls, ("h~"+str(round(sk.get_bounds().box_extent.z*2,1))) if cls=="SkeletalMesh" else "")
    return sk if cls == "SkeletalMesh" else None

def apply_mat(sk, M):
    if sk and M:
        mats = sk.get_editor_property("materials")
        for sm in mats: sm.set_editor_property("material_interface", M)
        sk.set_editor_property("materials", mats)
        EAL.save_asset(sk.get_path_name().split('.')[0])

def imp_tex(png, dest, name, kind):
    if not os.path.exists(png): return None
    t=unreal.AssetImportTask(); t.set_editor_property("filename", png); t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name); t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
    AT.import_asset_tasks([t]); tex=unreal.load_asset(dest+"/"+name)
    if tex and kind=="normal": tex.set_editor_property("srgb",False); tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP); EAL.save_asset(dest+"/"+name)
    elif tex and kind=="linear": tex.set_editor_property("srgb",False); tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS); EAL.save_asset(dest+"/"+name)
    return tex

def build_pbr(path, base, norm, mr):
    if EAL.does_asset_exist(path): EAL.delete_asset(path)
    d="/".join(path.split("/")[:-1]); n=path.split("/")[-1]
    mat=AT.create_asset(n, d, unreal.Material, unreal.MaterialFactoryNew())
    def tx(tt,stype,x,y):
        e=MEL.create_material_expression(mat, unreal.MaterialExpressionTextureSample, x, y)
        if tt: e.set_editor_property("texture", tt)
        e.set_editor_property("sampler_type", stype); return e
    if base: MEL.connect_material_property(tx(base,ST.SAMPLERTYPE_COLOR,-500,-200),"RGB",MP.MP_BASE_COLOR)
    if norm: MEL.connect_material_property(tx(norm,ST.SAMPLERTYPE_NORMAL,-500,100),"RGB",MP.MP_NORMAL)
    if mr:
        m=tx(mr,ST.SAMPLERTYPE_MASKS,-500,360); MEL.connect_material_property(m,"B",MP.MP_METALLIC); MEL.connect_material_property(m,"G",MP.MP_ROUGHNESS)
    MEL.recompile_material(mat); EAL.save_asset(path); return unreal.load_asset(path)

print("LIDIA:");   l = imp_mesh(r"E:\References\3D\Lidia-T-Pose.fbx",   "/Game/Alice/Characters/LidiaReal",   "SK_LidiaReal");   apply_mat(l, unreal.load_asset("/Game/Alice/Materials/M_LidiaReal"))
print("COELHO:");  c = imp_mesh(r"E:\References\3D\Coelho-T-Pose.fbx",  "/Game/Alice/Characters/CoelhoReal",  "SK_CoelhoReal");  apply_mat(c, unreal.load_asset("/Game/Alice/Materials/M_CoelhoReal"))
print("CAVALEIRO:")
cb=imp_tex(r"E:\References\3D\cavaleiro_tex\cav_base.png","/Game/Alice/Textures/Cavaleiro","T_Cav_Base","base")
cn=imp_tex(r"E:\References\3D\cavaleiro_tex\cav_normal.png","/Game/Alice/Textures/Cavaleiro","T_Cav_Normal","normal")
cm=imp_tex(r"E:\References\3D\cavaleiro_tex\cav_mr.png","/Game/Alice/Textures/Cavaleiro","T_Cav_MR","linear")
cvm=build_pbr("/Game/Alice/Materials/M_CavaleiroReal", cb, cn, cm)
cv=imp_mesh(r"E:\References\3D\cavaleiro-T-Pose.fbx","/Game/Alice/Characters/CavaleiroReal","SK_CavaleiroReal"); apply_mat(cv, cvm)
print("BATCH_CHARS_DONE")
