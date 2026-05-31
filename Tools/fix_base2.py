"""WorldBase grande certo. Engine Cube = 100cm (1m) com scale 1.
Mundo span: X -500..500=1000m, Y -75..575=650m. Centro(0,250)m. Folga: 1400x1000m.
scale p/ 1400m = 1400 (cube 1m * 1400 = 1400m). pos em cm: (0, 25000, -30)."""
import unreal
L=lambda s:unreal.log(f"[B] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
cube=unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
for a in eas.get_all_level_actors():
    if a.get_actor_label()=="WorldBase": eas.destroy_actor(a)
base=eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 25000, -30))
base.set_actor_label("WorldBase")
base.static_mesh_component.set_static_mesh(cube)
base.set_actor_scale3d(unreal.Vector(1400, 1000, 0.5))  # cube 1m * 1400 = 1400m X, 1000m Y, 0.5m alto
o,e=base.get_actor_bounds(False)
L(f"WorldBase tam=({e.x*2/100:.0f}x{e.y*2/100:.0f})m centro=({o.x/100:.0f},{o.y/100:.0f})")
unreal.EditorLoadingAndSavingUtils.save_current_level()
L("salvo")
L("END")
