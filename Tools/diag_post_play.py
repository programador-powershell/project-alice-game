"""Diag tudo: skeleton corpo vs anims, vestido skel, DressMesh asset, BP mesh atual."""
import unreal
L = lambda s: unreal.log(f"[DP] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
body=mc.get_editor_property("skeletal_mesh_asset")
bskel=body.skeleton.get_name() if body and body.skeleton else "NULL"
bbones=len(body.skeleton.get_editor_property("bone_tree")) if body and body.skeleton else 0
L(f"BODY mesh={body.get_name() if body else None} skel={bskel} bones={bbones}")
L(f"  rot={mc.get_editor_property('relative_rotation')}")
L(f"  loc={mc.get_editor_property('relative_location')}")
L(f"  anim_mode={mc.get_editor_property('animation_mode')}")

dress_asset=cdo.get_editor_property("dress_mesh_asset")
if dress_asset:
    dskel=dress_asset.skeleton.get_name() if dress_asset.skeleton else "NULL"
    dbones=len(dress_asset.skeleton.get_editor_property("bone_tree")) if dress_asset.skeleton else 0
    L(f"DRESS asset={dress_asset.get_name()} skel={dskel} bones={dbones}")
else:
    L("DRESS asset=None")

for cn in ("A_Idle","A_Walk","A_Run","A_Atk1"):
    a=unreal.load_asset(f"/Game/Alice/AnimAlice/{cn}")
    if a:
        s=a.get_skeleton()
        L(f"  {cn} skel={s.get_name() if s else 'NULL'}")
    else:
        L(f"  {cn} MISS")

# Anim_Idle prop do BP aponta pra qual asset?
ai=cdo.get_editor_property("anim_idle")
L(f"BP.Anim_Idle = {ai.get_path_name() if ai else None}")
L("END")
