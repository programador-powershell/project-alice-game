import unreal
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class()) if bp else None
if cdo:
    m = cdo.get_editor_property("mesh")
    sk = None
    try:
        sk = m.get_editor_property("skeletal_mesh_asset")
    except Exception:
        pass
    vm = cdo.get_editor_property("visual_mesh_asset")
    unreal.log("[Alice] CHECK skeletal=%s visual=%s scale=%s" % (
        sk.get_name() if sk else "None",
        vm.get_name() if vm else "None",
        cdo.get_editor_property("visual_mesh_scale")))
else:
    unreal.log("[Alice] CHECK no BP_Alice")
unreal.log("[Alice] CHECK DONE")
