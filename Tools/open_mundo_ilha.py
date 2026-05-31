"""Abre L_MundoIlha no editor + build nav."""
import unreal
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_MundoIlha")
unreal.SystemLibrary.execute_console_command(None, "RebuildNavigation")
unreal.log("[OMI] L_MundoIlha aberto + nav rebuild")
