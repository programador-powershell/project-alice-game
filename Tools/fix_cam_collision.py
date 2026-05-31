"""Desliga do_collision_test do CameraBoom — spring arm colapsava pra 0 (1a pessoa)
por bater no mesh/chao. Sem collision test = camera fica nos 420cm = 3a pessoa."""
import unreal
L = lambda s: unreal.log(f"[CC] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
boom=cdo.get_editor_property("camera_boom")
L(f"do_collision_test antes = {boom.get_editor_property('do_collision_test')}")
boom.set_editor_property("do_collision_test", False)
boom.set_editor_property("target_arm_length", 420.0)
boom.set_editor_property("socket_offset", unreal.Vector(0, 40, 70))
L(f"do_collision_test depois = {boom.get_editor_property('do_collision_test')}")
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP salvo: camera sem collision-collapse")
L("END")
