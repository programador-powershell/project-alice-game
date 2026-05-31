"""Investiga profundamente por que DressMesh nao instancia: lista TODOS subobjects
do BP (incl heredados), procura override do componente."""
import unreal
L = lambda s: unreal.log(f"[DD] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
gc=bp.generated_class()

# get_all_class_default_subobjects do CDO
cdo=unreal.get_default_object(gc)
# tenta default_subobjects via reflection
try:
    sds=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles=sds.k2_gather_subobject_data_for_blueprint(bp)
    L(f"total subobject handles = {len(handles)}")
    for h in handles:
        d=sds.k2_find_subobject_data_from_handle(h)
        o=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(d)
        if o:
            L(f"  {o.get_class().get_name():28s} '{o.get_name()}'")
except Exception as e:
    L(f"sds err: {e}")

# Native subobjects do C++ (achados via list_archetypes?)
L("--- procura DressMesh em qualquer lugar do CDO ---")
for n in dir(cdo):
    if 'dress' in n.lower():
        L(f"  CDO attr: {n}")
        try:
            v=getattr(cdo, n)
            L(f"    val type={type(v).__name__} val={v}")
        except Exception as e:
            L(f"    err: {e}")
L("END")
