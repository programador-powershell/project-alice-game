"""
Build the 5 remaining boss arenas in one editor run, following L_Arena's pattern,
parametrized per area theme. Each: basic-shape arena (real boundary walls), themed
Lumen lighting + fog, Mesa de Chá checkpoint, the correct boss + 2 mobs, PlayerStart,
and BP_AliceGameMode so it's playable standalone.

  UnrealEditor-Cmd.exe E:\Alice\Alice.uproject -ExecutePythonScript=E:\Alice\Tools\build_arenas.py
"""
import math
import unreal

EAL = unreal.EditorAssetLibrary
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

MAP_DIR = "/Game/Alice/Maps"


def load(path):
    try:
        return EAL.load_asset(path) if EAL.does_asset_exist(path) else None
    except Exception:
        return None


def char_mesh(name):
    return load("/Game/Alice/Characters/%s/StaticMeshes/%s" % (name, name)) if name else None


def mesh_height(mesh):
    try:
        return max(1.0, mesh.get_bounds().box_extent.z * 2.0)
    except Exception:
        return 0.0


def v(x, y, z):
    return unreal.Vector(x, y, z)


def r(yaw):
    return unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw)


def lin(t):
    return unreal.LinearColor(t[0], t[1], t[2])


def spawn_sm(mesh, loc, rot, scale, label):
    a = EAS.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
    if not a:
        return None
    a.set_actor_label(label)
    a.set_actor_scale3d(scale)
    if mesh:
        a.static_mesh_component.set_static_mesh(mesh)
    a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    return a


def set_char(actor, mesh, factor):
    try:
        if mesh:
            actor.set_editor_property("visual_mesh_asset", mesh)
        actor.set_editor_property("visual_mesh_scale", factor)
    except Exception as e:
        unreal.log_warning("set_char: %s" % e)


def build(cfg, cube, cyl, factor, gm_class):
    LES.new_level(MAP_DIR + "/" + cfg["map"])

    spawn_sm(cyl, v(0, 0, -15), r(0), unreal.Vector(54, 54, 0.3), "Floor")
    spawn_sm(cyl, v(0, 900, 5), r(0), unreal.Vector(14, 14, 0.15), "BossDais")
    nseg = 28
    for i in range(nseg):
        ang = math.radians(360.0 / nseg * i)
        spawn_sm(cube, v(2800 * math.cos(ang), 2800 * math.sin(ang), 420),
                 r(360.0 / nseg * i), unreal.Vector(3.2, 7.5, 9.5), "Wall_%d" % i)
    for i in range(8):
        ang = math.radians(45 * i)
        spawn_sm(cube, v(1750 * math.cos(ang), 1750 * math.sin(ang), 250),
                 r(45 * i), unreal.Vector(1.4, 1.4, 6.0), "Pillar_%d" % i)

    sun = EAS.spawn_actor_from_class(unreal.DirectionalLight, v(0, 0, 1500), unreal.Rotator(roll=0, pitch=-44, yaw=40))
    if sun:
        c = sun.get_component_by_class(unreal.DirectionalLightComponent)
        c.set_intensity(2.2)
        c.set_light_color(lin(cfg["sun"]))
    sky = EAS.spawn_actor_from_class(unreal.SkyLight, v(0, 0, 900))
    if sky:
        sky.get_component_by_class(unreal.SkyLightComponent).set_intensity(cfg["sky"])
    EAS.spawn_actor_from_class(unreal.SkyAtmosphere, v(0, 0, 0))
    fog = EAS.spawn_actor_from_class(unreal.ExponentialHeightFog, v(0, 0, 20))
    if fog:
        try:
            fog.get_component_by_class(unreal.ExponentialHeightFogComponent).set_editor_property("fog_density", cfg["fog"])
        except Exception:
            pass
    ppv = EAS.spawn_actor_from_class(unreal.PostProcessVolume, v(0, 0, 0))
    if ppv:
        ppv.set_editor_property("unbound", True)
        try:
            s = ppv.get_editor_property("settings")
            s.set_editor_property("override_auto_exposure_bias", True)
            s.set_editor_property("auto_exposure_bias", -1.0)
            ppv.set_editor_property("settings", s)
        except Exception:
            pass
    for i, ang in enumerate((30, 150, 270)):
        rad = math.radians(ang)
        pl = EAS.spawn_actor_from_class(unreal.PointLight, v(950 * math.cos(rad), 950 * math.sin(rad), 320))
        if pl:
            pc = pl.get_component_by_class(unreal.PointLightComponent)
            pc.set_intensity(5000.0)
            pc.set_light_color(lin(cfg["beacon"]))
            pc.set_attenuation_radius(1500.0)

    cp = EAS.spawn_actor_from_class(unreal.CheckpointActor, v(0, -1700, 0), r(0))
    if cp:
        cp.set_actor_label("Checkpoint")
        try:
            tm = cp.get_editor_property("table_mesh")
            if tm and cyl:
                tm.set_static_mesh(cyl)
                tm.set_world_scale3d(unreal.Vector(1.4, 1.4, 0.85))
            cp.set_editor_property("beacon_color", lin(cfg["cp"]))
        except Exception:
            pass

    ps = EAS.spawn_actor_from_class(unreal.PlayerStart, v(0, -1550, 120), r(90))
    if ps:
        ps.set_actor_label("PlayerStart")

    boss = EAS.spawn_actor_from_class(cfg["boss"], v(0, 900, 120), r(-90))
    if boss:
        boss.set_actor_label("Boss")
        set_char(boss, char_mesh(cfg["boss_mesh"]), factor)

    mob_m = char_mesh(cfg["mob"])
    for i, off in enumerate(((-520, 150), (520, 200))):
        m = EAS.spawn_actor_from_class(unreal.EnemyCharacter, v(off[0], off[1], 120), r(-90))
        if m:
            m.set_actor_label("Mob_%d" % i)
            set_char(m, mob_m, factor)

    try:
        ws = unreal.EditorLevelLibrary.get_editor_world().get_world_settings()
        if gm_class:
            ws.set_editor_property("default_game_mode", gm_class)
    except Exception as e:
        unreal.log_warning("gm: %s" % e)

    LES.save_current_level()
    unreal.log("[Alice] built %s" % cfg["map"])


