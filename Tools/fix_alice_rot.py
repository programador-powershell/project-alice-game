import unreal
EAL = unreal.EditorAssetLibrary
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
# upright + facing: yaw=-90, pitch=0, roll=0 (python Rotator arg order != C++ FRotator)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0.0, pitch=0.0, yaw=-90.0))
mc.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, -88.0))
print("rot now =", str(mc.get_editor_property("relative_rotation")))
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
print("FIX_ROT_DONE")
