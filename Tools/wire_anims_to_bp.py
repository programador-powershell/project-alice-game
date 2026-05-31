"""Liga os 8 anims importados aos campos Anim_* do BP_Alice (CDO).
O AliceCharacter C++ usa esses no Tick (SingleNode PlayAnimation)."""
import unreal
L = lambda s: unreal.log(f"[W] {s}")

DST = "/Game/Alice/AnimAlice"
def A(n):
    p = f"{DST}/{n}"
    a = unreal.load_asset(p)
    return a

mapping = {
    "Anim_Idle":  "Alice_Idle",
    "Anim_Walk":  "Alice_Walk",
    "Anim_Run":   "Alice_Run",
    "Anim_Atk1":  "Alice_Atk1",
    "Anim_Atk2":  "Alice_Atk2",
    "Anim_Atk3":  "Alice_Atk3",
    "Anim_Attack":"Alice_Atk1",
    "Anim_Dodge": "Alice_Dodge",
    "Anim_Death": "Alice_Death",
}

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
ok=0
for prop, clip in mapping.items():
    a = A(clip)
    if not a:
        L(f"  {prop}: clip {clip} MISS"); continue
    try:
        cdo.set_editor_property(prop, a)
        L(f"  {prop} = {clip}  OK")
        ok+=1
    except Exception as e:
        L(f"  {prop}: ERR {e}")

unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L(f"SET {ok}/{len(mapping)}  BP salvo")

# confirma mesh + skeleton coerentes
mc = cdo.get_editor_property("mesh")
m = mc.get_editor_property("skeletal_mesh_asset")
L(f"mesh={m.get_name() if m else None} skel={m.skeleton.get_name() if m and m.skeleton else None}")
ia = A("Alice_Idle")
L(f"Alice_Idle.skeleton={ia.get_skeleton().get_name() if ia and ia.get_skeleton() else None}")
L("DONE — pode dar Play")
