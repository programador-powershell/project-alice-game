"""Import rock/tree packs (legacy FBX -> materials from TGAs) and scatter for detail."""
import os
import math
import random
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

ROCK_DIR = "/Game/Alice/Env/Rocks"
TREE_DIR = "/Game/Alice/Env/Trees"


def load(p):
    return EAL.load_asset(p) if EAL.does_asset_exist(p) else None


def imp_static(fp, dest, name):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", fp)
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", True)
    ui.set_editor_property("import_as_skeletal", False)
    ui.set_editor_property("import_materials", True)
    ui.set_editor_property("import_textures", True)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
    t.set_editor_property("options", ui)
    return t


def main():
    tasks = []
    for i in range(1, 8):
        fp = r"E:\arquivos\extracted\rocks\Rock_%02d\Meshes\SM_Rock_%02d.fbx" % (i, i)
        if os.path.exists(fp):
            tasks.append(imp_static(fp, ROCK_DIR, "SM_Rock_%02d" % i))
    tree_fp = r"E:\arquivos\extracted\tree_hp\HighPoly Tree Model\Model\SM_HP_Tree.FBX"
    if os.path.exists(tree_fp):
        tasks.append(imp_static(tree_fp, TREE_DIR, "SM_HP_Tree"))
    if tasks:
        AT.import_asset_tasks(tasks)
        EAL.save_directory("/Game/Alice/Env", False, True)

    rocks = [load(ROCK_DIR + "/SM_Rock_%02d" % i) for i in range(1, 8)]
    rocks = [r for r in rocks if r]
    tree = load(TREE_DIR + "/SM_HP_Tree")
    unreal.log("[Alice] rocks=%d tree=%s" % (len(rocks), tree is not None))
    if not rocks:
        unreal.log_warning("[Alice] no rocks imported; abort scatter")
        return

    random.seed(7)

    def scatter(mapname, nrocks, ntrees, rmin, rmax):
        path = "/Game/Alice/Maps/" + mapname
        if not EAL.does_asset_exist(path):
            return
        LES.load_level(path)
        for i in range(nrocks):
            ang = random.uniform(0, 2 * math.pi)
            rad = random.uniform(rmin, rmax)
            loc = unreal.Vector(rad * math.cos(ang), rad * math.sin(ang), -20.0)
            a = EAS.spawn_actor_from_class(unreal.StaticMeshActor, loc, unreal.Rotator(roll=0, pitch=0, yaw=random.uniform(0, 360)))
            if not a:
                continue
            a.set_actor_label("Rock_%d" % i)
            s = random.uniform(1.8, 4.2)
            a.set_actor_scale3d(unreal.Vector(s, s, s * random.uniform(0.8, 1.2)))
            a.static_mesh_component.set_static_mesh(random.choice(rocks))
            a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
        if tree and ntrees > 0:
            for i in range(ntrees):
                ang = random.uniform(0, 2 * math.pi)
                rad = random.uniform(rmin * 0.8, rmax)
                loc = unreal.Vector(rad * math.cos(ang), rad * math.sin(ang), -20.0)
                a = EAS.spawn_actor_from_class(unreal.StaticMeshActor, loc, unreal.Rotator(roll=0, pitch=0, yaw=random.uniform(0, 360)))
                if not a:
                    continue
                a.set_actor_label("Tree_%d" % i)
                s = random.uniform(0.8, 1.6)
                a.set_actor_scale3d(unreal.Vector(s, s, s))
                a.static_mesh_component.set_static_mesh(tree)
                a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
        LES.save_current_level()
        unreal.log("[Alice] scattered %s (%dR %dT)" % (mapname, nrocks, ntrees))

    cfg = {
        "L_Arena": (18, 0), "L_FlorestaCheshire": (14, 12), "L_Ruinas": (22, 4),
        "L_Vortice": (10, 0), "L_TocaMecanica": (14, 0), "L_PatioReal": (12, 0),
        "L_NevoaCogumelos": (14, 4), "L_SalaoCha": (8, 0), "L_CampoEtereo": (10, 0),
        "L_MargemDoRio": (16, 10),
    }
    for mapname, (nr, nt) in cfg.items():
        scatter(mapname, nr, nt, 1900.0, 2650.0)

    EAL.save_directory("/Game/Alice", False, True)
    unreal.log("[Alice] SCATTER DONE")


main()
