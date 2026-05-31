"""Importa alice_FULL_rigged.fbx (corpo+vestido 1 mesh) + TODOS os 25 anims da pasta.
BP_Alice mesh = SK_AliceFull, DressMeshAsset=None (vestido ja no mesh)."""
import unreal, os
L=lambda s:unreal.log(f"[FA] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()

# pastas ja limpas no disco antes deste run
L("inicio (pastas limpas no disco)")

# 1. MESH merged
DSTB="/Game/Alice/Characters/AliceFull"
tb=unreal.AssetImportTask(); tb.filename=r"E:\References\3D\alice_FULL_rigged.fbx"
tb.destination_path=DSTB; tb.destination_name="SK_AliceFull"
tb.replace_existing=True; tb.automated=True; tb.save=True
ob=unreal.FbxImportUI()
ob.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH
ob.import_mesh=True; ob.import_as_skeletal=True; ob.import_materials=True; ob.import_textures=True
ob.import_animations=False; ob.create_physics_asset=True
tb.options=ob
tools.import_asset_tasks([tb])
body=unreal.load_asset(f"{DSTB}/SK_AliceFull")
bskel=unreal.load_asset(f"{DSTB}/SK_AliceFull_Skeleton")
L(f"mesh={'OK' if body else 'NULL'} skel={'OK' if bskel else 'NULL'}")
if not bskel: L("ABORT"); raise SystemExit
for i,m in enumerate(body.materials):
    mi=m.material_interface
    L(f"  mat[{i}]={mi.get_name() if mi else None}")

# 2. TODOS anims raiz
DSTA="/Game/Alice/AnimAlice"
AD=r"E:\References\model\anims"
import_ok=[]; import_fail=[]
for f in os.listdir(AD):
    if not f.lower().endswith(".fbx"): continue
    if f=="Eve_Skel.fbx": continue  # skeleton, nao anim
    name="A_"+os.path.splitext(f)[0].replace(" ","_").replace(".","_")
    p=os.path.join(AD,f)
    t=unreal.AssetImportTask(); t.filename=p; t.destination_path=DSTA; t.destination_name=name
    t.replace_existing=True; t.automated=True; t.save=True
    o=unreal.FbxImportUI()
    o.mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION
    o.import_mesh=False; o.import_as_skeletal=True; o.import_animations=True
    o.import_materials=False; o.import_textures=False; o.skeleton=bskel
    t.options=o
    tools.import_asset_tasks([t])
    a=unreal.load_asset(f"{DSTA}/{name}")
    if a and a.get_skeleton(): import_ok.append(name)
    else: import_fail.append(f)
L(f"anims OK={len(import_ok)} FAIL={len(import_fail)}")
for n in import_fail: L(f"  FALHOU: {n}")

# 3. BP wire — mesh full, sem DressMesh (vestido ja no mesh)
bp=unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo=unreal.get_default_object(bp.generated_class())
mc=cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", body)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_scale3d", unreal.Vector(1,1,1))
cdo.set_editor_property("dress_mesh_asset", None)  # vestido ja no mesh principal
# mapeia anims principais (nomes Mixamo)
def find(*keys):
    for k in keys:
        a=unreal.load_asset(f"{DSTA}/A_{k}")
        if a: return a
    return None
mp={
 "Anim_Idle": find("Standing_Idle","Eve_Idle"),
 "Anim_Walk": find("Walking","Eve_Walk"),
 "Anim_Run": find("Fast_Run","Eve_Run","Slow_Run"),
 "Anim_Atk1": find("Standing_Melee_Attack_Horizontal","Eve_Attack"),
 "Anim_Atk2": find("Standing_Melee_Attack_Backhand"),
 "Anim_Atk3": find("Standing_Melee_Attack_Downward"),
 "Anim_Attack": find("Standing_Melee_Combo_Attack_Ver__2","One_Hand_Sword_Combo"),
 "Anim_Dodge": find("Sprinting_Forward_Roll","Eve_Dodge"),
 "Anim_Death": find("Standing_React_Death_Forward","Eve_Death"),
 "Anim_Hit": find("Eve_Hit"),
}
nw=0
for prop,a in mp.items():
    if a:
        try: cdo.set_editor_property(prop.lower(), a); nw+=1
        except Exception as e: L(f"  wire {prop} err")
L(f"anims wired no BP={nw}")
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP salvo")
L("END")
