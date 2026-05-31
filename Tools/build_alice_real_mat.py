"""Rebuild M_AliceDress = real 4K PBR (base x per-dress tint + normal + metallic/roughness)
+ keep the C++-driven magic: Fresnel rim emissive (pulsing) + dissolve mask w/ edge glow.
Param names match AAliceCharacter: BaseTint, EmissiveColor, EmissivePower, DissolveAmount."""
import unreal
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
MP = unreal.MaterialProperty
MATDIR = "/Game/Alice/Materials"; PATH = MATDIR + "/M_AliceDress"

base = unreal.load_asset("/Game/Alice/Textures/Alice/T_Alice_Base")
norm = unreal.load_asset("/Game/Alice/Textures/Alice/T_Alice_Normal")
mr   = unreal.load_asset("/Game/Alice/Textures/Alice/T_Alice_MR")
print("TEX", base is not None, norm is not None, mr is not None)

if EAL.does_asset_exist(PATH):
    EAL.delete_asset(PATH)
mat = AT.create_asset("M_AliceDress", MATDIR, unreal.Material, unreal.MaterialFactoryNew())
mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
mat.set_editor_property("opacity_mask_clip_value", 0.0)
mat.set_editor_property("two_sided", True)

def ex(cls, x, y): return MEL.create_material_expression(mat, cls, x, y)
def C(a, ao, b, bi):
    try: return MEL.connect_material_expressions(a, ao, b, bi)
    except Exception as e: print("C FAIL", ao, bi, e); return False
def P(e, o, p):
    try: return MEL.connect_material_property(e, o, p)
    except Exception as e: print("P FAIL", p, e); return False
def tex(t, stype, x, y):
    n = ex(unreal.MaterialExpressionTextureSample, x, y)
    if t: n.set_editor_property("texture", t)
    n.set_editor_property("sampler_type", stype)
    return n
def vec(name, r, g, b, x, y):
    e = ex(unreal.MaterialExpressionVectorParameter, x, y)
    e.set_editor_property("parameter_name", name); e.set_editor_property("default_value", unreal.LinearColor(r,g,b,1)); return e
def scal(name, v, x, y):
    e = ex(unreal.MaterialExpressionScalarParameter, x, y)
    e.set_editor_property("parameter_name", name); e.set_editor_property("default_value", v); return e

