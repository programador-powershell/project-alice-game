"""Fix mobs deitados em L_Arena:
- Boss_CoelhoBranco: skeletal=SK_CoelhoReal, esconde VisualMesh estatico
- Mob_0/Mob_1 (soldados, so static): rotaciona VisualMesh pitch=-90 (gambiarra ate rigar)
Salva o level.
"""
import unreal
L = lambda s: unreal.log(f"[fix_mobs] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()

sk_coelho = unreal.load_asset("/Game/Alice/Characters/CoelhoReal/SK_CoelhoReal")
L(f"SK_CoelhoReal load = {'OK' if sk_coelho else 'MISS'}")

for a in actors:
    cn = a.get_class().get_name()
    label = a.get_actor_label()
    # COELHO BOSS — tem skeletal pronto
    if "CoelhoBrancoBoss" in cn and sk_coelho:
        m = a.get_component_by_class(unreal.SkeletalMeshComponent)
        if m:
            m.set_editor_property("skeletal_mesh_asset", sk_coelho)
            m.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
            m.set_editor_property("relative_location", unreal.Vector(0,0,-88))
            L(f"  [{label}] Mesh.skeletal=SK_CoelhoReal + rot pitch=0 yaw=-90")
        for c in a.get_components_by_class(unreal.StaticMeshComponent):
            if c.get_name() == "VisualMesh":
                c.set_editor_property("visible", False)
                c.set_editor_property("hidden_in_game", True)
                L(f"  [{label}] VisualMesh hidden (substituido por skeletal)")
    # SOLDADO MOBS — sem skel, so rotaciona o static
    elif "EnemyCharacter" in cn and "Mob" in label:
        for c in a.get_components_by_class(unreal.StaticMeshComponent):
            if c.get_name() == "VisualMesh":
                c.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=-90,yaw=0))
                # ajusta tb a altura (cm static rota pivot pode sair do chao)
                L(f"  [{label}] VisualMesh rotacionado pitch=-90 (em pe)")

# Salvar level
ok = unreal.EditorLoadingAndSavingUtils.save_current_level()
L(f"save L_Arena = {ok}")
L("FIX MOBS END")
