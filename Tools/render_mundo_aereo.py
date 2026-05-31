"""Render L_Mundo de cima (top) + iso pra ver layout/conexoes das 10 areas + pontes.
Salva 2 PNG. Mostra se mapa ta ligado ou isolado."""
import unreal
L=lambda s:unreal.log(f"[RA] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
# garante sublevels visiveis
import time

# TOP-DOWN: centro mundo ~(0, 37500), alto
unreal.EditorLevelLibrary.set_level_viewport_camera_info(
    unreal.Vector(0, 37500, 200000), unreal.Rotator(-90, 0, 0))
unreal.SystemLibrary.execute_console_command(None, "HighResShot 1600x1200 filename=mundo_top")
L("top shot disparado")

L("END")
