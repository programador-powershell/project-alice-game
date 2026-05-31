"""Seta DressMeshAsset (property simples, nao subobject) no BP_Alice.
SK_AliceDress sera spawnado em BeginPlay via NewObject."""
import unreal
L = lambda s: unreal.log(f"[SDA] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
dress=unreal.load_asset("/Game/Alice/Characters/AliceDress2/SK_AliceDress")
L(f"bp={'OK' if bp else 'MISS'} dress={'OK' if dress else 'MISS'}")
cdo=unreal.get_default_object(bp.generated_class())
try:
    cdo.set_editor_property("dress_mesh_asset", dress)
    L(f"DressMeshAsset = {dress.get_name()} OK")
except Exception as e:
    L(f"err: {e}")

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
# verifica
v=cdo.get_editor_property("dress_mesh_asset")
L(f"verify dress_mesh_asset = {v.get_name() if v else None}")
L("END")
