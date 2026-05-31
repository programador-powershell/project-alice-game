"""
Build the non-boss story areas as playable blockout maps + portals, then rewire the
flow: Margem -> Vortice -> Interior -> Toca -> L_Arena(Coelho) -> ... -> Patio(Rainha)
-> Ruinas -> Campo(Lidia).
"""
import math
import unreal

EAL = unreal.EditorAssetLibrary
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def load(p):
    return EAL.load_asset(p) if EAL.does_asset_exist(p) else None


def char_mesh(n):
    return load("/Game/Alice/Characters/%s/StaticMeshes/%s" % (n, n)) if n else None


def v(x, y, z):
    return unreal.Vector(x, y, z)


def r(yaw):
    return unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw)


def lin(t):
    return unreal.LinearColor(t[0], t[1], t[2])


def sm(mesh, loc, rot, scale, label):
    a = EAS.spawn_actor_from_class(unreal.StaticMeshActor, loc, rot)
    if not a:
        return None
    a.set_actor_label(label)
    a.set_actor_scale3d(scale)
    if mesh:
        a.static_mesh_component.set_static_mesh(mesh)
    a.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
    return a


def lights(cfg, cube, cyl):
    sun = EAS.spawn_actor_from_class(unreal.DirectionalLight, v(0, 0, 1500), unreal.Rotator(roll=0, pitch=-44, yaw=40))
    if sun:
        c = sun.get_component_by_class(unreal.DirectionalLightComponent)
        c.set_intensity(2.2); c.set_light_color(lin(cfg["sun"]))
    sky = EAS.spawn_actor_from_class(unreal.SkyLight, v(0, 0, 900))
    if sky:
        sky.get_component_by_class(unreal.SkyLightComponent).set_intensity(cfg.get("sky", 0.6))
    EAS.spawn_actor_from_class(unreal.SkyAtmosphere, v(0, 0, 0))
    fog = EAS.spawn_actor_from_class(unreal.ExponentialHeightFog, v(0, 0, 20))
    if fog:
        try:
            fog.get_component_by_class(unreal.ExponentialHeightFogComponent).set_editor_property("fog_density", cfg.get("fog", 0.03))
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
        pl = EAS.spawn_actor_from_class(unreal.PointLight, v(800 * math.cos(rad), 800 * math.sin(rad), 300))
        if pl:
            pc = pl.get_component_by_class(unreal.PointLightComponent)
            pc.set_intensity(6000.0); pc.set_light_color(lin(cfg["beacon"])); pc.set_attenuation_radius(1400.0)


def make_portal(loc, target, cyl):
    p = EAS.spawn_actor_from_class(unreal.PortalActor, loc, r(0))
    if not p:
        return
    p.set_actor_label("Portal_to_%s" % target)
    try:
        p.set_editor_property("target_level", unreal.Name(target))
        p.set_editor_property("delay", 1.0)
        pm = p.get_editor_property("mesh")
        if pm and cyl:
            pm.set_static_mesh(cyl)
            pm.set_world_scale3d(unreal.Vector(3.5, 3.5, 4.0))
    except Exception as e:
        unreal.log_warning("portal: %s" % e)
    glow = EAS.spawn_actor_from_class(unreal.PointLight, loc + v(0, 0, 250))
    if glow:
        gc = glow.get_component_by_class(unreal.PointLightComponent)
        gc.set_intensity(11000.0); gc.set_light_color(lin((0.5, 0.55, 1.0))); gc.set_attenuation_radius(1700.0)


def make_checkpoint(loc, cyl, color):
    cp = EAS.spawn_actor_from_class(unreal.CheckpointActor, loc, r(0))
    if not cp:
        return
    cp.set_actor_label("Checkpoint")
    try:
        tm = cp.get_editor_property("table_mesh")
        if tm and cyl:
            tm.set_static_mesh(cyl); tm.set_world_scale3d(unreal.Vector(1.4, 1.4, 0.85))
        cp.set_editor_property("beacon_color", lin(color))
    except Exception:
        pass


def spawn_mobs(mesh_name, count, factor):
    m = char_mesh(mesh_name)
    for i in range(count):
        ang = math.radians(360.0 / max(1, count) * i)
        mob = EAS.spawn_actor_from_class(unreal.EnemyCharacter, v(700 * math.cos(ang), 700 * math.sin(ang) + 300, 120), r(-90))
        if mob:
            mob.set_actor_label("Mob_%d" % i)
            try:
                if m:
                    mob.set_editor_property("visual_mesh_asset", m)
                mob.set_editor_property("visual_mesh_scale", factor)
            except Exception:
                pass


