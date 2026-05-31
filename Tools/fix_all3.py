import unreal, os
L = lambda s: unreal.log(f"[FX3] {s}")

SKEL = unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer_Skeleton")
L(f"skel coelho = {'OK' if SKEL else 'NULL'}")

# === 1. reimporta anims nesse skeleton + SALVA cada ===
DST="/Game/Alice/AnimCoelho"
AD=r"E:\References\model\anims"
clips=[("Standing Idle.fbx","C_Idle"),("Walking.fbx","C_Walk"),("Fast Run.fbx","C_Run"),
("Standing Melee Attack Horizontal.fbx","C_Atk1"),("Standing Melee Attack Backhand.fbx","C_Atk2"),
("Standing Melee Attack Downward.fbx","C_Atk3"),("Sprinting Forward Roll.fbx","C_Dodge"),
("Standing React Death Forward.fbx","C_Death")]
tools=unreal.AssetToolsHelpers.get_asset_tools()
for src,dst in clips:
    p=os.path.join(AD,src)
    if not os.path.exists(p): continue
    t=unreal.AssetImportTask(); t.filename=p; t.destination_path=DST; t.destination_name=dst
    t.replace_existing=True; t.automated=True; t.save=True
    o=unreal.FbxImportUI()
    o.mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION
    o.import_mesh=False; o.import_as_skeletal=True; o.import_animations=True
    o.import_materials=False; o.import_textures=False; o.skeleton=SKEL
    t.options=o
    tools.import_asset_tasks([t])
    a=unreal.load_asset(f"{DST}/{dst}")
    sk=a.get_skeleton() if a else None
    if a: unreal.EditorAssetLibrary.save_loaded_asset(a, only_if_is_dirty=False)
    L(f"  {dst} skel={sk.get_name() if sk else 'NULL'}")

# === 2. wire anims no BP + 3. GameMode no Mundo ===
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer"))
mc.set_editor_property("anim_class", None)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_rotation", unreal.Rotator(0,-90,0))
mp={"Anim_Idle":"C_Idle","Anim_Walk":"C_Walk","Anim_Run":"C_Run","Anim_Atk1":"C_Atk1",
"Anim_Atk2":"C_Atk2","Anim_Atk3":"C_Atk3","Anim_Attack":"C_Atk1","Anim_Dodge":"C_Dodge","Anim_Death":"C_Death"}
for prop,clip in mp.items():
    a=unreal.load_asset(f"{DST}/{clip}")
    if a:
        try: cdo.set_editor_property(prop,a)
        except: pass
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP anims+mesh salvos")

# === GameMode no L_Mundo (via World Settings, persistir) ===
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
gm=unreal.load_class(None,"/Game/Alice/Blueprints/BP_AliceGameMode.BP_AliceGameMode_C")
L(f"gm class={'OK' if gm else 'NULL'}")
ws=None
for a in eas.get_all_level_actors():
    if "WorldSettings" in a.get_class().get_name(): ws=a; break
if ws and gm:
    ws.set_editor_property("default_game_mode", gm)
    L("GameMode setado WorldSettings")
# === extra PlayerStarts dos sublevels: deixa so 1 (Interior) ===
pss=[a for a in eas.get_all_level_actors() if "PlayerStart" in a.get_class().get_name()]
L(f"playerstarts={len(pss)}")
# mantem o mais a oeste (Interior, x mais negativo), apaga resto
if len(pss)>1:
    pss.sort(key=lambda a:a.get_actor_location().x)
    keep=pss[0]; keep.set_actor_location(unreal.Vector(-50000,0,200),False,False)
    for extra in pss[1:]: eas.destroy_actor(extra)
    L(f"mantido 1 PlayerStart no Interior, apagados {len(pss)-1}")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L("L_Mundo salvo")
L("END")
