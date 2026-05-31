"""
Build L_MargemDoRio — the riverbank intro (roteiro scene 1): dusk-gold vale, a river
channel, the sister Lidia as a static NPC, and a PortalActor that leads into the boss
rush (L_Arena). Standalone, no combat. Uses BP_AliceGameMode so the player is Alice.

  UnrealEditor-Cmd.exe E:\Alice\Alice.uproject -ExecutePythonScript=E:\Alice\Tools\build_margem.py
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


def main():
    cube = load("/Engine/BasicShapes/Cube")
    cyl = load("/Engine/BasicShapes/Cylinder")

    alice = char_mesh("SM_Alice_3D")
    factor = 1.0
    if alice:
        try:
            h = max(1.0, alice.get_bounds().box_extent.z * 2.0)
            factor = max(0.01, min(175.0 / h, 500.0))
        except Exception:
            pass

    LES.new_level("/Game/Alice/Maps/L_MargemDoRio")

    # Ground vale + river channel
    sm(cube, v(0, 0, -40), r(0), unreal.Vector(80, 90, 0.6), "Ground")
    sm(cube, v(0, 0, -70), r(0), unreal.Vector(10, 90, 0.5), "RiverChannel")
    # Bank rocks
    for i in range(14):
        x = -700 + (i * 100) % 1400 - 700
        sm(cube, v(620 * (1 if i % 2 else -1), -2000 + i * 280, -10), r(i * 23),
           unreal.Vector(1.2, 1.2, 0.8), "Rock_%d" % i)
    # Distant castle silhouette (tall blocks far north)
    for i, (dx, h) in enumerate(((-400, 26), (-150, 34), (120, 30), (380, 22))):
        sm(cube, v(dx, 4200, h * 50 - 40), r(0), unreal.Vector(3, 3, h), "Castle_%d" % i)

    # Sister Lidia (static NPC) by the river
    lidia = char_mesh("SM_Lidia_3D")
    if lidia:
        a = sm(lidia, v(220, -1350, 5), r(220), unreal.Vector(factor, factor, factor), "Lidia_NPC")

    # Dusk-gold lighting
    sun = EAS.spawn_actor_from_class(unreal.DirectionalLight, v(0, 0, 1500), unreal.Rotator(roll=0, pitch=-11, yaw=205))
    if sun:
        c = sun.get_component_by_class(unreal.DirectionalLightComponent)
        c.set_intensity(3.0)
        c.set_light_color(lin((1.0, 0.72, 0.42)))
    sky = EAS.spawn_actor_from_class(unreal.SkyLight, v(0, 0, 900))
    if sky:
        sky.get_component_by_class(unreal.SkyLightComponent).set_intensity(0.7)
    EAS.spawn_actor_from_class(unreal.SkyAtmosphere, v(0, 0, 0))
    fog = EAS.spawn_actor_from_class(unreal.ExponentialHeightFog, v(0, 0, 20))
    if fog:
        try:
            fog.get_component_by_class(unreal.ExponentialHeightFogComponent).set_editor_property("fog_density", 0.025)
        except Exception:
            pass
    ppv = EAS.spawn_actor_from_class(unreal.PostProcessVolume, v(0, 0, 0))
    if ppv:
        ppv.set_editor_property("unbound", True)
        try:
            s = ppv.get_editor_property("settings")
            s.set_editor_property("override_auto_exposure_bias", True)
            s.set_editor_property("auto_exposure_bias", -0.5)
            ppv.set_editor_property("settings", s)
        except Exception:
            pass

    # Player start at the near bank, facing the portal
    ps = EAS.spawn_actor_from_class(unreal.PlayerStart, v(0, -1600, 120), r(90))
    if ps:
        ps.set_actor_label("PlayerStart")

    # Portal "Toca do Coelho" -> the boss rush
    portal = EAS.spawn_actor_from_class(unreal.PortalActor, v(0, 1300, 120), r(0))
    if portal:
        portal.set_actor_label("Portal_TocaDoCoelho")
        try:
            portal.set_editor_property("target_level", unreal.Name("L_Arena"))
            portal.set_editor_property("delay", 1.2)
            pm = portal.get_editor_property("mesh")
            if pm and cyl:
                pm.set_static_mesh(cyl)
                pm.set_world_scale3d(unreal.Vector(3.5, 3.5, 4.0))
        except Exception as e:
            unreal.log_warning("portal: %s" % e)
        # glow at the portal
        pl = EAS.spawn_actor_from_class(unreal.PointLight, v(0, 1300, 300))
        if pl:
            lc = pl.get_component_by_class(unreal.PointLightComponent)
            lc.set_intensity(12000.0)
            lc.set_light_color(lin((0.5, 0.55, 1.0)))
            lc.set_attenuation_radius(1800.0)

    # GameMode -> player is Alice
    try:
        bp_gm = load("/Game/Alice/Blueprints/BP_AliceGameMode")
        ws = unreal.EditorLevelLibrary.get_editor_world().get_world_settings()
        if bp_gm:
            ws.set_editor_property("default_game_mode", bp_gm.generated_class())
    except Exception as e:
        unreal.log_warning("gm: %s" % e)

    LES.save_current_level()
    EAL.save_directory("/Game/Alice", False, True)
    unreal.log("[Alice] MARGEM DONE (factor=%.3f)" % factor)


main()
