"""Diagnostica qual pawn class o GameMode spawna no Play, e bone count de SK_AliceDressed."""
import unreal
L = lambda s: unreal.log(f"[gm] {s}")

# 1. GameMode + DefaultPawnClass
gm_bp = unreal.load_asset("/Game/Alice/Blueprints/BP_AliceGameMode")
if gm_bp:
    cdo = unreal.get_default_object(gm_bp.generated_class())
    dpc = cdo.get_editor_property("default_pawn_class")
    L(f"BP_AliceGameMode.default_pawn_class = {dpc.get_path_name() if dpc else 'None'}")
    L(f"  is BP_Alice? {'YES' if dpc and 'BP_Alice' in dpc.get_path_name() else 'NO ❌'}")
else:
    L("BP_AliceGameMode não carrega")

# 2. SK_AliceDressed — bone count e vertex skinning
sk = unreal.load_asset("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
if sk:
    skel = sk.skeleton
    if skel:
        bones = skel.get_editor_property("reference_skeleton") if hasattr(skel,'get_editor_property') else None
        # API alternativa:
        try:
            ref = skel.get_reference_pose()
            L(f"SK_AliceDressed reference_pose bones = {len(ref) if ref else '?'}")
        except Exception:
            pass
        # SkeletalMesh bone names
        try:
            bones = sk.get_editor_property("ref_skeleton")
        except Exception:
            pass
    # Vertex count
    try:
        info = sk.get_editor_property("imported_model")
        L(f"SK_AliceDressed imported_model = {info}")
    except Exception as e:
        L(f"  imported_model err: {e}")
    # PhysicsAsset
    pa = sk.get_editor_property("physics_asset") if hasattr(sk,'get_editor_property') else None
    L(f"  physics_asset = {pa.get_name() if pa else 'None'}")

# 3. Hierarquia de classes do BP_Alice
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
if bp:
    gc = bp.generated_class()
    parent = gc.get_super_class()
    L(f"BP_Alice parent class = {parent.get_name()}")

# 4. CDO de AliceCharacter (C++ direto) — mesh seteado?
ac_class = unreal.load_class(None, "/Script/Alice.AliceCharacter")
if ac_class:
    ac_cdo = unreal.get_default_object(ac_class)
    if ac_cdo:
        m = ac_cdo.get_editor_property("mesh")
        sm = m.get_editor_property("skeletal_mesh_asset") if m else None
        L(f"AliceCharacter (C++).mesh.skeletal = {sm.get_path_name() if sm else 'None (esperado — C++ é vazio)'}")

L("END")
