"""Corrige animation_mode do mesh do BP_Alice via SubobjectDataSubsystem (CDO edit
nao persiste set_animation_mode confiavelmente). Estrategia dupla:
1. seta anim_class=None E animation_mode=SingleNode + animation_data=Idle no CDO
2. usa o template component do blueprint (SCS node) pra persistir
"""
import unreal
L = lambda s: unreal.log(f"[FM] {s}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
idle = unreal.load_asset("/Game/Alice/AnimAlice/Alice_Idle")

L(f"antes: mode={mc.get_editor_property('animation_mode')} anim_class={mc.get_editor_property('anim_class')}")

# 1. limpa anim_class (se houver) e poe SingleNode
mc.set_editor_property("anim_class", None)
import unreal as u
# tenta enum correto
try:
    mc.set_editor_property("animation_mode", u.AnimationMode.ANIMATION_SINGLE_NODE)
    L("set animation_mode=SingleNode OK")
except Exception as e:
    L(f"set mode err: {e}")

play = u.SingleAnimationPlayData()
play.anim_to_play = idle
play.looping = True
play.playing = True
mc.set_editor_property("animation_data", play)
L("animation_data=Alice_Idle loop")

L(f"depois(CDO): mode={mc.get_editor_property('animation_mode')}")

# 2. PERSISTE no template component via SubobjectData (o que o BP realmente usa)
try:
    sds = u.get_engine_subsystem(u.SubobjectDataSubsystem)
    handles = sds.k2_gather_subobject_data_for_blueprint(bp)
    for h in handles:
        data = sds.k2_find_subobject_data_from_handle(h)
        obj = u.SubobjectDataBlueprintFunctionLibrary.get_object(data)
        if obj and isinstance(obj, u.SkeletalMeshComponent):
            obj.set_editor_property("anim_class", None)
            obj.set_editor_property("animation_mode", u.AnimationMode.ANIMATION_SINGLE_NODE)
            p2 = u.SingleAnimationPlayData()
            p2.anim_to_play = idle; p2.looping=True; p2.playing=True
            obj.set_editor_property("animation_data", p2)
            L(f"template comp '{obj.get_name()}' -> SingleNode+Idle")
except Exception as e:
    L(f"subobject err: {e}")

# compila e salva
u.BlueprintEditorLibrary.compile_blueprint(bp)
u.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("compilado+salvo")
L("END")
