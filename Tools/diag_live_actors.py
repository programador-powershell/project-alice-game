"""Inspeciona TODOS os actors do tipo *Character no L_Arena:
- qual mesh skeletal/static cada um tem
- rotacao da capsule e do mesh
- velocidade (se PIE rodando)
Identifica mobs deitados.
"""
import unreal
L = lambda s: unreal.log(f"[live] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()

count = 0
for a in actors:
    cn = a.get_class().get_name()
    if "Character" not in cn and not any(t in cn for t in ("Enemy","Boss","Coelho","Cheshire","Chapeleiro","Lagarta","Rainha","Lidia","Alice")):
        continue
    count += 1
    L(f"--- {cn}  '{a.get_actor_label()}' ---")
    L(f"  loc={a.get_actor_location()}  rot={a.get_actor_rotation()}")
    # SkeletalMeshComponent (slot 'Mesh' do Character)
    try:
        m = a.get_component_by_class(unreal.SkeletalMeshComponent)
        if m:
            sm = m.get_editor_property("skeletal_mesh_asset")
            L(f"  Mesh.skeletal = {sm.get_name() if sm else 'None'}")
            L(f"  Mesh.rot      = {m.get_relative_rotation()}")
            L(f"  Mesh.loc      = {m.get_relative_location()}")
            L(f"  Mesh.animMode = {m.get_editor_property('animation_mode')}")
    except Exception as e:
        L(f"  skel err: {e}")
    # Static meshes (VisualMesh etc)
    try:
        for comp in a.get_components_by_class(unreal.StaticMeshComponent):
            sm = comp.get_editor_property("static_mesh")
            if sm:
                L(f"  StaticMeshComp '{comp.get_name()}' = {sm.get_name()}  rot={comp.get_relative_rotation()}")
    except Exception as e:
        L(f"  static err: {e}")

L(f"TOTAL characters in L_Arena = {count}")
L("DIAG END")
