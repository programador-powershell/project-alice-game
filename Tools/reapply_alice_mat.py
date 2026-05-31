"""Reapply Alice's original material (from her GLB static import) onto the player mesh."""
import unreal
EAL = unreal.EditorAssetLibrary
src = unreal.load_asset("/Game/Alice/Characters/SM_Alice_3D/StaticMeshes/SM_Alice_3D")
mat = src.get_material(0) if src else None
print("REMAT src_mat=%s" % (mat.get_name() if mat else "None"))
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
if bp and mat:
    cdo = unreal.get_default_object(bp.generated_class())
    mc = cdo.get_editor_property("mesh")
    try:
        for i in range(max(1, mc.get_num_materials())):
            mc.set_material(i, mat)
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
        print("REMAT applied to %d slots" % mc.get_num_materials())
    except Exception as e:
        print("REMAT fail", e)
print("REMAT DONE")
