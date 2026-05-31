"""Mesh nativo JA e tamanho humano (test x1 confirmou). Reverte player scale=1.
Remove test actors do L_Arena."""
import unreal
L = lambda s: unreal.log(f"[R1] {s}")

# revert BP scale
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("relative_scale3d", unreal.Vector(1,1,1))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("player mesh scale=1 (revertido)")

# remove test actors
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
n=0
for a in eas.get_all_level_actors():
    if a.get_actor_label().startswith("TestSize") or a.get_actor_label()=="TestAliceAnim":
        eas.destroy_actor(a); n+=1
unreal.EditorLoadingAndSavingUtils.save_current_level()
L(f"test actors removidos={n}")
L("END")
