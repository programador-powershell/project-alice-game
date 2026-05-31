"""Versao corrigida: lista todos os components de mesh dos actors no L_Arena.
Usa proprieties (nao metodos get_relative_*)."""
import unreal
L = lambda s: unreal.log(f"[live2] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()

for a in actors:
    cn = a.get_class().get_name()
    if not any(t in cn for t in ("Enemy","Boss","Coelho","Cheshire","Chapeleiro","Lagarta","Rainha","Lidia","Alice")):
        continue
    L(f"=== {cn} '{a.get_actor_label()}' ===")
    # SkeletalMeshComponent
    m = a.get_component_by_class(unreal.SkeletalMeshComponent)
    if m:
        sm = m.get_editor_property("skeletal_mesh_asset")
        rot = m.get_editor_property("relative_rotation")
        L(f"  Mesh.skeletal={sm.get_name() if sm else 'None'}  rel_rot={rot}")
    # StaticMeshComponent(s)
    sml = a.get_components_by_class(unreal.StaticMeshComponent)
    for c in sml:
        sm = c.get_editor_property("static_mesh")
        rot = c.get_editor_property("relative_rotation")
        scl = c.get_editor_property("relative_scale3d")
        L(f"  StaticComp '{c.get_name()}' mesh={sm.get_path_name() if sm else 'None'}")
        L(f"               rel_rot={rot}  scale={scl}")
L("END")
