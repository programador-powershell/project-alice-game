"""Build M_AliceDress: magic dress master material (headless).
Layers: BaseColor = VertexColor * BaseTint (per-dress, set from C++ via MID).
        Emissive = rim(Fresnel)*pulse + dissolve-edge glow  (EmissiveColor param).
        OpacityMask = Noise - DissolveAmount  (Masked, clip 0) -> dissolve on skill.
Then apply to SK_Alice (all slots) + BP_Alice mesh component, save.
Params driven from C++: BaseTint(Vec), EmissiveColor(Vec), EmissivePower(Scalar),
                        DissolveAmount(Scalar 0..1), PulseSpeed(Scalar)."""
import unreal

AT  = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
MATDIR = "/Game/Alice/Materials"
PATH = MATDIR + "/M_AliceDress"

if EAL.does_asset_exist(PATH):
    EAL.delete_asset(PATH)

mat = AT.create_asset("M_AliceDress", MATDIR, unreal.Material, unreal.MaterialFactoryNew())
mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
mat.set_editor_property("opacity_mask_clip_value", 0.0)
mat.set_editor_property("two_sided", True)

def expr(cls, x, y):
    return MEL.create_material_expression(mat, cls, x, y)

def vec(name, r, g, b, x, y):
    e = expr(unreal.MaterialExpressionVectorParameter, x, y)
    e.set_editor_property("parameter_name", name)
    e.set_editor_property("default_value", unreal.LinearColor(r, g, b, 1.0))
    return e

def scal(name, v, x, y):
    e = expr(unreal.MaterialExpressionScalarParameter, x, y)
    e.set_editor_property("parameter_name", name)
    e.set_editor_property("default_value", v)
    return e

report = []
def C(a, ao, b, bi):
    try:
        ok = MEL.connect_material_expressions(a, ao, b, bi)
        report.append("C %s->%s = %s" % (ao or "out", bi, ok)); return ok
    except Exception as ex:
        report.append("C FAIL %s->%s %s" % (ao, bi, ex)); return False

def P(e, o, prop):
    try:
        ok = MEL.connect_material_property(e, o, prop)
        report.append("P ->%s = %s" % (prop, ok)); return ok
    except Exception as ex:
        report.append("P FAIL %s %s" % (prop, ex)); return False

MP = unreal.MaterialProperty

# ---- BaseColor = BaseTint (per-dress hue; driven by C++ per dress) ----
# (Live Blender confirmed the mesh vertex colors are a grayscale AO bake, not painted
#  hue — so color comes from the per-dress tint param; AO overlay deferred.)
tint  = vec("BaseTint", 0.85, 0.45, 0.62, -900, 0)
P(tint, "", MP.MP_BASE_COLOR)

# ---- Roughness / Metallic (cloth) ----
rough = scal("Roughness", 0.55, -650, 60)
P(rough, "", MP.MP_ROUGHNESS)

# ---- Pulse = 0.8 + 0.2*sin(Time*PulseSpeed) ----
tnode = expr(unreal.MaterialExpressionTime, -1300, 360)
pspd  = scal("PulseSpeed", 3.0, -1300, 480)
tmul  = expr(unreal.MaterialExpressionMultiply, -1120, 380)
C(tnode, "", tmul, "A"); C(pspd, "", tmul, "B")
sine  = expr(unreal.MaterialExpressionSine, -960, 380)
C(tmul, "", sine, "")
pamp  = expr(unreal.MaterialExpressionMultiply, -800, 380)
pampC = expr(unreal.MaterialExpressionConstant, -940, 470); pampC.set_editor_property("r", 0.2)
C(sine, "", pamp, "A"); C(pampC, "", pamp, "B")
pulse = expr(unreal.MaterialExpressionAdd, -640, 380)
pbase = expr(unreal.MaterialExpressionConstant, -800, 470); pbase.set_editor_property("r", 0.8)
C(pamp, "", pulse, "A"); C(pbase, "", pulse, "B")   # pulse scalar 0.6..1.0

# ---- Rim = Fresnel * EmissivePower * pulse ----
fres  = expr(unreal.MaterialExpressionFresnel, -900, 220)
fres.set_editor_property("exponent", 4.0)
fres.set_editor_property("base_reflect_fraction", 0.04)
epow  = scal("EmissivePower", 2.5, -900, 140)
rim1  = expr(unreal.MaterialExpressionMultiply, -700, 200)
C(fres, "", rim1, "A"); C(epow, "", rim1, "B")
rim   = expr(unreal.MaterialExpressionMultiply, -520, 260)
C(rim1, "", rim, "A"); C(pulse, "", rim, "B")        # rim scalar

