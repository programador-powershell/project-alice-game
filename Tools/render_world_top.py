"""Render topo do L_Mundo pra ver layout das areas + roads."""
import unreal
L = lambda s: unreal.log(f"[RT] {s}")
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
# camera topo: centro mundo (0, 375m) alto, olhando baixo
unreal.EditorLevelLibrary.set_level_viewport_camera_info(
    unreal.Vector(0, 37500, 120000), unreal.Rotator(-90,0,0))
shot = r"E:\Alice\_PREVIEWS\world_top.png"
unreal.AutomationLibrary.take_high_res_screenshot(1200,1000, shot)
L(f"shot -> {shot}")
L("END")
