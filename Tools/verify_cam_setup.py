"""Confirma scale revertido + investiga CADEIA de attach da camera.
1a pessoa com mesh OK = CameraBoom mal attachado ou TargetArmLength=0 em runtime."""
import unreal
L = lambda s: unreal.log(f"[V] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
L(f"mesh scale={mc.get_editor_property('relative_scale3d')}")

# CameraBoom attach + settings
boom=cdo.get_editor_property("camera_boom")
if boom:
    L(f"Boom armlen={boom.get_editor_property('target_arm_length')}")
    pp=boom.get_attach_parent() if hasattr(boom,'get_attach_parent') else None
    L(f"Boom attach_parent={pp.get_name() if pp else 'None/Root'}")
    L(f"Boom do_collision_test={boom.get_editor_property('do_collision_test')}")
    L(f"Boom socket_offset={boom.get_editor_property('socket_offset')}")

# remove test actors (retry)
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
n=0
for a in eas.get_all_level_actors():
    lb=a.get_actor_label()
    if lb.startswith("TestSize") or lb=="TestAliceAnim": eas.destroy_actor(a); n+=1
unreal.EditorLoadingAndSavingUtils.save_current_level()
L(f"tests removidos={n}")
L("END")
