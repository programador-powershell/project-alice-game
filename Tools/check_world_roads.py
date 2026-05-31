import unreal
L = lambda s: unreal.log(f"[CR] {s}")
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
roads=0; base=0
for a in eas.get_all_level_actors():
    lbl=a.get_actor_label()
    if lbl.startswith("Road_"): roads+=1
    if lbl=="WorldBase": base+=1
L(f"roads={roads} base={base}")
L("END")
