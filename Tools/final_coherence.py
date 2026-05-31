import unreal
L = lambda s: unreal.log(f"[FC] {s}")
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
m = mc.get_editor_property("skeletal_mesh_asset")
mesh_skel = m.skeleton.get_name() if m and m.skeleton else None
L(f"mesh = {m.get_name() if m else None}")
L(f"mesh.skeleton = {mesh_skel}")
ia = unreal.load_asset("/Game/Alice/AnimAlice/Alice_Idle")
anim_skel = ia.get_skeleton().get_name() if ia and ia.get_skeleton() else None
L(f"Alice_Idle.skeleton = {anim_skel}")
L(f">>> COERENTE? {mesh_skel == anim_skel}")
L(f"rot = {mc.get_editor_property('relative_rotation')}")
L("END")
