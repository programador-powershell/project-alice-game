"""Importa 8 anims essenciais no SK_CoelhoPlayer_Skeleton (41 bones).
UE mapeia por nome (anims 65 -> coelho 41 subconjunto mixamorig).
Depois liga ao BP_Alice + seta mesh = SK_CoelhoPlayer.
"""
import unreal, os
L = lambda s: unreal.log(f"[AC] {s}")

SKEL = unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer_Skeleton")
if not SKEL: L("ABORT sem skeleton"); raise SystemExit
DST = "/Game/Alice/AnimCoelho"
unreal.EditorAssetLibrary.make_directory(DST)
AD = r"E:\References\model\anims"

clips = [
    ("Standing Idle.fbx","C_Idle"),
    ("Walking.fbx","C_Walk"),
    ("Fast Run.fbx","C_Run"),
    ("Standing Melee Attack Horizontal.fbx","C_Atk1"),
    ("Standing Melee Attack Backhand.fbx","C_Atk2"),
    ("Standing Melee Attack Downward.fbx","C_Atk3"),
    ("Sprinting Forward Roll.fbx","C_Dodge"),
    ("Standing React Death Forward.fbx","C_Death"),
]
tools = unreal.AssetToolsHelpers.get_asset_tools()
done = {}
for src,dst in clips:
    p = os.path.join(AD, src)
    if not os.path.exists(p): L(f"  MISS {src}"); continue
    t = unreal.AssetImportTask()
    t.filename=p; t.destination_path=DST; t.destination_name=dst
    t.replace_existing=True; t.automated=True; t.save=True
    o = unreal.FbxImportUI()
    o.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
    o.import_mesh=False; o.import_as_skeletal=True
    o.import_animations=True; o.import_materials=False; o.import_textures=False
    o.skeleton = SKEL
    t.options=o
    tools.import_asset_tasks([t])
    ok = t.imported_object_paths
    done[dst]= ok[0] if ok else None
    L(f"  {dst} <- {src} {'OK' if ok else 'FALHOU'}")
L(f"anims ok = {sum(1 for v in done.values() if v)}/{len(clips)}")

# seta mesh + anims no BP_Alice
sk = unreal.load_asset("/Game/Alice/Characters/CoelhoPlayer/SK_CoelhoPlayer")
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", sk)
mc.set_editor_property("anim_class", None)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))

def A(n): return unreal.load_asset(f"{DST}/{n}")
mp = {"Anim_Idle":"C_Idle","Anim_Walk":"C_Walk","Anim_Run":"C_Run",
      "Anim_Atk1":"C_Atk1","Anim_Atk2":"C_Atk2","Anim_Atk3":"C_Atk3",
      "Anim_Attack":"C_Atk1","Anim_Dodge":"C_Dodge","Anim_Death":"C_Death"}
for prop,clip in mp.items():
    a=A(clip)
    if a:
        try: cdo.set_editor_property(prop,a)
        except Exception as e: L(f"  set {prop} err {e}")
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L(f"BP_Alice mesh=SK_CoelhoPlayer + anims ligados SAVED")
L(f"coerencia: mesh.skel={sk.skeleton.get_name()} idle.skel={A('C_Idle').get_skeleton().get_name() if A('C_Idle') else None}")
L("DONE — da Play")
