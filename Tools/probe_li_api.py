"""Descobre API de Level Instance / WP no UE5.7."""
import unreal
L = lambda s: unreal.log(f"[LI] {s}")

for n in ["LevelInstanceSubsystem","EditorLevelUtils","LevelStreamingDynamic",
          "EditorActorSubsystem","new_level","EditorLoadingAndSavingUtils"]:
    L(f"  unreal.{n} = {hasattr(unreal,n)}")

# metodos de EditorLevelUtils
elu = [m for m in dir(unreal.EditorLevelUtils) if not m.startswith('_')] if hasattr(unreal,'EditorLevelUtils') else []
L(f"  EditorLevelUtils: {elu}")

# LevelInstanceSubsystem methods
if hasattr(unreal,'LevelInstanceSubsystem'):
    lis = [m for m in dir(unreal.LevelInstanceSubsystem) if 'creat' in m.lower() or 'level' in m.lower()]
    L(f"  LevelInstanceSubsystem create-ish: {lis}")

# EditorLoadingAndSaving new map WP?
els = [m for m in dir(unreal.EditorLoadingAndSavingUtils) if 'new' in m.lower() or 'map' in m.lower()]
L(f"  ELSU new/map: {els}")

# como criar level instance actor: LevelInstanceEditorLibrary?
for n in ["LevelInstanceEditorLibrary","ActorPartitionSubsystem","WorldPartitionBlueprintLibrary","NewLevelInstanceParams"]:
    L(f"  unreal.{n} = {hasattr(unreal,n)}")
L("END")