ST = unreal.MaterialSamplerType
# ---- BaseColor = Base * BaseTint ----
tb = tex(base, ST.SAMPLERTYPE_COLOR, -900, -260)
tint = vec("BaseTint", 1.0, 1.0, 1.0, -900, -60)
bmul = ex(unreal.MaterialExpressionMultiply, -650, -200)
C(tb, "RGB", bmul, "A"); C(tint, "", bmul, "B")
P(bmul, "", MP.MP_BASE_COLOR)
# ---- Normal ----
tn = tex(norm, ST.SAMPLERTYPE_NORMAL, -650, 120)
P(tn, "RGB", MP.MP_NORMAL)
# ---- Metallic (B) / Roughness (G) from MR ----
tmr = tex(mr, ST.SAMPLERTYPE_MASKS, -650, 360)
P(tmr, "B", MP.MP_METALLIC)
P(tmr, "G", MP.MP_ROUGHNESS)
# ---- Pulse = 0.8 + 0.2*sin(Time*PulseSpeed) ----
tnode = ex(unreal.MaterialExpressionTime, -1300, 640)
pspd = scal("PulseSpeed", 3.0, -1300, 760)
tmul = ex(unreal.MaterialExpressionMultiply, -1130, 660); C(tnode, "", tmul, "A"); C(pspd, "", tmul, "B")
sine = ex(unreal.MaterialExpressionSine, -980, 660); C(tmul, "", sine, "")
pamp = ex(unreal.MaterialExpressionMultiply, -820, 660); pac = ex(unreal.MaterialExpressionConstant, -960, 740); pac.set_editor_property("r", 0.2)
C(sine, "", pamp, "A"); C(pac, "", pamp, "B")
pulse = ex(unreal.MaterialExpressionAdd, -660, 660); pbc = ex(unreal.MaterialExpressionConstant, -820, 740); pbc.set_editor_property("r", 0.8)
C(pamp, "", pulse, "A"); C(pbc, "", pulse, "B")
# ---- Rim = Fresnel * EmissivePower * pulse ; emRim = EmissiveColor * Rim ----
fres = ex(unreal.MaterialExpressionFresnel, -900, 440); fres.set_editor_property("exponent", 4.0); fres.set_editor_property("base_reflect_fraction", 0.04)
epow = scal("EmissivePower", 1.6, -900, 360)
rim1 = ex(unreal.MaterialExpressionMultiply, -700, 430); C(fres, "", rim1, "A"); C(epow, "", rim1, "B")
rim = ex(unreal.MaterialExpressionMultiply, -540, 500); C(rim1, "", rim, "A"); C(pulse, "", rim, "B")
ecol = vec("EmissiveColor", 1.0, 0.3, 0.6, -540, 330)
emRim = ex(unreal.MaterialExpressionMultiply, -340, 380); C(ecol, "", emRim, "A"); C(rim, "", emRim, "B")
# ---- Dissolve: saturate(noise*0.5+0.5) - DissolveAmount + 0.02 -> OpacityMask ----
noise = ex(unreal.MaterialExpressionNoise, -1560, 980); noise.set_editor_property("scale", 2.5)
nh = ex(unreal.MaterialExpressionMultiply, -1380, 980); nhc = ex(unreal.MaterialExpressionConstant, -1520, 1060); nhc.set_editor_property("r", 0.5)
C(noise, "", nh, "A"); C(nhc, "", nh, "B")
nc = ex(unreal.MaterialExpressionAdd, -1220, 980); ncc = ex(unreal.MaterialExpressionConstant, -1360, 1060); ncc.set_editor_property("r", 0.5)
C(nh, "", nc, "A"); C(ncc, "", nc, "B")
n01 = ex(unreal.MaterialExpressionSaturate, -1070, 980); C(nc, "", n01, "")
diss = scal("DissolveAmount", 0.0, -1300, 1120)
sub = ex(unreal.MaterialExpressionSubtract, -900, 980); C(n01, "", sub, "A"); C(diss, "", sub, "B")
maskV = ex(unreal.MaterialExpressionAdd, -740, 980); bc = ex(unreal.MaterialExpressionConstant, -880, 1060); bc.set_editor_property("r", 0.02)
C(sub, "", maskV, "A"); C(bc, "", maskV, "B")
P(maskV, "", MP.MP_OPACITY_MASK)
# ---- edge glow ----
absE = ex(unreal.MaterialExpressionAbs, -860, 1180); C(maskV, "", absE, "")
shp = ex(unreal.MaterialExpressionMultiply, -700, 1180); shc = ex(unreal.MaterialExpressionConstant, -840, 1260); shc.set_editor_property("r", 9.0)
C(absE, "", shp, "A"); C(shc, "", shp, "B")
sat = ex(unreal.MaterialExpressionSaturate, -560, 1180); C(shp, "", sat, "")
om = ex(unreal.MaterialExpressionOneMinus, -420, 1180); C(sat, "", om, "")
eg = scal("EdgeGlow", 6.0, -560, 1280)
es = ex(unreal.MaterialExpressionMultiply, -260, 1200); C(om, "", es, "A"); C(eg, "", es, "B")
emEdge = ex(unreal.MaterialExpressionMultiply, -120, 1140); C(ecol, "", emEdge, "A"); C(es, "", emEdge, "B")
# ---- Emissive = emRim + emEdge ----
emSum = ex(unreal.MaterialExpressionAdd, 80, 600); C(emRim, "", emSum, "A"); C(emEdge, "", emSum, "B")
P(emSum, "", MP.MP_EMISSIVE_COLOR)

MEL.recompile_material(mat); EAL.save_asset(PATH)
print("M_AliceDress rebuilt with PBR textures")

# apply to SK_AliceReal slots (editor visual; runtime InitDressMID also forces it)
sk = unreal.load_asset("/Game/Alice/Characters/AliceReal/SK_AliceReal")
M = unreal.load_asset(PATH)
if sk and M:
    try:
        mats = sk.get_editor_property("materials")
        for sm in mats: sm.set_editor_property("material_interface", M)
        sk.set_editor_property("materials", mats)
        EAL.save_asset("/Game/Alice/Characters/AliceReal/SK_AliceReal")
        print("applied to SK_AliceReal slots", len(mats))
    except Exception as e: print("apply err", e)
print("ALICE_MAT_DONE")
