import unreal
EAL = unreal.EditorAssetLibrary
sk = unreal.load_asset("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
M = unreal.load_asset("/Game/Alice/Materials/M_AliceDress")
print("sk", sk is not None, "M", M is not None)
# apply material to all slots
if sk and M:
    mats = sk.get_editor_property("materials")
    for smat in mats: smat.set_editor_property("material_interface", M)
    sk.set_editor_property("materials", mats)
    EAL.save_asset("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
    print("applied M_AliceDress to", len(mats), "slots")
# wire player BP
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
if bp and sk:
    cdo = unreal.get_default_object(bp.generated_class())
    mc = cdo.get_editor_property("mesh")
    mc.set_skeletal_mesh_asset(sk)
    mc.set_editor_property("relative_scale3d", unreal.Vector(1.0,1.0,1.0))
    mc.set_editor_property("relative_location", unreal.Vector(0.0,0.0,-88.0))
    mc.set_editor_property("relative_rotation", unreal.Rotator(0.0,-90.0,0.0))
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    print("WIRED player = SK_AliceDressed")
print("WIRE_DRESSED_DONE")
