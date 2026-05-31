"""Mapeia: todos .umap, GameDefaultMap, e como mapas conectam (portais/OpenLevel)."""
import unreal
L = lambda s: unreal.log(f"[MC] {s}")

ar = unreal.AssetRegistryHelpers.get_asset_registry()
maps = [str(a.package_name) for a in ar.get_assets_by_path("/Game/Alice/Maps", recursive=True) if str(a.asset_class_path.asset_name)=="World"]
L(f"MAPAS ({len(maps)}):")
for m in sorted(maps): L(f"  {m}")

# procura portais / triggers de transicao no L_Arena
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
portals=0
for a in eas.get_all_level_actors():
    cn = a.get_class().get_name()
    if any(t in cn for t in ("Portal","Trigger","Transition","Checkpoint","Door","LevelStream")):
        portals+=1
        L(f"  L_Arena portal/trigger: {cn} '{a.get_actor_label()}'")
L(f"L_Arena portais={portals}")

# C++ tem classe de portal?
L("END")
