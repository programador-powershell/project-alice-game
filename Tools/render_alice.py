"""Render SK_Alice with M_AliceDress (MID) in lit L_Arena via SceneCapture2D -> PNG.
Two stills: solid (DissolveAmount=0) and mid-dissolve (0.45) to verify the magic shader."""
import unreal

status = []
def log(s):
    status.append(s); print("RENDER " + s)

try:
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    les.load_level("/Game/Alice/Maps/L_Arena")
    ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = ues.get_editor_world()
    actsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

    SK = unreal.load_asset("/Game/Alice/Characters/AliceRig/SK_Alice")
    MAT = unreal.load_asset("/Game/Alice/Materials/M_AliceDress")
    log("SK=%s MAT=%s" % (SK is not None, MAT is not None))

    loc = unreal.Vector(0, 0, 150)
    alice = actsys.spawn_actor_from_class(unreal.SkeletalMeshActor, loc, unreal.Rotator(0, 0, 0))
    smc = alice.skeletal_mesh_component
    smc.set_skeletal_mesh_asset(SK)
    smc.set_render_custom_depth(True)
    mid = smc.create_dynamic_material_instance(0, MAT)
    if mid:
        mid.set_vector_parameter_value("BaseTint", unreal.LinearColor(0.55, 0.30, 0.60))
        mid.set_vector_parameter_value("EmissiveColor", unreal.LinearColor(1.0, 0.2, 0.85))
        mid.set_scalar_parameter_value("EmissivePower", 6.0)
        mid.set_scalar_parameter_value("DissolveAmount", 0.0)
    log("alice spawned mid=%s nummat=%d" % (mid is not None, smc.get_num_materials()))

    # scale Alice to ~180 cm (her raw Blender export is tiny), feet near floor
    org, ext = alice.get_actor_bounds(False)
    h = max(1.0, ext.z * 2.0)
    s = 180.0 / h
    alice.set_actor_scale3d(unreal.Vector(s, s, s))
    alice.set_actor_location(unreal.Vector(0, 0, 100.0), False, False)
    org, ext = alice.get_actor_bounds(False)

    # 3/4 close framing
    dist = ext.z * 2.3 + 70
    cam_loc = unreal.Vector(org.x + dist * 0.85, org.y - dist * 0.5, org.z + ext.z * 0.28)
    cam_rot = unreal.MathLibrary.find_look_at_rotation(cam_loc, org)

    # key light shining FROM the camera onto Alice (front-lit, not backlit)
    try:
        dl = actsys.spawn_actor_from_class(unreal.DirectionalLight, cam_loc, cam_rot)
        dlc = dl.get_component_by_class(unreal.DirectionalLightComponent)
        if dlc:
            dlc.set_intensity(12.0)
        sky = actsys.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(org.x, org.y, org.z + 200), unreal.Rotator(0, 0, 0))
        skc = sky.get_component_by_class(unreal.SkyLightComponent)
        if skc:
            skc.set_intensity(1.5)
    except Exception as le:
        log("light skip %s" % le)

    rt = unreal.RenderingLibrary.create_render_target2d(world, 640, 900, unreal.TextureRenderTargetFormat.RTF_RGBA8)
    cap = actsys.spawn_actor_from_class(unreal.SceneCapture2D, cam_loc, cam_rot)
    cc = cap.capture_component2d
    cc.set_editor_property("texture_target", rt)
    cc.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_BASE_COLOR)
    cc.set_editor_property("fov_angle", 40.0)
    cc.set_editor_property("capture_every_frame", False)
    cc.set_editor_property("capture_on_movement", False)

    cc.capture_scene()
    unreal.RenderingLibrary.export_render_target(world, rt, r"E:\Alice\_PREVIEWS", "alice_dress_solid")
    log("rendered solid")

    if mid:
        mid.set_scalar_parameter_value("DissolveAmount", 0.45)
    cc.capture_scene()
    unreal.RenderingLibrary.export_render_target(world, rt, r"E:\Alice\_PREVIEWS", "alice_dress_dissolve")
    log("rendered dissolve")

except Exception as e:
    log("EXCEPTION %s" % e)

with open(r"E:\Alice\render_status.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(status))
print("RENDER DONE")
