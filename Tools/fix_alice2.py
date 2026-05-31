"""Fix definitivo BP_Alice:
1. mesh.skeletal_mesh_asset = SK_AliceDressed
2. mesh.relative_rotation = (0, -90, 0)
3. mesh.anim_class = primeiro ABP_* encontrado (se houver)
4. Save + compile
5. Listar ABP candidatos pra escolha posterior
6. Caçar de onde vem a ref SK_AliceReal pra limpar
"""
import unreal

BP_PATH = "/Game/Alice/Blueprints/BP_Alice"
SK_PATH = "/Game/Alice/Characters/AliceDressed/SK_AliceDressed"
L = lambda s: unreal.log(f"[fix] {s}")

bp = unreal.load_asset(BP_PATH)
sk = unreal.load_asset(SK_PATH)
L(f"BP={'OK' if bp else 'MISS'}  SK_AliceDressed={'OK' if sk else 'MISS'}")
if not bp:
    L("ABORT — BP_Alice não carrega"); raise SystemExit
if not sk:
    L("ABORT — SK_AliceDressed não existe"); raise SystemExit

cdo = unreal.get_default_object(bp.generated_class())
mc  = cdo.get_editor_property("mesh")

# 1. skeletal mesh
mc.set_editor_property("skeletal_mesh_asset", sk)
L(f"OK  mesh.skeletal_mesh_asset = SK_AliceDressed")

# 2. rotation (pitch=0 yaw=-90 — em pé + virada)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0.0, pitch=0.0, yaw=-90.0))
L("OK  mesh.relative_rotation = pitch=0 yaw=-90 roll=0")

# 3. AnimBP candidatos
L("--- caça ABP candidatos ---")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
abp_found = []
for d in ("/Game/Alice/AnimM","/Game/Alice/Animations","/Game/Alice/Blueprints",
          "/Game/Alice/Characters/AliceDressed","/Game/Alice/Characters"):
    for a in (ar.get_assets_by_path(d, recursive=True) or []):
        n = str(a.asset_name)
        if n.startswith("ABP_") or "AnimBlueprint" in str(a.asset_class_path.asset_name):
            full = str(a.package_name)
            abp_found.append(full)
            L(f"  candidato: {full}")
if abp_found:
    abp = unreal.load_asset(abp_found[0])
    if abp:
        mc.set_editor_property("anim_class", abp.generated_class())
        L(f"OK  mesh.anim_class = {abp_found[0]}")
else:
    L("⚠  Nenhum ABP_* encontrado — anim_class fica None")
    L("    (vai animar via PlayAnimMontage direto se C++ chamar)")

# 4. salvar
ok = unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L(f"save BP_Alice = {ok}")

# 5. caçar quem ainda referencia SK_AliceReal
L("--- caça refs órfãs a SK_AliceReal ---")
ORPHAN = "/Game/Alice/Characters/AliceReal/SK_AliceReal"
try:
    refs = ar.get_referencers(ORPHAN, unreal.AssetRegistryDependencyOptions(
        include_soft_package_references=True, include_hard_package_references=True))
    for r in (refs or []):
        L(f"  ref por: {r}")
except Exception as e:
    L(f"  err: {e}")

L("FIX END — re-rode diag_alice2.py pra confirmar")
