import unreal
sk = unreal.load_asset("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
eve = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
skl = sk.get_editor_property("skeleton") if sk else None
print("SK_AliceDressed.skeleton =", skl.get_name() if skl else None)
print("SK_EveM_Skeleton =", eve.get_name() if eve else None)
print("SAME_SKELETON =", skl == eve)
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
sma = mc.get_skeletal_mesh_asset()
print("BP_mesh =", sma.get_name() if sma else None)
print("BP_rot =", str(mc.get_editor_property("relative_rotation")))
print("BP_loc =", str(mc.get_editor_property("relative_location")))
for p in ["anim_idle", "anim_walk", "anim_run"]:
    try:
        v = cdo.get_editor_property(p)
        print(p, "=", v.get_name() if v else None)
    except Exception as e:
        print(p, "ERR", e)
print("DIAG_DONE")
