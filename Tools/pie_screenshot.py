"""Inicia PIE, screenshot do que o JOGADOR ve, para PIE. Verdade sobre a camera."""
import unreal
L = lambda s: unreal.log(f"[PS] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
les=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
try:
    les.editor_request_begin_play()
    L("PIE iniciado — screenshot vem no proximo comando (delay p/ spawn)")
except Exception as e:
    L(f"play err: {e}")
L("END")
