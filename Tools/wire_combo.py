"""Assign combo + block clips to BP_Alice's new slots."""
import unreal
EAL = unreal.EditorAssetLibrary
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
m = {"anim_atk1": "A_Atk1", "anim_atk2": "A_Atk2", "anim_atk3": "A_Atk3",
     "anim_block": "A_Block", "anim_parry": "A_Parry"}
if bp:
    cdo = unreal.get_default_object(bp.generated_class())
    for slot, name in m.items():
        a = unreal.load_asset("/Game/Alice/AnimM/%s" % name)
        if isinstance(a, unreal.AnimSequence):
            try:
                cdo.set_editor_property(slot, a)
                print("WIRECMB", slot, "ok")
            except Exception as e:
                print("WIRECMB", slot, "FAIL", e)
        else:
            print("WIRECMB", slot, "missing/not-anim")
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    except Exception as e:
        print("WIRECMB save", e)
print("WIRECMB DONE")
