"""Atribui ABP_Coelho ao mesh do BP_Alice (anim_class), pra GetAnimInstance() ser valido
no C++ -> Dynamic Montage funciona. Compila + salva."""
import unreal
L = lambda s: unreal.log(f"[SA] {s}")

abp = unreal.load_asset("/Game/Alice/AnimCoelho/ABP_Coelho")
L(f"ABP = {'OK' if abp else 'MISS'}")
gc = abp.generated_class() if abp else None
L(f"ABP gen class = {gc.get_name() if gc else None}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
if gc:
    mc.set_editor_property("anim_class", gc)
    L("anim_class = ABP_Coelho setado")
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)

# verifica
c2 = unreal.get_default_object(bp.generated_class()).get_editor_property("mesh")
ac = c2.get_editor_property("anim_class")
L(f"pos-compile anim_class = {ac.get_name() if ac else 'None'}")
L("END")
