"""Diagnóstico robusto do BP_Alice: lista mesh em cada componente + todas as refs SOFT/HARD."""
import unreal

BP_PATH = "/Game/Alice/Blueprints/BP_Alice"
L = lambda s: unreal.log(f"[diag] {s}")

def safe(cdo, name):
    try: return cdo.get_editor_property(name)
    except Exception as e: return f"<err:{e.__class__.__name__}>"

bp = unreal.load_asset(BP_PATH)
L(f"BP loaded: {bp}")
if not bp:
    L("ABORT — BP_Alice não carregou")
else:
    gc = bp.generated_class()
    cdo = unreal.get_default_object(gc)
    L(f"CDO class: {cdo.get_class().get_name() if cdo else None}")

    # SkeletalMeshComponent default do Character (slot 'Mesh')
    mc = safe(cdo, "mesh")
    L(f"comp 'mesh' = {mc}")
    if hasattr(mc, "get_editor_property"):
        sm = safe(mc, "skeletal_mesh_asset")
        L(f"  mesh.skeletal_mesh_asset = {sm.get_path_name() if hasattr(sm,'get_path_name') else sm}")
        L(f"  mesh.relative_location   = {safe(mc,'relative_location')}")
        L(f"  mesh.relative_rotation   = {safe(mc,'relative_rotation')}")
        L(f"  mesh.relative_scale3d    = {safe(mc,'relative_scale3d')}")
        L(f"  mesh.anim_class          = {safe(mc,'anim_class')}")

    # Listar TODAS as propriedades do CDO que terminam em _asset / _component
    L("--- propriedades 'mesh-like' do CDO ---")
    for pname in ("visual_mesh","visual_mesh_asset","visual_mesh_scale",
                  "visual_skeletal_mesh","visual_static_mesh",
                  "weapon_mesh","dress_mesh","alice_mesh"):
        v = safe(cdo, pname)
        if v is not None and "<err:" not in str(v):
            L(f"  {pname} = {v}")

    # AssetRegistry: dependencias do BP
    L("--- DEPENDENCIES (hard) ---")
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    try:
        opts = unreal.AssetRegistryDependencyOptions(
            include_soft_package_references=False,
            include_hard_package_references=True,
            include_searchable_names=False,
            include_soft_management_references=False,
            include_hard_management_references=False)
        for d in (ar.get_dependencies(BP_PATH, opts) or []):
            tag = " ⚠ FALTA" if not unreal.EditorAssetLibrary.does_asset_exist(str(d)) and "Characters" in str(d) else ""
            L(f"  HARD: {d}{tag}")
    except Exception as e: L(f"  hard deps err: {e}")
    L("--- DEPENDENCIES (soft) ---")
    try:
        opts2 = unreal.AssetRegistryDependencyOptions(
            include_soft_package_references=True,
            include_hard_package_references=False,
            include_searchable_names=False,
            include_soft_management_references=False,
            include_hard_management_references=False)
        for d in (ar.get_dependencies(BP_PATH, opts2) or []):
            tag = " ⚠ FALTA" if not unreal.EditorAssetLibrary.does_asset_exist(str(d)) and "Characters" in str(d) else ""
            L(f"  SOFT: {d}{tag}")
    except Exception as e: L(f"  soft deps err: {e}")

L("DIAG END")
