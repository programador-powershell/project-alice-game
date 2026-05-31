"""Assign per-dress stance clips to BP_Alice."""
import unreal
EAL = unreal.EditorAssetLibrary
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
m = {
    "anim_gs_idle": "A_GS_Idle", "anim_gs_run": "A_GS_Run", "anim_gs_atk": "A_GS_Atk",
    "anim_ss_idle": "A_SS_Idle", "anim_ss_atk": "A_SS_Atk", "anim_dual_atk": "A_Dual_Atk",
}
if bp:
    cdo = unreal.get_default_object(bp.generated_class())
    for slot, name in m.items():
        a = unreal.load_asset("/Game/Alice/AnimM/%s" % name)
        if isinstance(a, unreal.AnimSequence):
            try:
                cdo.set_editor_property(slot, a)
                print("WIREST", slot, "ok")
            except Exception as e:
                print("WIREST", slot, "FAIL", e)
        else:
            print("WIREST", slot, "missing")
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    except Exception as e:
        print("WIREST save", e)
print("WIREST DONE")
