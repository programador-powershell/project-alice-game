"""
Headless level + Blueprint assembly for Alice's first playable slice (v2).

Imported character GLBs live at /Game/Alice/Characters/<N>/StaticMeshes/<N> (single mesh).
Builds L_Arena: a clockwork boss arena from basic shapes (real boundary geometry = no
invisible walls), Lumen lighting + fog, a Mesa de Chá checkpoint, the White Rabbit boss
and two mobs (with their static meshes auto-scaled to a consistent unit), plus BP_Alice /
BP_AliceGameMode. Saves everything.

  UnrealEditor-Cmd.exe E:\Alice\Alice.uproject -ExecutePythonScript=E:\Alice\Tools\build_game.py
"""
import math
import unreal

AT  = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

BP_DIR  = "/Game/Alice/Blueprints"
MAP_DIR = "/Game/Alice/Maps"

TARGET_ALICE_CM = 175.0  # desired Alice height; derives a uniform unit factor for all chars


def load(path):
    try:
        if EAL.does_asset_exist(path):
            return EAL.load_asset(path)
    except Exception as e:
        unreal.log_warning("load %s: %s" % (path, e))
    return None


def char_mesh(name):
    return load("/Game/Alice/Characters/%s/StaticMeshes/%s" % (name, name))


def mesh_height(mesh):
    try:
        b = mesh.get_bounds()
        return max(1.0, b.box_extent.z * 2.0)
    except Exception as e:
        unreal.log_warning("bounds: %s" % e)
        return 0.0


def v(x, y, z):
    return unreal.Vector(x, y, z)


def r(yaw):
    return unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw)


def make_bp(name, parent_class, props=None):
    path = BP_DIR + "/" + name
    bp = load(path)
    if not bp:
        fac = unreal.BlueprintFactory()
        fac.set_editor_property("parent_class", parent_class)
        bp = AT.create_asset(name, BP_DIR, unreal.Blueprint, fac)
    if bp and props:
        try:
            cdo = unreal.get_default_object(bp.generated_class())
            for k, val in props.items():
                cdo.set_editor_property(k, val)
            unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        except Exception as e:
            unreal.log_warning("CDO %s: %s" % (name, e))
    if bp:
        EAL.save_asset(path)
    return bp


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
        unreal.log_warning("set_char %s: %s" % (actor, e))


def build_lighting():
    sun = EAS.spawn_actor_from_class(unreal.DirectionalLight, v(0, 0, 1500), unreal.Rotator(roll=0, pitch=-44, yaw=40))
    if sun:
        sun.set_actor_label("Sun")
        c = sun.get_component_by_class(unreal.DirectionalLightComponent)
        c.set_intensity(3.2)
        c.set_light_color(unreal.LinearColor(0.55, 0.7, 1.0))
    sky = EAS.spawn_actor_from_class(unreal.SkyLight, v(0, 0, 900))
    if sky:
        sky.set_actor_label("SkyLight")
        sky.get_component_by_class(unreal.SkyLightComponent).set_intensity(1.2)
    atm = EAS.spawn_actor_from_class(unreal.SkyAtmosphere, v(0, 0, 0))
    if atm:
        atm.set_actor_label("SkyAtmosphere")
    fog = EAS.spawn_actor_from_class(unreal.ExponentialHeightFog, v(0, 0, 20))
    if fog:
        fog.set_actor_label("HeightFog")
        try:
            fc = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
            fc.set_editor_property("fog_density", 0.025)
        except Exception:
            pass
    ppv = EAS.spawn_actor_from_class(unreal.PostProcessVolume, v(0, 0, 0))
    if ppv:
        ppv.set_actor_label("PostProcess")
        ppv.set_editor_property("unbound", True)
    for i, ang in enumerate((30, 150, 270)):
        rad = math.radians(ang)
        pl = EAS.spawn_actor_from_class(unreal.PointLight, v(950 * math.cos(rad), 950 * math.sin(rad), 320))
        if pl:
            pc = pl.get_component_by_class(unreal.PointLightComponent)
            pc.set_intensity(9000.0)
            pc.set_light_color(unreal.LinearColor(1.0, 0.7, 0.25))
            pc.set_attenuation_radius(1500.0)
            pl.set_actor_label("Beacon_%d" % i)


