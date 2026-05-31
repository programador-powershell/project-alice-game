"""Inicia PIE, deixa 1.5s rodando, le a transform de um bone do player em 2 momentos.
Se o bone muda = ANIMA de verdade no jogo. Depois para o PIE.
Tudo via bridge — nao precisa o usuario jogar."""
import unreal, time
L = lambda s: unreal.log(f"[PIE] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

# inicia PIE
les.editor_request_begin_play()
L("PIE begin requested")
