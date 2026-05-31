import unreal
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
vm = cdo.get_editor_property("visual_mesh")
sm = vm.get_editor_property("static_mesh") if vm else None
unreal.log(f"[vm] visual_mesh.static_mesh   = {sm.get_path_name() if sm else None}")
unreal.log(f"[vm] visual_mesh.visible       = {vm.get_editor_property('visible') if vm else None}")
unreal.log(f"[vm] visual_mesh.hidden_in_game= {vm.get_editor_property('hidden_in_game') if vm else None}")
unreal.log(f"[vm] visual_mesh.rel_location  = {vm.get_editor_property('relative_location') if vm else None}")
unreal.log(f"[vm] visual_mesh.rel_scale     = {vm.get_editor_property('relative_scale3d') if vm else None}")
unreal.log(f"[vm] visual_mesh.rel_rotation  = {vm.get_editor_property('relative_rotation') if vm else None}")
