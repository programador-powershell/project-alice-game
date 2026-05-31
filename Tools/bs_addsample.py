"""Adiciona samples ao BS_CoelhoLoco testando assinaturas de BlendSpaceLibrary.add_sample."""
import unreal
L = lambda s: unreal.log(f"[AS] {s}")

DST = "/Game/Alice/AnimCoelho"
bs = unreal.load_asset(f"{DST}/BS_CoelhoLoco")
idle = unreal.load_asset(f"{DST}/C_Idle")
walk = unreal.load_asset(f"{DST}/C_Walk")
run  = unreal.load_asset(f"{DST}/C_Run")
L(f"bs={bs is not None} idle={idle is not None}")

# help da assinatura
import inspect
try:
    L(f"add_sample doc: {unreal.BlendSpaceLibrary.add_sample.__doc__}")
except Exception as e:
    L(f"doc err {e}")

# tenta variações de assinatura
attempts = [
    ("v1 (bs,anim,vec)", lambda: unreal.BlendSpaceLibrary.add_sample(bs, idle, unreal.Vector(0,0,0))),
    ("v2 kw", lambda: unreal.BlendSpaceLibrary.add_sample(blend_space=bs, animation_sequence=idle, sample_value=unreal.Vector(0,0,0))),
]
for name, fn in attempts:
    try:
        r = fn()
        L(f"{name} OK -> {r}")
        break
    except Exception as e:
        L(f"{name} ERR: {e}")
L("END")
