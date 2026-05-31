"""Reload do BP_Alice pra pegar DressMesh do C++ atualizado, depois seta SK_AliceDress."""
import unreal
L = lambda s: unreal.log(f"[RD] {s}")

# reload do BP class
unreal.EditorAssetLibrary.consolidate_assets
ar=unreal.AssetRegistryHelpers.get_asset_registry()
# unload + load
path="/Game/Alice/Blueprints/BP_Alice"
unreal.EditorAssetLibrary.do_assets_exist  # noop
# tenta reload via class compile
bp=unreal.load_asset(path)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
gc=bp.generated_class()
L(f"BP class={gc.get_name()}")

# Lista TODAS props do CDO que contem 'mesh' (achar nome real)
cdo=unreal.get_default_object(gc)
props_mesh=[]
for p in dir(cdo):
    if 'mesh' in p.lower() and not p.startswith('_'):
        props_mesh.append(p)
L(f"props com 'mesh': {props_mesh}")

# Tenta varios nomes
dress=unreal.load_asset("/Game/Alice/Characters/AliceDress2/SK_AliceDress")
for prop in ["dress_mesh","DressMesh","dressmesh","dress_mesh_component"]:
    try:
        v=cdo.get_editor_property(prop)
        L(f"  prop '{prop}' = {v}")
        if v and hasattr(v,'set_editor_property'):
            v.set_editor_property("skeletal_mesh_asset", dress)
            L(f"  >>> SET ok via '{prop}'")
            break
    except Exception as e:
        L(f"  '{prop}' err: {type(e).__name__}")

# Alternativa: itera subobjects
try:
    sds=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles=sds.k2_gather_subobject_data_for_blueprint(bp)
    for h in handles:
        d=sds.k2_find_subobject_data_from_handle(h)
        o=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(d)
        if o and isinstance(o, unreal.SkeletalMeshComponent):
            curr=o.get_editor_property("skeletal_mesh_asset")
            L(f"  subobj '{o.get_name()}' currMesh={curr.get_name() if curr else None}")
            if o.get_name()!="CharacterMesh0" and (not curr or curr.get_name()!="SK_AliceBody"):
                o.set_editor_property("skeletal_mesh_asset", dress)
                L(f"  >>> SET DressMesh via subobject '{o.get_name()}'")
except Exception as e:
    L(f"subobj err: {e}")

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP recompilado+salvo")
L("END")
