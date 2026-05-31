"""Remove o DressMeshComp criado via Python no BP_Alice (C++ vai criar DressMesh nativo)."""
import unreal
L = lambda s: unreal.log(f"[RM] {s}")
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
sds=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
handles=sds.k2_gather_subobject_data_for_blueprint(bp)
removed=0
for h in handles:
    d=sds.k2_find_subobject_data_from_handle(h)
    obj=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(d)
    if obj and "DressMeshComp" in obj.get_name():
        sds.delete_subobject(handles[0], h, bp)
        removed+=1
        L(f"removido {obj.get_name()}")
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L(f"removidos={removed} BP salvo")
L("END")
