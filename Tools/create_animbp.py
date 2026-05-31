"""Cria AnimBlueprint + BlendSpace1D de locomocao pro coelho (SK_CoelhoPlayer_Skeleton).
Parte 1: cria os ASSETS via Python (o que da pra automatizar).
Os nos do AnimGraph precisam de liga manual (Python nao edita AnimGraph) -> instrucoes depois.
"""
import unreal
L = lambda s: unreal.log(f"[AB] {s}")

SKEL_PATH = "/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer_Skeleton"
skel = unreal.load_asset(SKEL_PATH)
L(f"skeleton = {'OK' if skel else 'MISS'}")
if not skel: raise SystemExit

DST = "/Game/Alice/AnimCoelho"
tools = unreal.AssetToolsHelpers.get_asset_tools()

# 1. BlendSpace1D de locomocao (eixo Speed 0..600)
bs_factory = unreal.BlendSpaceFactory1D()
bs_factory.set_editor_property("target_skeleton", skel)
bs = tools.create_asset("BS_CoelhoLoco", DST, unreal.BlendSpace1D, bs_factory)
if bs:
    # configura eixo X = Speed
    bs.set_editor_property("axis_to_scale_animation", unreal.AnimationBlendSpaceAxis.BSA_X)
    # samples: idle(0), walk(150), run(550)
    idle = unreal.load_asset(f"{DST}/C_Idle")
    walk = unreal.load_asset(f"{DST}/C_Walk")
    run  = unreal.load_asset(f"{DST}/C_Run")
    try:
        bs.add_sample(idle, unreal.Vector(0,0,0))
        bs.add_sample(walk, unreal.Vector(150,0,0))
        bs.add_sample(run,  unreal.Vector(550,0,0))
        L("BS samples: idle@0 walk@150 run@550")
    except Exception as e:
        L(f"add_sample err (API): {e}")
    unreal.EditorAssetLibrary.save_loaded_asset(bs, only_if_is_dirty=False)
    L("BS_CoelhoLoco criado")
else:
    L("BS criacao falhou")

# 2. AnimBlueprint
abp_factory = unreal.AnimBlueprintFactory()
abp_factory.set_editor_property("target_skeleton", skel)
abp = tools.create_asset("ABP_Coelho", DST, unreal.AnimBlueprint, abp_factory)
if abp:
    unreal.EditorAssetLibrary.save_loaded_asset(abp, only_if_is_dirty=False)
    L(f"ABP_Coelho criado em {DST}/ABP_Coelho")
else:
    L("ABP criacao falhou")

L("PART1 DONE")
L(">>> Proximo: ligar BlendSpace no AnimGraph do ABP (manual, te guio)")
