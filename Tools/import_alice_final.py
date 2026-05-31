"""Importa Alice corpo + vestido (mesmo skeleton) + anims + vira player com Leader Pose.
1. corpo alice_RIGGED -> SK_AliceBody (skeleton novo)
2. vestido alice_vestido_rigged -> SK_AliceDress (REUSA skeleton do corpo)
3. 8 anims no skeleton do corpo
4. BP_Alice: mesh=corpo + anims; add SK_AliceDress como child com Leader Pose
"""
import unreal, os
L = lambda s: unreal.log(f"[AF] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()

# === 1. CORPO ===
DSTB="/Game/Alice/Characters/AliceBody"
unreal.EditorAssetLibrary.make_directory(DSTB)
tb=unreal.AssetImportTask(); tb.filename=r"E:\References\3D\alice_RIGGED.fbx"
tb.destination_path=DSTB; tb.destination_name="SK_AliceBody"
tb.replace_existing=True; tb.automated=True; tb.save=True
ob=unreal.FbxImportUI()
ob.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
ob.import_mesh=True; ob.import_as_skeletal=True; ob.import_materials=True; ob.import_textures=True
ob.import_animations=False; ob.create_physics_asset=True
tb.options=ob
tools.import_asset_tasks([tb])
ar=unreal.AssetRegistryHelpers.get_asset_registry()
body=None; bodyskel=None
for a in ar.get_assets_by_path(DSTB, recursive=True):
    c=str(a.asset_class_path.asset_name)
    if c=="SkeletalMesh": body=unreal.load_asset(str(a.package_name))
    if c=="Skeleton": bodyskel=unreal.load_asset(str(a.package_name))
L(f"corpo={body.get_name() if body else None} skel={bodyskel.get_name() if bodyskel else None}")
if not body or not bodyskel: L("ABORT corpo"); raise SystemExit

# === 2. VESTIDO (reusa skeleton do corpo) ===
DSTD="/Game/Alice/Characters/AliceDress2"
unreal.EditorAssetLibrary.make_directory(DSTD)
td=unreal.AssetImportTask(); td.filename=r"E:\References\3D\alice_vestido_rigged.fbx"
td.destination_path=DSTD; td.destination_name="SK_AliceDress"
td.replace_existing=True; td.automated=True; td.save=True
od=unreal.FbxImportUI()
od.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
od.import_mesh=True; od.import_as_skeletal=True; od.import_materials=True; od.import_textures=True
od.import_animations=False; od.create_physics_asset=False
od.skeleton=bodyskel  # MESMO skeleton -> Leader Pose funciona
td.options=od
tools.import_asset_tasks([td])
dress=None
for a in ar.get_assets_by_path(DSTD, recursive=True):
    if str(a.asset_class_path.asset_name)=="SkeletalMesh": dress=unreal.load_asset(str(a.package_name))
L(f"vestido={dress.get_name() if dress else None} skel={dress.skeleton.get_name() if dress and dress.skeleton else None}")

# === 3. ANIMS no skeleton do corpo ===
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
    if a: nok+=1
L(f"anims={nok}/8 no skeleton corpo")

# === 4. BP_Alice: mesh corpo + anims ===
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
L("BP_Alice: corpo + anims SAVED")
L(f"NOTA: vestido SK_AliceDress pronto p/ Leader Pose (mesmo skel). Add no BP component depois.")
L("DONE")
