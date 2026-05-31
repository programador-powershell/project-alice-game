"""Forca mesh rotation pra pitch=0 yaw=-90 roll=0 (em pé + virada).
Usa unreal.Rotator(roll, pitch, yaw) que é ordem TKEYWORDED segura."""
import unreal
L = lambda s: unreal.log(f"[FO] {s}")

bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")

# tenta varias formas
import unreal as u
r1 = u.Rotator(0.0, 0.0, -90.0)   # posicional: (roll, pitch, yaw) UE5 Python convention?
L(f"r1 = {r1}")
r2 = u.Rotator(roll=0.0, pitch=0.0, yaw=-90.0)
L(f"r2 = {r2}")

# escolhe kw (explicito)
mc.set_editor_property("relative_rotation", r2)
mc.set_editor_property("relative_location", u.Vector(0,0,-88))
# leitura final
rr=mc.get_editor_property("relative_rotation")
L(f"depois set: rel_rot={rr}")

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP salvo")
L("END")
