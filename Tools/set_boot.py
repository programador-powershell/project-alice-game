import unreal
L = lambda s: unreal.log(f"[BT] {s}")

# Margem: portal + target?
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_MargemDoRio")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
pfound=0
for a in eas.get_all_level_actors():
    if "Portal" in a.get_class().get_name():
        tl=a.get_editor_property("target_level"); pfound+=1
        L(f"Margem portal -> {tl}")
if pfound==0: L("Margem SEM portal")

# Mundo: gamemode + nav + sublevels
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas2 = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
nav=0; ps=0; roads=0
for a in eas2.get_all_level_actors():
    cn=a.get_class().get_name(); lbl=a.get_actor_label()
    if "NavMeshBounds" in cn: nav+=1
    if "PlayerStart" in cn: ps+=1
    if lbl.startswith("Road_"): roads+=1
ws=None
for a in eas2.get_all_level_actors():
    if "WorldSettings" in a.get_class().get_name(): ws=a; break
gm=ws.get_editor_property("default_game_mode") if ws else None
levels=unreal.EditorLevelUtils.get_levels(unreal.EditorLevelLibrary.get_editor_world())
L(f"Mundo: sublevels={len(levels)} GameMode={gm.get_name() if gm else None} nav={nav} roads={roads} playerstart={ps}")

# BP_Alice mesh + anim coerencia
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
m=cdo.get_editor_property("mesh").get_editor_property("skeletal_mesh_asset")
mskel=m.skeleton.get_name() if m and m.skeleton else "NULL"
idle=unreal.load_asset("/Game/Alice/AnimCoelho/C_Idle")
iskel=idle.get_skeleton().get_name() if idle and idle.get_skeleton() else "NULL"
L(f"player mesh={m.get_name() if m else None} mesh.skel={mskel} idle.skel={iskel} coerente={mskel==iskel}")
L("END")
