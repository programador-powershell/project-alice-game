"""Wire final no BP_Alice depois do build C++ com DressMesh:
- mesh = SK_AliceBody
- DressMesh.SkeletalMesh = SK_AliceDress (Leader Pose feito no C++ BeginPlay)
- Anim_* = anims A_*
- compila + salva
"""
import unreal
L = lambda s: unreal.log(f"[W] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
body=unreal.load_asset("/Game/Alice/Characters/AliceBody/SK_AliceBody")
dress=unreal.load_asset("/Game/Alice/Characters/AliceDress2/SK_AliceDress")
L(f"bp={bp is not None} body={body is not None} dress={dress is not None}")
if not(bp and body and dress): L("ABORT"); raise SystemExit

cdo=unreal.get_default_object(bp.generated_class())
# mesh do corpo
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", body)
mc.set_editor_property("anim_class", None)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_rotation", unreal.Rotator(0,-90,0))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
L("corpo wired")

# DressMesh (criado no C++)
try:
    dm=cdo.get_editor_property("dress_mesh")
    if dm:
        dm.set_editor_property("skeletal_mesh_asset", dress)
        L(f"vestido wired (DressMesh.SkeletalMesh={dress.get_name()})")
    else:
        L("DressMesh property None — C++ talvez precise reabrir editor pra reconhecer")
except Exception as e:
    L(f"DressMesh err: {e}")

# anims
DSTA="/Game/Alice/AnimAlice"
mp={"Anim_Idle":"A_Idle","Anim_Walk":"A_Walk","Anim_Run":"A_Run","Anim_Atk1":"A_Atk1",
"Anim_Atk2":"A_Atk2","Anim_Atk3":"A_Atk3","Anim_Attack":"A_Atk1","Anim_Dodge":"A_Dodge","Anim_Death":"A_Death"}
nok=0
for prop,clip in mp.items():
    a=unreal.load_asset(f"{DSTA}/{clip}")
    if a:
        try: cdo.set_editor_property(prop,a); nok+=1
        except: pass
L(f"anims wired={nok}/9")

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP compilado+salvo")

# coerencia
idle=unreal.load_asset(f"{DSTA}/A_Idle")
L(f"COER body.skel={body.skeleton.get_name()} dress.skel={dress.skeleton.get_name() if dress.skeleton else 'NULL'} idle.skel={idle.get_skeleton().get_name() if idle and idle.get_skeleton() else 'NULL'}")
L("DONE")
