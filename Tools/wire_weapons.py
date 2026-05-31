"""Populate BP_Alice's WeaponComponent loadout with faithful weapon meshes per dress,
attached to the Mixamo right-hand bone. Index matches EDressType (0 None ... 5 Rainha)."""
import unreal
EAL = unreal.EditorAssetLibrary
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")

# index by EDressType: 0 None, 1 Coelho, 2 Cheshire, 3 Chapeleiro, 4 Lagarta, 5 Rainha
MESHES = [
    None,
    "SM_weapon_relogio_coelho_branco",
    "SM_weapon_sorriso_cheshire",
    "SM_weapon_bengala_cha_eterno",
    "SM_weapon_foice_lagarta_azul",
    "SM_weapon_guillotine_heartbreaker",
]


def cmesh(name):
    if not name:
        return None
    return unreal.load_asset("/Game/Alice/Characters/%s/StaticMeshes/%s" % (name, name))


if bp:
    cdo = unreal.get_default_object(bp.generated_class())
    weap = cdo.get_editor_property("weapon")
    loadout = []
    for i, mname in enumerate(MESHES):
        d = unreal.WeaponDef()
        d.set_editor_property("id", unreal.Name("W%d" % i))
        m = cmesh(mname)
        if m:
            d.set_editor_property("mesh", m)
        d.set_editor_property("attach_socket", unreal.Name("mixamorig:RightHand"))
        try:
            bh = unreal.HitData()
            bh.set_editor_property("damage", 85.0)
            bh.set_editor_property("posture_damage", 35.0)
            d.set_editor_property("base_hit", bh)
        except Exception as e:
            print("WIREW hit", e)
        loadout.append(d)
        print("WIREW slot %d mesh=%s" % (i, mname))
    try:
        weap.set_editor_property("loadout", loadout)
    except Exception as e:
        print("WIREW loadout set FAIL", e)
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    except Exception as e:
        print("WIREW save", e)
print("WIREW DONE")
