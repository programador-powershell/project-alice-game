"""Screenshot do PIE em andamento + le pos camera vs pawn."""
import unreal
L = lambda s: unreal.log(f"[P2] {s}")

# acha mundo PIE
w=None
for world in unreal.EditorLevelLibrary.get_editor_world().get_world() if False else []:
    pass
# pega via GameplayStatics no PIE world
try:
    pc = unreal.GameplayStatics.get_player_controller(unreal.EditorLevelLibrary.get_game_world(), 0) if hasattr(unreal.EditorLevelLibrary,'get_game_world') else None
except Exception as e:
    pc=None; L(f"pc err: {e}")

# screenshot via console (vai pro Saved/Screenshots)
unreal.SystemLibrary.execute_console_command(None, "HighResShot 1280x720")
L("HighResShot disparado (Saved/Screenshots/WindowsEditor)")
L("END")