def build_area(cfg, cube, cyl, factor, gm_class):
    LES.new_level("/Game/Alice/Maps/" + cfg["map"])
    style = cfg["style"]

    if style == "funnel":
        # descending rings into a shaft; fall to the portal at the bottom
        for i in range(7):
            rad = max(6.0, 32.0 - i * 4.0)
            sm(cyl, v(0, 0, -i * 200), r(i * 20), unreal.Vector(rad, rad, 0.3), "Ring_%d" % i)
        sm(cyl, v(0, 0, -1500), r(0), unreal.Vector(10, 10, 0.4), "Bottom")
        lights(cfg, cube, cyl)
        ps = EAS.spawn_actor_from_class(unreal.PlayerStart, v(0, -200, 260), r(0))
        if ps: ps.set_actor_label("PlayerStart")
        make_portal(v(0, 0, -1380), cfg["portal_to"], cyl)
    elif style == "room":
        sm(cube, v(0, 0, -20), r(0), unreal.Vector(26, 20, 0.5), "Floor")
        # 4 walls
        sm(cube, v(0, 1000, 300), r(0), unreal.Vector(26, 0.6, 8), "WallN")
        sm(cube, v(0, -1000, 300), r(0), unreal.Vector(26, 0.6, 8), "WallS")
        sm(cube, v(1300, 0, 300), r(0), unreal.Vector(0.6, 20, 8), "WallE")
        sm(cube, v(-1300, 0, 300), r(0), unreal.Vector(0.6, 20, 8), "WallW")
        for i in range(6):
            sm(cube, v(-900 + i * 360, 0, 250), r(0), unreal.Vector(0.8, 0.8, 5), "Col_%d" % i)
        lights(cfg, cube, cyl)
        make_checkpoint(v(0, 0, 0), cyl, cfg["beacon"])
        ps = EAS.spawn_actor_from_class(unreal.PlayerStart, v(0, -800, 120), r(90))
        if ps: ps.set_actor_label("PlayerStart")
        make_portal(v(0, 900, 120), cfg["portal_to"], cyl)
        spawn_mobs(cfg["mobs"][0], cfg["mobs"][1], factor)
    elif style == "warren":
        sm(cyl, v(0, 0, -15), r(0), unreal.Vector(50, 50, 0.3), "Floor")
        nseg = 24
        for i in range(nseg):
            ang = math.radians(360.0 / nseg * i)
            sm(cube, v(2500 * math.cos(ang), 2500 * math.sin(ang), 400), r(360.0 / nseg * i), unreal.Vector(3, 7, 9), "Wall_%d" % i)
        # gears = upright cylinders
        for i in range(6):
            ang = math.radians(60 * i)
            sm(cyl, v(1400 * math.cos(ang), 1400 * math.sin(ang), 300), unreal.Rotator(roll=90, pitch=0, yaw=60 * i), unreal.Vector(6, 6, 1.2), "Gear_%d" % i)
        lights(cfg, cube, cyl)
        make_checkpoint(v(0, -1400, 0), cyl, cfg["beacon"])
        ps = EAS.spawn_actor_from_class(unreal.PlayerStart, v(0, -1700, 120), r(90))
        if ps: ps.set_actor_label("PlayerStart")
        make_portal(v(0, 1500, 120), cfg["portal_to"], cyl)
        spawn_mobs(cfg["mobs"][0], cfg["mobs"][1], factor)
    elif style == "ruins":
        sm(cyl, v(0, 0, -15), r(0), unreal.Vector(52, 52, 0.3), "Floor")
        # broken columns + rubble (varied heights)
        for i in range(16):
            ang = math.radians(22.5 * i)
            h = 3.0 + (i % 4) * 2.0
            sm(cube, v(1700 * math.cos(ang), 1700 * math.sin(ang), h * 50), r(22.5 * i), unreal.Vector(1.2, 1.2, h), "Col_%d" % i)
        # central freestanding arch
        sm(cube, v(-180, 600, 250), r(0), unreal.Vector(0.8, 0.8, 6), "ArchL")
        sm(cube, v(180, 600, 250), r(0), unreal.Vector(0.8, 0.8, 6), "ArchR")
        sm(cube, v(0, 600, 560), r(0), unreal.Vector(3, 0.8, 0.8), "ArchTop")
        for i in range(10):
            sm(cube, v(-900 + i * 200, -200 + (i % 3) * 150, 40), r(i * 33), unreal.Vector(1.5, 1.5, 0.6), "Rubble_%d" % i)
        lights(cfg, cube, cyl)
        make_checkpoint(v(0, -1700, 0), cyl, cfg["beacon"])
        ps = EAS.spawn_actor_from_class(unreal.PlayerStart, v(0, -1900, 120), r(90))
        if ps: ps.set_actor_label("PlayerStart")
        make_portal(v(0, 1900, 120), cfg["portal_to"], cyl)
        spawn_mobs(cfg["mobs"][0], cfg["mobs"][1], factor)

    try:
        ws = unreal.EditorLevelLibrary.get_editor_world().get_world_settings()
        if gm_class:
            ws.set_editor_property("default_game_mode", gm_class)
    except Exception as e:
        unreal.log_warning("gm %s: %s" % (cfg["map"], e))

    LES.save_current_level()
    unreal.log("[Alice] built %s -> %s" % (cfg["map"], cfg["portal_to"]))


