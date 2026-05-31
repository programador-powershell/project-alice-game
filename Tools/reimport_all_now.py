"""Reimporta corpo+vestido+anims AGORA (skeletons quebraram).
Tudo no MESMO skeleton SK_AliceBody_Skeleton (novo) + wire BP."""
import unreal, os
L = lambda s: unreal.log(f"[R] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()

# === 1. CORPO (novo skel) ===
DSTB="/Game/Alice/Characters/AliceBody"
# delete velho pra forcar skel novo
for n in ["SK_AliceBody","SK_AliceBody_Skeleton","SK_AliceBody_PhysicsAsset"]:
    p=f"{DSTB}/{n}"
    if unreal.EditorAssetLibrary.does_asset_exist(p):
        unreal.EditorAssetLibrary.delete_asset(p)
L("velhos deletados")

tb=unreal.AssetImportTask()
tb.filename=r"E:\References\3D\alice_RIGGED.fbx"
tb.destination_path=DSTB; tb.destination_name="SK_AliceBody"
tb.replace_existing=True; tb.automated=True; tb.save=True
ob=unreal.FbxImportUI()
ob.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
ob.import_mesh=True; ob.import_as_skeletal=True; ob.import_materials=True; ob.import_textures=True
ob.import_animations=False; ob.create_physics_asset=True
tb.options=ob
tools.import_asset_tasks([tb])
body=unreal.load_asset(f"{DSTB}/SK_AliceBody")
bskel=unreal.load_asset(f"{DSTB}/SK_AliceBody_Skeleton")
L(f"body skel={bskel.get_name() if bskel else 'NULL'}")

# === 2. VESTIDO no mesmo skel ===
DSTD="/Game/Alice/Characters/AliceDress2"
for n in ["SK_AliceDress","SK_AliceDress_PhysicsAsset"]:
    p=f"{DSTD}/{n}"
    if unreal.EditorAssetLibrary.does_asset_exist(p): unreal.EditorAssetLibrary.delete_asset(p)
td=unreal.AssetImportTask(); td.filename=r"E:\References\3D\alice_vestido_rigged.fbx"
td.destination_path=DSTD; td.destination_name="SK_AliceDress"
td.replace_existing=True; td.automated=True; td.save=True
od=unreal.FbxImportUI()
od.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
od.import_mesh=True; od.import_as_skeletal=True; od.import_materials=True; od.import_textures=True
od.import_animations=False; od.create_physics_asset=False; od.skeleton=bskel
td.options=od
tools.import_asset_tasks([td])
dress=unreal.load_asset(f"{DSTD}/SK_AliceDress")
L(f"dress skel={dress.skeleton.get_name() if dress and dress.skeleton else 'NULL'}")

# === 3. ANIMS ===
DSTA="/Game/Alice/AnimAlice"
AD=r"E:\References\model\anims"
clips=[("Standing Idle.fbx","A_Idle"),("Walking.fbx","A_Walk"),("Fast Run.fbx","A_Run"),
("Standing Melee Attack Horizontal.fbx","A_Atk1"),("Standing Melee Attack Backhand.fbx","A_Atk2"),
("Standing Melee Attack Downward.fbx","A_Atk3"),("Sprinting Forward Roll.fbx","A_Dodge"),
("Standing React Death Forward.fbx","A_Death")]
nok=0
for src,dst in clips:
    p=os.path.join(AD,src)
    if not os.path.exists(p): continue
    full=f"{DSTA}/{dst}"
    if unreal.EditorAssetLibrary.does_asset_exist(full): unreal.EditorAssetLibrary.delete_asset(full)
    t=unreal.AssetImportTask(); t.filename=p; t.destination_path=DSTA; t.destination_name=dst
    t.replace_existing=True; t.automated=True; t.save=True
    o=unreal.FbxImportUI()
    o.mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION
    o.import_mesh=False; o.import_as_skeletal=True; o.import_animations=True
    o.import_materials=False; o.import_textures=False; o.skeleton=bskel
    t.options=o
    tools.import_asset_tasks([t])
    a=unreal.load_asset(full)
    if a and a.get_skeleton(): nok+=1
L(f"anims OK={nok}/8")

# === 4. WIRE BP ===
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", body)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
cdo.set_editor_property("dress_mesh_asset", dress)
mp={"Anim_Idle":"A_Idle","Anim_Walk":"A_Walk","Anim_Run":"A_Run","Anim_Atk1":"A_Atk1",
"Anim_Atk2":"A_Atk2","Anim_Atk3":"A_Atk3","Anim_Attack":"A_Atk1","Anim_Dodge":"A_Dodge","Anim_Death":"A_Death"}
for prop,clip in mp.items():
    a=unreal.load_asset(f"{DSTA}/{clip}")
    if a:
        try: cdo.set_editor_property(prop,a)
        except: pass
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP wired+compiled")

# valida
idle=unreal.load_asset(f"{DSTA}/A_Idle")
L(f"FINAL body.skel={body.skeleton.get_name() if body.skeleton else 'NULL'} idle.skel={idle.get_skeleton().get_name() if idle and idle.get_skeleton() else 'NULL'}")
L("END")
