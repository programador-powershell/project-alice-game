"""Link robusto: cada etapa em try. Nao deixa anim C_* quebrado travar tudo.
Tambem diagnostica os C_* (skeleton invalido)."""
import unreal
L = lambda s: unreal.log(f"[LW2] {s}")

# === diag anims C_* ===
L("--- diag AnimCoelho ---")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
for a in ar.get_assets_by_path("/Game/Alice/AnimCoelho", recursive=True):
    n=str(a.package_name); cls=str(a.asset_class_path.asset_name)
    if cls=="AnimSequence":
        try:
            asset=unreal.load_asset(n)
            sk=asset.get_skeleton() if asset else None
            L(f"  {n.split('/')[-1]} skel={sk.get_name() if sk else 'NULL'}")
        except Exception as e:
            L(f"  {n.split('/')[-1]} ERR {e}")

# === 1. Portal Margem ===
try:
    unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_MargemDoRio")
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    pc = unreal.load_class(None, "/Script/Alice.PortalActor")
    for a in eas.get_all_level_actors():
        if "Portal" in a.get_class().get_name(): eas.destroy_actor(a)
    ps=None
    for a in eas.get_all_level_actors():
        if "PlayerStart" in a.get_class().get_name(): ps=a; break
    loc=unreal.Vector(0,1500,150)
    if ps:
        p=ps.get_actor_location(); loc=unreal.Vector(p.x,p.y+1200,p.z)
    if pc:
        portal=eas.spawn_actor_from_class(pc,loc)
        portal.set_actor_label("Portal_ToMundo")
        portal.set_editor_property("target_level","L_Mundo")
        L(f"portal Margem->L_Mundo @ {loc}")
    unreal.EditorLoadingAndSavingUtils.save_current_level()
    L("Margem OK")
except Exception as e:
    L(f"MARGEM ERR: {e}")

# === 2+3. GameMode + Nav no Mundo ===
try:
    unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
    eas2 = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ws=None
    for a in eas2.get_all_level_actors():
        if "WorldSettings" in a.get_class().get_name(): ws=a; break
    gm=unreal.load_class(None,"/Game/Alice/Blueprints/BP_AliceGameMode.BP_AliceGameMode_C")
    if ws and gm: ws.set_editor_property("default_game_mode",gm); L("GameMode OK")
    # nav
    hasNav=any("NavMeshBounds" in a.get_class().get_name() for a in eas2.get_all_level_actors())
    if not hasNav:
        nav=eas2.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(0,37500,0))
        nav.set_actor_scale3d(unreal.Vector(160,140,30)); nav.set_actor_label("WorldNav")
        L("Nav OK")
    unreal.EditorLoadingAndSavingUtils.save_current_level()
    L("Mundo OK")
except Exception as e:
    L(f"MUNDO ERR: {e}")
L("END")