def main():
    for d in (BP_DIR, MAP_DIR):
        if not EAL.does_directory_exist(d):
            EAL.make_directory(d)

    cube = load("/Engine/BasicShapes/Cube")
    cyl  = load("/Engine/BasicShapes/Cylinder")

    alice  = char_mesh("SM_Alice_3D")
    coelho = char_mesh("SM_coelho_boss") or char_mesh("SM_coelho")
    mob    = char_mesh("SM_mob_soldado") or char_mesh("SM_boss_soldado")

    factor = 1.0
    if alice:
        h = mesh_height(alice)
        if h > 0:
            factor = TARGET_ALICE_CM / h
    factor = max(0.01, min(factor, 500.0))
    unreal.log("[Alice] unit factor = %.4f (Alice raw height -> %.1f cm target)" % (factor, TARGET_ALICE_CM))

    # --- Blueprints ---
    bp_alice = make_bp("BP_Alice", unreal.AliceCharacter,
                       {"visual_mesh_asset": alice, "visual_mesh_scale": factor} if alice else {"visual_mesh_scale": factor})
    gm_props = {}
    if bp_alice:
        gm_props["default_pawn_class"] = bp_alice.generated_class()
    bp_gm = make_bp("BP_AliceGameMode", unreal.AliceGameMode, gm_props)

    # --- Level ---
    LES.new_level(MAP_DIR + "/L_Arena")

    spawn_sm(cyl, v(0, 0, -15), r(0), unreal.Vector(54.0, 54.0, 0.3), "ArenaFloor")
    spawn_sm(cyl, v(0, 900, 5), r(0), unreal.Vector(14.0, 14.0, 0.15), "BossDais")

    nseg = 28
    for i in range(nseg):
        ang = math.radians(360.0 / nseg * i)
        spawn_sm(cube, v(2800 * math.cos(ang), 2800 * math.sin(ang), 420),
                 r(360.0 / nseg * i), unreal.Vector(3.2, 7.5, 9.5), "Wall_%d" % i)
    # inner pillars
    for i in range(8):
        ang = math.radians(45 * i)
        spawn_sm(cube, v(1750 * math.cos(ang), 1750 * math.sin(ang), 250),
                 r(45 * i), unreal.Vector(1.4, 1.4, 6.0), "Pillar_%d" % i)

    build_lighting()

    # Checkpoint (basic-shape table placeholder + beacon light is the real marker)
    cp = EAS.spawn_actor_from_class(unreal.CheckpointActor, v(0, -1700, 0), r(0))
    if cp:
        cp.set_actor_label("Checkpoint_Coelho")
        try:
            tm = cp.get_editor_property("table_mesh")
            if tm and cyl:
                tm.set_static_mesh(cyl)
                tm.set_world_scale3d(unreal.Vector(1.4, 1.4, 0.85))
            cp.set_editor_property("beacon_color", unreal.LinearColor(1.0, 0.7, 0.25))
        except Exception as e:
            unreal.log_warning("cp: %s" % e)

    ps = EAS.spawn_actor_from_class(unreal.PlayerStart, v(0, -1550, 120), r(90))
    if ps:
        ps.set_actor_label("PlayerStart")

    boss = EAS.spawn_actor_from_class(unreal.CoelhoBrancoBoss, v(0, 900, 120), r(-90))
    if boss:
        boss.set_actor_label("Boss_CoelhoBranco")
        set_char(boss, coelho, factor)

    for i, off in enumerate(((-520, 150), (520, 200))):
        m = EAS.spawn_actor_from_class(unreal.EnemyCharacter, v(off[0], off[1], 120), r(-90))
        if m:
            m.set_actor_label("Mob_%d" % i)
            set_char(m, mob, factor)

    # GameMode override on the map
    try:
        world = unreal.EditorLevelLibrary.get_editor_world()
        ws = world.get_world_settings()
        if bp_gm:
            ws.set_editor_property("default_game_mode", bp_gm.generated_class())
        unreal.log("[Alice] world GameMode set")
    except Exception as e:
        unreal.log_warning("worldsettings gamemode (will rely on ini): %s" % e)

    LES.save_current_level()
    EAL.save_directory("/Game/Alice", False, True)
    unreal.log("[Alice] BUILD_GAME DONE  (factor=%.3f)" % factor)


main()
