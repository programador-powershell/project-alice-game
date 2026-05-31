from pathlib import Path
import unreal

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "Content" / "UI" / "MainMenu" / "SourceArt"
DESTINATION = "/Game/UI/MainMenu"
ASSETS = [SOURCE_DIR / "menu_cheshire_clean.png", SOURCE_DIR / "autosave_icon.png"]

def main():
    tasks = []
    for source in ASSETS:
        task = unreal.AssetImportTask()
        task.filename = str(source)
        task.destination_path = DESTINATION
        task.automated = True
        task.save = True
        task.replace_existing = True
        task.replace_existing_settings = True
        tasks.append(task)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    unreal.EditorAssetLibrary.save_directory(DESTINATION, only_if_is_dirty=False, recursive=True)
    for task in tasks:
        print(f"[MenuArt] {task.filename} -> {task.imported_object_paths}")

if __name__ == "__main__":
    main()
