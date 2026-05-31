"""Confirma bones do SK_EveM_Skeleton (o que os clips A_* usam no UE)
e do SK_AliceVestido ja importado. Decide se casam."""
import unreal
L = lambda s: unreal.log(f"[CK] {s}")

skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
if skel:
    bt = skel.get_editor_property("bone_tree")
    L(f"SK_EveM_Skeleton bones = {len(bt)}")

# o SK_AliceVestido que importei (Eve donor)
sk = unreal.load_asset("/Game/Alice/Characters/AliceVestido/SK_AliceVestido")
if sk and sk.skeleton:
    L(f"SK_AliceVestido.skeleton = {sk.skeleton.get_name()}")
    bt2 = sk.skeleton.get_editor_property("bone_tree")
    L(f"SK_AliceVestido bones = {len(bt2)}")
    L(f"  mesmo skeleton dos anims? {sk.skeleton.get_name()=='SK_EveM_Skeleton'}")

# clips A_* usam qual skeleton?
for c in ("A_Idle","A_Walk","A_Run"):
    a = unreal.load_asset(f"/Game/Alice/AnimM/{c}")
    if a:
        s = a.get_skeleton()
        L(f"  {c}.skeleton = {s.get_name() if s else None}")
L("END")
