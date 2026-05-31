import unreal
L=lambda s:unreal.log(f"[W] {s}")
DSTA="/Game/Alice/AnimAlice"
body=unreal.load_asset("/Game/Alice/Characters/AliceFull/SK_AliceFull")
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", body)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_scale3d", unreal.Vector(1,1,1))
cdo.set_editor_property("dress_mesh_asset", None)

def find(*keys):
    for k in keys:
        a=unreal.load_asset(f"{DSTA}/A_{k}")
        if a: return a
    return None
mp={
 "anim_idle": find("Standing_Idle"),
 "anim_walk": find("Walking"),
 "anim_run": find("Fast_Run","Slow_Run","Injured_Run"),
 "anim_atk1": find("Standing_Melee_Attack_Horizontal"),
 "anim_atk2": find("Standing_Melee_Attack_Backhand"),
 "anim_atk3": find("Standing_Melee_Attack_Downward"),
 "anim_attack": find("Standing_Melee_Combo_Attack_Ver__2","One_Hand_Sword_Combo"),
 "anim_dodge": find("Sprinting_Forward_Roll"),
 "anim_death": find("Standing_React_Death_Forward"),
}
nw=0
for prop,a in mp.items():
    if a:
        try: cdo.set_editor_property(prop,a); nw+=1; L(f"  {prop}={a.get_name()}")
        except Exception as e: L(f"  {prop} ERR {e}")
    else: L(f"  {prop}=NAO ACHOU")
L(f"wired={nw}")
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
# coerencia
idle=mp["anim_idle"]
L(f"COER mesh.skel={body.skeleton.get_name()} idle.skel={idle.get_skeleton().get_name() if idle and idle.get_skeleton() else 'NULL'}")
L("END")
