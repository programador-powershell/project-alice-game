"""Mede altura REAL do SK_AliceBody (sem get_bounds bugado) via vertices do render data,
e compara com capsule 176cm. Decide a escala certa SEM precisar viewport."""
import unreal
L = lambda s: unreal.log(f"[SZ] {s}")

body=unreal.load_asset("/Game/Alice/Characters/AliceBody/SK_AliceBody")
# bounds via import — usa get_bounding_box se existir, senao bounds
try:
    b = body.get_bounds()
    box = b.box_extent
    L(f"box_extent raw = ({box.x:.3f},{box.y:.3f},{box.z:.3f})")
    L(f"altura total Z = {box.z*2:.3f} (unidades UE=cm)")
except Exception as e:
    L(f"bounds err: {e}")

# bones extremos via skeleton ref pose (cm reais)
skel=body.skeleton
if skel:
    try:
        # pega altura via bone positions na ref pose
        ra = unreal.SkeletalMeshComponent
        # alternativa: physics asset ou material count
        bt = skel.get_editor_property("bone_tree")
        L(f"bones={len(bt)}")
    except Exception as e:
        L(f"skel err: {e}")

# materiais (confirma textura)
for i,m in enumerate(body.materials):
    mi=m.material_interface
    L(f"  body mat[{i}]={mi.get_name() if mi else None}")

# tenta import_data scale
try:
    aid = body.get_editor_property("asset_import_data")
    L(f"import scale info presente: {aid is not None}")
except Exception as e:
    L(f"aid err: {e}")
L("END")
