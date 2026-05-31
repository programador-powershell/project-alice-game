"""Le os skin weights REAIS do SK_AliceOficial via render data.
MaxBoneInfluences e numero de bones usados = prova de skin.
Se influences>=1 e varios bones -> pesos OK (problema runtime).
Se tudo num bone so -> auto-weight falhou.
"""
import unreal
L = lambda s: unreal.log(f"[SW] {s}")

sk = unreal.load_asset("/Game/Alice/Characters/AliceOficial/SK_AliceOficial")
L(f"mesh = {sk.get_name() if sk else None}")

# tags do asset (UE expõe stats)
d = unreal.EditorAssetLibrary.find_asset_data(sk.get_path_name())
for tag in ("Vertices","Bones","MaxBoneInfluences","Triangles","NumLODs","UVChannels"):
    try:
        v = d.get_tag_value(tag)
        if v not in (None,""): L(f"  {tag} = {v}")
    except Exception: pass

# numero de bones do skeleton
if sk.skeleton:
    bt = sk.skeleton.get_editor_property("bone_tree")
    L(f"  skeleton bones = {len(bt)}")

# materiais
for i,m in enumerate(sk.materials):
    mi = m.material_interface
    L(f"  mat[{i}] = {mi.get_name() if mi else 'None'}")

# physics asset presente?
pa = sk.get_editor_property("physics_asset")
L(f"  physics_asset = {pa.get_name() if pa else None}")

L("END")
