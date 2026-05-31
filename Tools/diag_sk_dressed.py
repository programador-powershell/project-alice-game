"""Diagnostica SK_AliceDressed em profundidade: bones, vertex count, skin weights."""
import unreal
L = lambda s: unreal.log(f"[sk] {s}")

sk = unreal.load_asset("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
L(f"asset={sk}")
if not sk: raise SystemExit

# skeleton
skel = sk.skeleton
L(f"skeleton ref = {skel.get_path_name() if skel else None}")

# bones — varias APIs possiveis
try:
    names = sk.get_editor_property("bone_tree") if hasattr(sk,"get_editor_property") else None
    L(f"sk.bone_tree count = {len(names) if names else '?'}")
except Exception as e: L(f"  bone_tree err: {e}")

try:
    info = unreal.EditorAssetLibrary.find_asset_data(sk.get_path_name())
    L(f"asset tags:")
    for k,v in (info.get_tag_values_dict() or {}).items():
        if any(t in k.lower() for t in ("bones","vert","tri","skin","weight","mat","lod")):
            L(f"  {k}={v}")
except Exception as e: L(f"  tags err: {e}")

# skeleton bones via referência
try:
    s_bones = []
    n = skel.get_editor_property('animation_retarget_sources') if skel else None
    # tenta via API correta
    rs = unreal.SkeletalMeshSubsystem
except Exception: pass

# Tenta API alternativa: editor properties
L("--- editor_property keys do skeleton ---")
try:
    for prop in ("bone_tree","virtual_bones","blend_profiles","slot_group_container"):
        v = skel.get_editor_property(prop) if skel else None
        L(f"  skeleton.{prop} = type={type(v).__name__}  len={len(v) if hasattr(v,'__len__') else '?'}")
except Exception as e: L(f"err: {e}")

# Mesh vertex/tri count
try:
    L(f"sk.num_bones (attribute?) = {getattr(sk,'num_bones','?')}")
    L(f"sk.materials count = {len(sk.materials) if hasattr(sk,'materials') else '?'}")
except: pass

# LODs
try:
    lods = sk.get_editor_property("lod_info")
    L(f"sk.lod_info count = {len(lods) if lods else '?'}")
except Exception as e: L(f"  lod err: {e}")

L("END")
