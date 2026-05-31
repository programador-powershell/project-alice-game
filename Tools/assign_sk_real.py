"""Lista assets em AliceReal e ATRIBUI o SK correto ao BP_Alice (carregando por classe)."""
import unreal
L = lambda s: unreal.log(f"[ar] {s}")

# lista tudo na pasta
ar = unreal.AssetRegistryHelpers.get_asset_registry()
assets = ar.get_assets_by_path("/Game/Alice/Characters/AliceReal", recursive=True)
for a in assets:
    L(f"  {str(a.asset_class_path.asset_name):20s}  {str(a.package_name)}")

# pega o SkeletalMesh
sk = None
for a in assets:
    if str(a.asset_class_path.asset_name) == "SkeletalMesh":
        sk = unreal.load_asset(str(a.package_name))
        L(f"SkeletalMesh achado: {a.package_name}  type={type(sk).__name__}")
        break

if not sk:
    L("ABORT — nenhum SkeletalMesh encontrado em AliceReal"); raise SystemExit

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", sk)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L(f"BP_Alice.mesh.skeletal = {sk.get_path_name()}  SAVED")

# confirma skeleton
L(f"sk.skeleton = {sk.skeleton.get_path_name() if sk.skeleton else None}")
L("DONE — da Play, Alice nua mas com anim Mixamo real")
