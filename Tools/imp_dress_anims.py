"""Vestido (reusa skel corpo) + anims + wire BP. Corpo ja importado."""
import unreal, os
L = lambda s: unreal.log(f"[DA] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()

bodyskel=unreal.load_asset("/Game/Alice/Characters/AliceBody/SK_AliceBody_Skeleton")
body=unreal.load_asset("/Game/Alice/Characters/AliceBody/SK_AliceBody")
L(f"bodyskel={'OK' if bodyskel else 'NULL'}")
if not bodyskel: raise SystemExit

# vestido reusa skel
DSTD="/Game/Alice/Characters/AliceDress2"
unreal.EditorAssetLibrary.make_directory(DSTD)
td=unreal.AssetImportTask(); td.filename=r"E:\References\3D\alice_vestido_rigged.fbx"
td.destination_path=DSTD; td.destination_name="SK_AliceDress"
td.replace_existing=True; td.automated=True; td.save=True
od=unreal.FbxImportUI()
od.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
od.import_mesh=True; od.import_as_skeletal=True; od.import_materials=True; od.import_textures=True
od.import_animations=False; od.create_physics_asset=False; od.skeleton=bodyskel
td.options=od
tools.import_asset_tasks([td])
dress=unreal.load_asset(f"{DSTD}/SK_AliceDress")
L(f"vestido={'OK' if dress else 'NULL'} skel={dress.skeleton.get_name() if dress and dress.skeleton else 'NULL'}")

# anims
DSTA="/Game/Alice/AnimAlice"
unreal.EditorAssetLibrary.make_directory(DSTA)
AD=r"E:\References\model\anims"
clips=[("Standing Idle.fbx","A_Idle"),("Walking.fbx","A_Walk"),("Fast Run.fbx","A_Run"),
("Standing Melee Attack Horizontal.fbx","A_Atk1"),("Standing Melee Attack Backhand.fbx","A_Atk2"),
("Standing Melee Attack Downward.fbx","A_Atk3"),("Sprinting Forward Roll.fbx","A_Dodge"),
("Standing React Death Forward.fbx","A_Death")]
nok=0
for src,dst in clips:
    p=os.path.join(AD,src)
    if not os.path.exists(p): continue
    t=unreal.AssetImportTask(); t.filename=p; t.destination_path=DSTA; t.destination_name=dst
    t.replace_existing=True; t.automated=True; t.save=True
    o=unreal.FbxImportUI()
    o.mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION
    o.import_mesh=False; o.import_as_skeletal=True; o.import_animations=True
    o.import_materials=False; o.import_textures=False; o.skeleton=bodyskel
    t.options=o
    tools.import_asset_tasks([t])
    a=unreal.load_asset(f"{DSTA}/{dst}")
    sk=a.get_skeleton() if a else None
    if a and sk: nok+=1
L(f"anims OK={nok}/8")

# wire BP
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", body)
mc.set_editor_property("anim_class", None)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_rotation", unreal.Rotator(0,-90,0))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
mp={"Anim_Idle":"A_Idle","Anim_Walk":"A_Walk","Anim_Run":"A_Run","Anim_Atk1":"A_Atk1",
"Anim_Atk2":"A_Atk2","Anim_Atk3":"A_Atk3","Anim_Attack":"A_Atk1","Anim_Dodge":"A_Dodge","Anim_Death":"A_Death"}
for prop,clip in mp.items():
    a=unreal.load_asset(f"{DSTA}/{clip}")
    if a:
        try: cdo.set_editor_property(prop,a)
        except: pass
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP_Alice corpo+anims SAVED")
# coerencia
idle=unreal.load_asset(f"{DSTA}/A_Idle")
L(f"COER mesh.skel={body.skeleton.get_name()} idle.skel={idle.get_skeleton().get_name() if idle and idle.get_skeleton() else 'NULL'}")
L("DONE")
