"""Player = coelho (3a pessoa que funcionava) + boot direto no L_Mundo pra andar e ver mapa."""
import unreal
L=lambda s:unreal.log(f"[CM] {s}")

# player mesh = coelho
coelho=unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer")
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
if coelho:
    mc.set_editor_property("skeletal_mesh_asset", coelho)
    mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
    mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
    mc.set_editor_property("relative_scale3d", unreal.Vector(1,1,1))
    cdo.set_editor_property("dress_mesh_asset", None)
    L(f"player mesh = SK_CoelhoPlayer")
else:
    L("coelho MISS - mantem mesh atual")
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP salvo")
L("PRONTO — abra L_Mundo + Alt+P pra andar")
L("END")
