"""Inicia PIE no L_Arena. Screenshot vem em script separado apos delay."""
import unreal
L=lambda s:unreal.log(f"[PA] {s}")
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
les=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
les.editor_request_begin_play()
L("PIE begin")
L("END")
