import unreal
EAL = unreal.EditorAssetLibrary
sk = unreal.load_asset("/Game/Alice/Characters/AliceReal/SK_AliceReal")
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
print("SK", sk is not None, "BP", bp is not None)
if sk and bp:
    cdo = unreal.get_default_object(bp.generated_class())
    mc = cdo.get_editor_property("mesh")
    mc.set_skeletal_mesh_asset(sk)
    mc.set_editor_property("relative_scale3d", unreal.Vector(1.0, 1.0, 1.0))   # 1.7m -> 170uu native
    mc.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, -88.0))
    mc.set_editor_property("relative_rotation", unreal.Rotator(0.0, -90.0, 0.0))
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    print("WIRED player mesh = SK_AliceReal")
print("WIRE_ALICE_DONE")
