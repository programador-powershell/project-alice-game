import unreal
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
try:
    les.editor_request_end_play()
    unreal.log("[stop] PIE ended")
except Exception as e:
    unreal.log(f"[stop] {e}")
