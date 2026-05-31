"""Preenche BS_CoelhoLoco via BlendSpaceLibrary (API correta UE5.7).
Recria limpo se preciso. Eixo X=Speed 0..600, samples idle/walk/run."""
import unreal
L = lambda s: unreal.log(f"[FB] {s}")

DST = "/Game/Alice/AnimCoelho"
SKEL = unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer_Skeleton")

# apaga BS velho e recria limpo
old = f"{DST}/BS_CoelhoLoco"
if unreal.EditorAssetLibrary.does_asset_exist(old):
    unreal.EditorAssetLibrary.delete_asset(old)
    L("BS velho deletado")

f = unreal.BlendSpaceFactory1D()
f.set_editor_property("target_skeleton", SKEL)
tools = unreal.AssetToolsHelpers.get_asset_tools()
bs = tools.create_asset("BS_CoelhoLoco", DST, unreal.BlendSpace1D, f)
L(f"BS recriado = {bs is not None}")

# metodos da BlendSpaceLibrary
lib_methods = [m for m in dir(unreal.BlendSpaceLibrary) if not m.startswith('_')]
L(f"BlendSpaceLibrary metodos: {lib_methods}")

idle = unreal.load_asset(f"{DST}/C_Idle")
walk = unreal.load_asset(f"{DST}/C_Walk")
run  = unreal.load_asset(f"{DST}/C_Run")

# configura eixo via editor_property
try:
    # nome do eixo X
    bs.set_editor_property("blend_parameters", bs.get_editor_property("blend_parameters"))
except Exception as e:
    L(f"axis cfg: {e}")

# tenta add via library
added=0
for clip, spd in [(idle,0.0),(walk,150.0),(run,550.0)]:
    if not clip: continue
    try:
        unreal.BlendSpaceLibrary.add_sample(bs, clip, unreal.Vector(spd,0,0))
        added+=1
    except Exception as e:
        L(f"  lib.add_sample({spd}) err: {e}")
L(f"samples via lib: {added}")
if bs: unreal.EditorAssetLibrary.save_loaded_asset(bs, only_if_is_dirty=False)
L("END")