ecol  = vec("EmissiveColor", 1.0, 0.2, 0.55, -520, 120)
emRim = expr(unreal.MaterialExpressionMultiply, -320, 180)
C(ecol, "", emRim, "A"); C(rim, "", emRim, "B")      # rim glow color

# ---- Dissolve: remap noise to [0,1], then (noise01 - DissolveAmount + floor) -> OpacityMask
#      floor 0.02 guarantees fully-solid at rest (DissolveAmount=0); holes only as it rises.
noise = expr(unreal.MaterialExpressionNoise, -1560, 700)
noise.set_editor_property("scale", 2.5)
nh   = expr(unreal.MaterialExpressionMultiply, -1380, 700)
nhC  = expr(unreal.MaterialExpressionConstant, -1520, 800); nhC.set_editor_property("r", 0.5)
C(noise, "", nh, "A"); C(nhC, "", nh, "B")
nc   = expr(unreal.MaterialExpressionAdd, -1220, 700)
ncC  = expr(unreal.MaterialExpressionConstant, -1360, 800); ncC.set_editor_property("r", 0.5)
C(nh, "", nc, "A"); C(ncC, "", nc, "B")
n01  = expr(unreal.MaterialExpressionSaturate, -1070, 700)
C(nc, "", n01, "")                              # n01 in [0,1]
diss = scal("DissolveAmount", 0.0, -1300, 920)
sub  = expr(unreal.MaterialExpressionSubtract, -900, 700)
C(n01, "", sub, "A"); C(diss, "", sub, "B")
maskV= expr(unreal.MaterialExpressionAdd, -740, 700)
biasC= expr(unreal.MaterialExpressionConstant, -880, 800); biasC.set_editor_property("r", 0.02)
C(sub, "", maskV, "A"); C(biasC, "", maskV, "B")
P(maskV, "", MP.MP_OPACITY_MASK)

# ---- Dissolve edge glow = (1 - saturate(abs(noise-diss)*Sharp)) * EmissiveColor * EdgeGlow ----
absE  = expr(unreal.MaterialExpressionAbs, -860, 740)
C(maskV, "", absE, "")
sharp = expr(unreal.MaterialExpressionMultiply, -700, 740)
sharpC= expr(unreal.MaterialExpressionConstant, -840, 840); sharpC.set_editor_property("r", 9.0)
C(absE, "", sharp, "A"); C(sharpC, "", sharp, "B")
sat   = expr(unreal.MaterialExpressionSaturate, -560, 740)
C(sharp, "", sat, "")
omEdge= expr(unreal.MaterialExpressionOneMinus, -420, 740)
C(sat, "", omEdge, "")
edgeG = scal("EdgeGlow", 6.0, -560, 860)
edgeS = expr(unreal.MaterialExpressionMultiply, -260, 760)
C(omEdge, "", edgeS, "A"); C(edgeG, "", edgeS, "B")
emEdge= expr(unreal.MaterialExpressionMultiply, -120, 700)
C(ecol, "", emEdge, "A"); C(edgeS, "", emEdge, "B")

# ---- Emissive = emRim + emEdge ----
emSum = expr(unreal.MaterialExpressionAdd, 80, 300)
C(emRim, "", emSum, "A"); C(emEdge, "", emSum, "B")
P(emSum, "", MP.MP_EMISSIVE_COLOR)

MEL.recompile_material(mat)
EAL.save_asset(PATH)
print("DRESSMAT built %s" % PATH)

# ---- Apply to SK_Alice (all slots) ----
M = unreal.load_asset(PATH)
sk = unreal.load_asset("/Game/Alice/Characters/AliceRig/SK_Alice")
if sk and M:
    try:
        mats = sk.get_editor_property("materials")
        for sm in mats:
            sm.set_editor_property("material_interface", M)
        sk.set_editor_property("materials", mats)
        EAL.save_asset("/Game/Alice/Characters/AliceRig/SK_Alice")
        print("DRESSMAT applied to SK_Alice %d slots" % len(mats))
    except Exception as ex:
        print("DRESSMAT sk apply fail", ex)

# ---- Apply to BP_Alice mesh component CDO ----
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
if bp and M:
    try:
        cdo = unreal.get_default_object(bp.generated_class())
        mc = cdo.get_editor_property("mesh")
        n = max(1, mc.get_num_materials())
        for i in range(n):
            mc.set_material(i, M)
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
        print("DRESSMAT applied to BP_Alice %d slots" % n)
    except Exception as ex:
        print("DRESSMAT bp apply fail", ex)

with open(r"E:\Alice\dress_build_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("DRESSMAT DONE")
