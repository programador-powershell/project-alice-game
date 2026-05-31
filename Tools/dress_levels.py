"""
Environment art (lite): create per-biome PBR materials + emissive accents and assign
them across every map by actor label. Turns gray blockouts into themed scenes.
"""
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

MAT_DIR = "/Game/Alice/Materials"


def make_mat(name, color, rough=0.75, metallic=0.0, emissive=None):
    path = MAT_DIR + "/" + name
    if EAL.does_asset_exist(path):
        return unreal.load_asset(path)
    m = AT.create_asset(name, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())
    try:
        base = MEL.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -480, 0)
        base.set_editor_property("constant", unreal.LinearColor(color[0], color[1], color[2], 1.0))
        MEL.connect_material_property(base, "", unreal.MaterialProperty.MP_BASE_COLOR)

        rg = MEL.create_material_expression(m, unreal.MaterialExpressionConstant, -480, 200)
        rg.set_editor_property("r", rough)
        MEL.connect_material_property(rg, "", unreal.MaterialProperty.MP_ROUGHNESS)

        if metallic > 0.0:
            mt = MEL.create_material_expression(m, unreal.MaterialExpressionConstant, -480, 320)
            mt.set_editor_property("r", metallic)
            MEL.connect_material_property(mt, "", unreal.MaterialProperty.MP_METALLIC)

        if emissive:
            em = MEL.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -480, 440)
            em.set_editor_property("constant", unreal.LinearColor(emissive[0], emissive[1], emissive[2], 1.0))
            MEL.connect_material_property(em, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)

        MEL.recompile_material(m)
        EAL.save_asset(path)
    except Exception as e:
        unreal.log_warning("mat %s: %s" % (name, e))
    return m


def main():
    if not EAL.does_directory_exist(MAT_DIR):
        EAL.make_directory(MAT_DIR)

    M = {
        "stone":   make_mat("M_Stone",        (0.17, 0.17, 0.20), 0.82),
        "warm":    make_mat("M_StoneWarm",    (0.24, 0.19, 0.14), 0.82),
        "purple":  make_mat("M_PurpleStone",  (0.16, 0.10, 0.22), 0.72),
        "forest":  make_mat("M_ForestPurple", (0.13, 0.08, 0.19), 0.80),
        "green":   make_mat("M_HatterGreen",  (0.10, 0.20, 0.12), 0.72),
        "mush":    make_mat("M_MushBlue",     (0.10, 0.16, 0.34), 0.72),
        "crimson": make_mat("M_Crimson",      (0.28, 0.06, 0.08), 0.62),
        "sand":    make_mat("M_Sand",         (0.30, 0.26, 0.18), 0.85),
        "cream":   make_mat("M_EtherCream",   (0.48, 0.45, 0.38), 0.60),
        "clock":   make_mat("M_ClockMetal",   (0.12, 0.16, 0.26), 0.40, 0.7),
        # emissive accents
        "g_blue":    make_mat("M_GlowBlue",    (0.02, 0.06, 0.12), 0.5, 0.0, (0.2, 0.45, 1.0)),
        "g_magenta": make_mat("M_GlowMagenta", (0.10, 0.02, 0.12), 0.5, 0.0, (0.7, 0.1, 0.9)),
        "g_gold":    make_mat("M_GlowGold",    (0.10, 0.07, 0.02), 0.5, 0.0, (1.0, 0.7, 0.2)),
        "g_teal":    make_mat("M_GlowTeal",    (0.02, 0.10, 0.10), 0.5, 0.0, (0.2, 0.85, 0.8)),
        "g_red":     make_mat("M_GlowRed",     (0.12, 0.01, 0.01), 0.5, 0.0, (1.0, 0.15, 0.1)),
        "g_green":   make_mat("M_GlowGreen",   (0.02, 0.12, 0.04), 0.5, 0.0, (0.2, 0.9, 0.3)),
    }

    # map -> (floor, wall, accent)
    cfg = {
        "L_MargemDoRio":     ("sand", "warm", "g_gold"),
        "L_Vortice":         ("purple", "purple", "g_magenta"),
        "L_InteriorDeCha":   ("warm", "stone", "g_gold"),
        "L_TocaMecanica":    ("stone", "stone", "g_blue"),
        "L_Arena":           ("stone", "stone", "g_blue"),
        "L_FlorestaCheshire":("forest", "forest", "g_teal"),
        "L_SalaoCha":        ("stone", "green", "g_green"),
        "L_NevoaCogumelos":  ("mush", "mush", "g_blue"),
        "L_PatioReal":       ("stone", "crimson", "g_red"),
        "L_Ruinas":          ("sand", "sand", "g_red"),
        "L_CampoEtereo":     ("cream", "cream", "g_gold"),
    }

    FLOOR = ("Floor", "Dais", "Bottom", "Ring")
    ACCENT = ("Gear", "Beacon", "Arch", "Compass", "Medallion", "Crystal")

    for mapname, (fk, wk, ak) in cfg.items():
        path = "/Game/Alice/Maps/" + mapname
        if not EAL.does_asset_exist(path):
            continue
        LES.load_level(path)
        fmat, wmat, amat = M[fk], M[wk], M[ak]
        n = 0
        for a in EAS.get_all_level_actors():
            if not isinstance(a, unreal.StaticMeshActor):
                continue
            lbl = a.get_actor_label()
            mat = wmat
            if any(k in lbl for k in FLOOR):
                mat = fmat
            elif any(k in lbl for k in ACCENT):
                mat = amat
            mc = a.static_mesh_component
            slots = max(1, mc.get_num_materials())
            for i in range(slots):
                mc.set_material(i, mat)
            n += 1
        LES.save_current_level()
        unreal.log("[Alice] dressed %s (%d meshes)" % (mapname, n))

    EAL.save_directory("/Game/Alice", False, True)
    unreal.log("[Alice] DRESS DONE")


main()