def rewire_portal(mappath, target):
    if not EAL.does_asset_exist(mappath):
        return
    LES.load_level(mappath)
    n = 0
    for a in EAS.get_all_level_actors():
        if isinstance(a, unreal.PortalActor):
            a.set_editor_property("target_level", unreal.Name(target)); n += 1
    LES.save_current_level()
    unreal.log("[Alice] rewired portal %s -> %s (%d)" % (mappath, target, n))


def rewire_boss_next(mappath, nextlvl):
    if not EAL.does_asset_exist(mappath):
        return
    LES.load_level(mappath)
    n = 0
    for a in EAS.get_all_level_actors():
        if isinstance(a, unreal.BossCharacter):
            a.set_editor_property("next_level_name", unreal.Name(nextlvl)); n += 1
    LES.save_current_level()
    unreal.log("[Alice] rewired boss %s -> %s (%d)" % (mappath, nextlvl, n))


def main():
    cube = load("/Engine/BasicShapes/Cube")
    cyl = load("/Engine/BasicShapes/Cylinder")
    alice = char_mesh("SM_Alice_3D")
    factor = 1.0
    if alice:
        try:
            factor = max(0.01, min(175.0 / max(1.0, alice.get_bounds().box_extent.z * 2.0), 500.0))
        except Exception:
            pass
    bp_gm = load("/Game/Alice/Blueprints/BP_AliceGameMode")
    gm_class = bp_gm.generated_class() if bp_gm else None

    areas = [
        dict(map="L_Vortice", portal_to="L_InteriorDeCha", style="funnel",
             sun=(0.5, 0.25, 0.75), sky=0.5, beacon=(0.78, 0.2, 0.9), fog=0.045, mobs=("", 0)),
        dict(map="L_InteriorDeCha", portal_to="L_TocaMecanica", style="room",
             sun=(0.4, 0.45, 0.72), sky=0.5, beacon=(1.0, 0.7, 0.3), fog=0.02, mobs=("SM_mob_carta", 3)),
        dict(map="L_TocaMecanica", portal_to="L_Arena", style="warren",
             sun=(0.4, 0.55, 1.0), sky=0.6, beacon=(1.0, 0.7, 0.25), fog=0.03, mobs=("SM_mob_soldado", 3)),
        dict(map="L_Ruinas", portal_to="L_CampoEtereo", style="ruins",
             sun=(0.95, 0.4, 0.42), sky=0.5, beacon=(1.0, 0.25, 0.2), fog=0.03, mobs=("SM_mob_soldado", 4)),
    ]
    for cfg in areas:
        try:
            build_area(cfg, cube, cyl, factor, gm_class)
        except Exception as e:
            unreal.log_warning("[Alice] FAILED %s: %s" % (cfg["map"], e))

    # Rewire the flow into the new areas.
    rewire_portal("/Game/Alice/Maps/L_MargemDoRio", "L_Vortice")
    rewire_boss_next("/Game/Alice/Maps/L_PatioReal", "L_Ruinas")

    EAL.save_directory("/Game/Alice", False, True)
    unreal.log("[Alice] AREAS2 DONE (factor=%.3f)" % factor)


main()
