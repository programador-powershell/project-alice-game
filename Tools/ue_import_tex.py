import unreal
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary

def imp_tex(png, dest, name, kind):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", png)
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    AT.import_asset_tasks([t])
    tex = unreal.load_asset(dest + "/" + name)
    if tex:
        if kind == "normal":
            tex.set_editor_property("srgb", False)
            tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        elif kind == "linear":
            tex.set_editor_property("srgb", False)
            tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
        EAL.save_asset(dest + "/" + name)
    print("TEX", name, tex is not None)
    return tex

A = r"E:\References\3D\alice_tex"
imp_tex(A + r"\texture_pbr_20250901.png", "/Game/Alice/Textures/Alice", "T_Alice_Base", "base")
imp_tex(A + r"\texture_pbr_20250901_normal.png", "/Game/Alice/Textures/Alice", "T_Alice_Normal", "normal")
imp_tex(A + r"\texture_pbr_20250901_metallic_texture_pbr_20250901_roughness.png", "/Game/Alice/Textures/Alice", "T_Alice_MR", "linear")

L = r"E:\References\3D\lidia_tex"
imp_tex(L + r"\texture_pbr_20250901.png", "/Game/Alice/Textures/Lidia", "T_Lidia_Base", "base")
imp_tex(L + r"\texture_pbr_20250901_normal.png", "/Game/Alice/Textures/Lidia", "T_Lidia_Normal", "normal")
imp_tex(L + r"\texture_pbr_20250901_metallic.png", "/Game/Alice/Textures/Lidia", "T_Lidia_Metallic", "linear")
imp_tex(L + r"\texture_pbr_20250901_roughness.png", "/Game/Alice/Textures/Lidia", "T_Lidia_Roughness", "linear")
print("IMPORT_TEX_DONE")
