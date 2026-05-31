import unreal
L = lambda s: unreal.log(f"[DC] {s}")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
L("--- CoelhoPlayer ---")
for a in ar.get_assets_by_path("/Game/Alice/Characters/CoelhoPlayer", recursive=True):
    L(f"  {str(a.asset_class_path.asset_name)} {str(a.package_name)}")
# mesh do BP_Alice + skel dele
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
m=cdo.get_editor_property("mesh").get_editor_property("skeletal_mesh_asset")
L(f"BP_Alice mesh={m.get_name() if m else None} skel={m.skeleton.get_name() if m and m.skeleton else 'NULL'}")
L("END")
