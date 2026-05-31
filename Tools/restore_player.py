"""Player = on-theme static Alice mesh + procedural motion (skeletal Eve kept as a spare asset)."""
import unreal

EAL = unreal.EditorAssetLibrary
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
alice = unreal.load_asset("/Game/Alice/Characters/SM_Alice_3D/StaticMeshes/SM_Alice_3D")

if not bp:
    unreal.log_warning("[Alice] RESTORE: no BP_Alice")
else:
    cdo = unreal.get_default_object(bp.generated_class())
    try:
        cdo.get_editor_property("mesh").set_skeletal_mesh_asset(None)
    except Exception as e:
        unreal.log_warning("[Alice] RESTORE mesh-none: %s" % e)
    if alice:
        cdo.set_editor_property("visual_mesh_asset", alice)
        cdo.set_editor_property("visual_mesh_scale", 1.79)
        unreal.log("[Alice] RESTORE set static Alice visual")
    else:
        unreal.log_warning("[Alice] RESTORE missing Alice static mesh")
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    except Exception as e:
        unreal.log_warning("[Alice] RESTORE save: %s" % e)
    unreal.log("[Alice] RESTORE DONE")