def main():
    cube = load("/Engine/BasicShapes/Cube")
    cyl = load("/Engine/BasicShapes/Cylinder")

    alice = char_mesh("SM_Alice_3D")
    factor = 1.0
    if alice:
        h = mesh_height(alice)
        if h > 0:
            factor = max(0.01, min(175.0 / h, 500.0))

    bp_gm = load("/Game/Alice/Blueprints/BP_AliceGameMode")
    gm_class = bp_gm.generated_class() if bp_gm else None

    arenas = [
        dict(map="L_FlorestaCheshire", boss=unreal.CheshireBoss, boss_mesh="", mob="SM_mob_carta",
             sun=(0.5, 0.35, 0.85), sky=0.5, beacon=(0.5, 0.2, 0.9), fog=0.035, cp=(0.55, 0.2, 0.85)),
        dict(map="L_SalaoCha", boss=unreal.ChapeleiroBoss, boss_mesh="SM_chapeleiro", mob="SM_mob_bule",
             sun=(0.4, 0.8, 0.45), sky=0.6, beacon=(0.3, 0.9, 0.4), fog=0.02, cp=(0.25, 0.85, 0.35)),
        dict(map="L_NevoaCogumelos", boss=unreal.LagartaAzulBoss, boss_mesh="SM_lagarta_boss", mob="SM_mob_biscoito",
             sun=(0.35, 0.55, 1.0), sky=0.7, beacon=(0.3, 0.6, 1.0), fog=0.06, cp=(0.3, 0.6, 1.0)),
        dict(map="L_PatioReal", boss=unreal.RainhaCopasBoss, boss_mesh="SM_rainha_boss", mob="SM_mob_soldado",
             sun=(1.0, 0.45, 0.4), sky=0.5, beacon=(1.0, 0.2, 0.2), fog=0.02, cp=(1.0, 0.15, 0.15)),
        dict(map="L_CampoEtereo", boss=unreal.LidiaBoss, boss_mesh="SM_Lidia_3D", mob="SM_mob_carta",
             sun=(1.0, 0.95, 0.85), sky=1.3, beacon=(1.0, 0.9, 0.6), fog=0.015, cp=(1.0, 0.92, 0.7)),
    ]

    for cfg in arenas:
        try:
            build(cfg, cube, cyl, factor, gm_class)
        except Exception as e:
            unreal.log_warning("[Alice] FAILED %s: %s" % (cfg["map"], e))

    EAL.save_directory("/Game/Alice", False, True)
    unreal.log("[Alice] BUILD_ARENAS DONE (factor=%.3f)" % factor)


main()
