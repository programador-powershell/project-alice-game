"""Teste decisivo: forca o SkeletalMeshComponent do BP_Alice a tocar Alice_Idle
em loop, modo SingleNode, direto no CDO. Independe do C++.
Se no Play animar = pesos OK (problema era runtime). Se estatua = pesos ruins.
"""
import unreal
L = lambda s: unreal.log(f"[FI] {s}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")

# estado atual do animation_mode
L(f"animation_mode atual = {mc.get_editor_property('animation_mode')}")

idle = unreal.load_asset("/Game/Alice/AnimAlice/Alice_Idle")
L(f"Alice_Idle = {'OK' if idle else 'MISS'}")

# forca single node + anim idle loop
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
play = unreal.SingleAnimationPlayData()
play.anim_to_play = idle
play.looping = True
play.playing = True
mc.set_editor_property("animation_data", play)
L("setado: SingleNode + Alice_Idle loop playing")

# tambem liga update no editor pra ver no viewport sem PIE
try:
    mc.set_editor_property("update_animation_in_editor", True)
    L("update_animation_in_editor = True")
except Exception as e:
    L(f"update_in_editor err: {e}")

unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L(f"animation_mode agora = {mc.get_editor_property('animation_mode')}")
L("SALVO — da Alt+P. Se animar idle = pesos OK. Se estatua = re-rig.")
L("END")
