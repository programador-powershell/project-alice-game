"""Causa do 'estatua desliza': Anim_* nulos no spawn -> C++ cai no fallback procedural.
Fix: seta mesh+anims no CDO, COMPILA o blueprint, salva, e LE de volta do
generated_class default pra confirmar que persistiu (o que o PIE vai usar).
"""
import unreal
L = lambda s: unreal.log(f"[FX] {s}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())

# mesh = coelho
sk = unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer")
mc = cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", sk)
mc.set_editor_property("anim_class", None)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))

# anims
DST="/Game/Alice/AnimCoelho"
def A(n): return unreal.load_asset(f"{DST}/{n}")
mp = {"Anim_Idle":"C_Idle","Anim_Walk":"C_Walk","Anim_Run":"C_Run",
      "Anim_Atk1":"C_Atk1","Anim_Atk2":"C_Atk2","Anim_Atk3":"C_Atk3",
      "Anim_Attack":"C_Atk1","Anim_Dodge":"C_Dodge","Anim_Hit":"C_Death",
      "Anim_Death":"C_Death"}
setn=0
for prop,clip in mp.items():
    a=A(clip)
    if a:
        try: cdo.set_editor_property(prop,a); setn+=1
        except Exception as e: L(f"  {prop} err {e}")
L(f"anims setados no CDO: {setn}")

# COMPILA + salva (essencial pra PIE pegar)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("blueprint COMPILADO + salvo")

# LE de volta do generated_class (o que PIE usa)
gc = bp.generated_class()
cdo2 = unreal.get_default_object(gc)
L("--- verificacao pos-compile (valores que o PIE vera) ---")
for prop in ("Anim_Idle","Anim_Walk","Anim_Run","Anim_Atk1","Anim_Dodge"):
    v = cdo2.get_editor_property(prop)
    L(f"  {prop} = {v.get_name() if v else 'None ❌'}")
m2 = cdo2.get_editor_property("mesh").get_editor_property("skeletal_mesh_asset")
L(f"  mesh = {m2.get_name() if m2 else None}")
L(f"  animation_mode = {cdo2.get_editor_property('mesh').get_editor_property('animation_mode')}")
L("END")
