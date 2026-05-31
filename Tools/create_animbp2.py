"""Cria BlendSpace1D + AnimBP com try/except em CADA passo pra achar o que falha."""
import unreal
L = lambda s: unreal.log(f"[A2] {s}")

SKEL = unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer_Skeleton")
DST = "/Game/Alice/AnimCoelho"
tools = unreal.AssetToolsHelpers.get_asset_tools()

# BlendSpace1D
try:
    f = unreal.BlendSpaceFactory1D()
    L("factory criada")
    try:
        f.set_editor_property("target_skeleton", SKEL)
        L("target_skeleton setado")
    except Exception as e:
        L(f"set target_skeleton ERR: {e}")
    bs = tools.create_asset("BS_CoelhoLoco", DST, unreal.BlendSpace1D, f)
    L(f"BS criado = {bs is not None}")
except Exception as e:
    L(f"BS FALHOU: {e}")
    bs = None

# tenta configurar samples com API correta
if bs:
    idle = unreal.load_asset(f"{DST}/C_Idle")
    walk = unreal.load_asset(f"{DST}/C_Walk")
    run  = unreal.load_asset(f"{DST}/C_Run")
    L(f"clips: idle={idle is not None} walk={walk is not None} run={run is not None}")
    # metodos disponiveis no blendspace
    methods = [m for m in dir(bs) if 'sample' in m.lower() or 'axis' in m.lower()]
    L(f"metodos BS: {methods}")
    unreal.EditorAssetLibrary.save_loaded_asset(bs, only_if_is_dirty=False)

# AnimBP
try:
    af = unreal.AnimBlueprintFactory()
    af.set_editor_property("target_skeleton", SKEL)
    abp = tools.create_asset("ABP_Coelho", DST, unreal.AnimBlueprint, af)
    L(f"ABP criado = {abp is not None}")
    if abp: unreal.EditorAssetLibrary.save_loaded_asset(abp, only_if_is_dirty=False)
except Exception as e:
    L(f"ABP FALHOU: {e}")

L("END")
