"""Cria tela inicial souls-like pra Project Alice (level + BPs + widgets + mood)."""
import unreal
import sys

TARGET_FOLDER = "/Game/UI/MainMenu"
MAP_PATH = f"{TARGET_FOLDER}/L_MainMenu"

def log(msg): unreal.log(f"[MainMenu] {msg}"); print(f"[MainMenu] {msg}")
def log_err(msg): unreal.log_error(f"[MainMenu] {msg}"); print(f"[MainMenu][ERR] {msg}")

def ensure_folder(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)

def create_blueprint(name, package_path, parent_class):
    full = f"{package_path}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(full):
        log(f"skip ja existe: {full}"); return unreal.EditorAssetLibrary.load_asset(full)
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    obj = tools.create_asset(name, package_path, unreal.Blueprint, factory)
    if obj:
        unreal.EditorAssetLibrary.save_asset(full, only_if_is_dirty=False); log(f"criado: {full}")
    return obj

def create_widget_blueprint(name, package_path):
    full = f"{package_path}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(full):
        log(f"skip ja existe: {full}"); return unreal.EditorAssetLibrary.load_asset(full)
    try:
        factory = unreal.WidgetBlueprintFactory()
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        obj = tools.create_asset(name, package_path, unreal.WidgetBlueprint, factory)
        if obj:
            unreal.EditorAssetLibrary.save_asset(full, only_if_is_dirty=False); log(f"criado widget: {full}")
        return obj
    except Exception as exc:
        log_err(f"widget {name}: {exc}"); return None

def _les():
    try: return unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    except Exception: return None
def _actors():
    try: return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    except Exception: return None

def spawn(cls, loc, rot=None):
    rot = rot or unreal.Rotator(0, 0, 0)
    a = _actors()
    if a:
        return a.spawn_actor_from_class(cls, loc, rot)
    return unreal.EditorLevelLibrary.spawn_actor_from_class(cls, loc, rot)

def create_main_menu_level():
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        log("L_MainMenu ja existe");
        les = _les()
        if les: les.load_level(MAP_PATH)
        return MAP_PATH
    ensure_folder(TARGET_FOLDER)
    les = _les()
    if les: les.new_level(MAP_PATH)
    else: unreal.EditorLevelLibrary.new_level(MAP_PATH)
    log(f"L_MainMenu criado: {MAP_PATH}")

    try:
        dl = spawn(unreal.DirectionalLight, unreal.Vector(0, 0, 500), unreal.Rotator(-40, 30, 0))
        if dl:
            dl.set_actor_label("KeyLight")
            lc = dl.get_component_by_class(unreal.DirectionalLightComponent)
            if lc: lc.set_intensity(0.5); lc.set_light_color(unreal.LinearColor(0.4, 0.3, 0.6, 1.0))
    except Exception as exc: log_err(f"directional: {exc}")
    try:
        sl = spawn(unreal.SkyLight, unreal.Vector(0, 0, 200))
        if sl: sl.set_actor_label("SkyLight")
    except Exception as exc: log_err(f"skylight: {exc}")
    try:
        sky = spawn(unreal.SkyAtmosphere, unreal.Vector(0, 0, 0))
    except Exception as exc: log_err(f"skyatmo: {exc}")
    for label, txt, z, size, col in [
        ("TitleText", "PROJECT ALICE", 200, 120, unreal.Color(220, 200, 230, 255)),
        ("SubtitleText", "souls-like dark fantasy   |   UE 5.7", 50, 35, unreal.Color(120, 100, 140, 255)),
        ("PressStartText", "PRESSIONE ENTER PARA INICIAR", -150, 50, unreal.Color(180, 160, 200, 255)),
    ]:
        try:
            t = spawn(unreal.TextRenderActor, unreal.Vector(500, 0, z), unreal.Rotator(0, 180, 0))
            if t:
                t.set_actor_label(label)
                tc = t.get_component_by_class(unreal.TextRenderComponent)
                if tc:
                    tc.set_text(unreal.Text(txt)); tc.set_text_render_color(col); tc.set_world_size(size)
                    tc.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
        except Exception as exc: log_err(f"text {label}: {exc}")
    try:
        spawn(unreal.PlayerStart, unreal.Vector(-300, 0, 80))
    except Exception as exc: log_err(f"player start: {exc}")
    try:
        ppv = spawn(unreal.PostProcessVolume, unreal.Vector(0, 0, 0))
        if ppv:
            ppv.set_actor_label("MoodVolume"); ppv.set_editor_property("unbound", True)
            s = ppv.get_editor_property("settings")
            s.override_vignette_intensity = True; s.vignette_intensity = 0.8
            s.override_scene_color_tint = True; s.scene_color_tint = unreal.LinearColor(0.45, 0.4, 0.55, 1.0)
            ppv.set_editor_property("settings", s)
    except Exception as exc: log_err(f"postprocess: {exc}")

    les = _les()
    if les: les.save_current_level()
    unreal.EditorAssetLibrary.save_asset(MAP_PATH, only_if_is_dirty=False)
    log(f"L_MainMenu salvo: {MAP_PATH}")
    return MAP_PATH

def main():
    ensure_folder(TARGET_FOLDER)
    create_main_menu_level()
    create_blueprint("BP_MainMenuController", TARGET_FOLDER, unreal.PlayerController)
    create_blueprint("BP_MainMenuGameMode", TARGET_FOLDER, unreal.GameModeBase)
    create_widget_blueprint("WBP_MainMenu", TARGET_FOLDER)
    create_widget_blueprint("WBP_Settings", TARGET_FOLDER)
    create_widget_blueprint("WBP_Continue", TARGET_FOLDER)
    create_widget_blueprint("WBP_NewGame", TARGET_FOLDER)
    create_blueprint("BP_SaveGameAlice", TARGET_FOLDER, unreal.SaveGame)
    log("Main Menu base criado.")

if __name__ == "__main__":
    main()
