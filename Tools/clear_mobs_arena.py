"""Remove mobs/boss do L_Arena pra explorar o mapa sem combate.
Mantem tudo o mais (geometria, checkpoint, iluminacao, NavMesh, etc).
"""
import unreal
L = lambda s: unreal.log(f"[clear] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()

removed = []
for a in actors:
    cn = a.get_class().get_name()
    if any(t in cn for t in ("EnemyCharacter","BossCharacter","CoelhoBrancoBoss",
                              "CheshireBoss","ChapeleiroBoss","LagartaAzulBoss",
                              "RainhaCopasBoss","LidiaBoss")):
        label = a.get_actor_label()
        eas.destroy_actor(a)
        removed.append(f"{cn}:{label}")

for r in removed: L(f"  removido: {r}")
L(f"TOTAL removidos: {len(removed)}")

ok = unreal.EditorLoadingAndSavingUtils.save_current_level()
L(f"save L_Arena = {ok}")
L("CLEAR END")
