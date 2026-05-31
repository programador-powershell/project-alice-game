"""Diagnostica a cadeia de animacao da Alice:
- Skeleton do SK_AliceDressed vs Skeleton dos clips A_Idle/Walk/Run/Atk*
- Se Anim_* estao seteados no CDO do BP_Alice
- Lista actors do L_Arena (mobs/bosses) com seus meshes
"""
import unreal
L = lambda s: unreal.log(f"[anim] {s}")

# 1. Skeleton do mesh do player
sk_mesh = unreal.load_asset("/Game/Alice/Characters/AliceDressed/SK_AliceDressed")
sk_skel = sk_mesh.skeleton if sk_mesh else None
L(f"SK_AliceDressed.skeleton = {sk_skel.get_path_name() if sk_skel else None}")

# 2. Skeleton dos clips
for clip_path in ("/Game/Alice/AnimM/A_Idle","/Game/Alice/AnimM/A_Walk",
                  "/Game/Alice/AnimM/A_Run","/Game/Alice/AnimM/A_Atk1",
                  "/Game/Alice/AnimM/A_Dodge","/Game/Alice/AnimM/A_Hit"):
    c = unreal.load_asset(clip_path)
    s = c.get_skeleton() if c else None
    L(f"  {clip_path.split('/')[-1]:8s} skeleton = {s.get_path_name() if s else 'None'}")

# 3. Anim_* setados no CDO do BP_Alice?
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
L("--- Anim_* no CDO BP_Alice ---")
for prop in ("Anim_Idle","Anim_Walk","Anim_Run","Anim_Attack","Anim_Atk1",
             "Anim_Atk2","Anim_Atk3","Anim_Dodge","Anim_Hit","Anim_Death",
             "Anim_Block","Anim_Parry","Anim_GS_Idle","Anim_GS_Run","Anim_GS_Atk",
             "Anim_SS_Idle","Anim_SS_Atk","Anim_Dual_Atk"):
    try:
        v = cdo.get_editor_property(prop)
        L(f"  {prop:14s} = {v.get_name() if v else 'None'}")
    except Exception as e:
        L(f"  {prop:14s} ERR {e}")

# 4. Actors no L_Arena (mob/boss)
L("--- actors em L_Arena ---")
ws = unreal.EditorAssetLibrary.load_asset("/Game/Alice/Maps/L_Arena")
try:
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    # tenta carregar level pra acessar actors
    unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
    actors = eas.get_all_level_actors()
    for a in actors:
        cn = a.get_class().get_name()
        if any(t in cn for t in ("Enemy","Boss","Coelho","Cheshire","Chapeleiro","Lagarta","Rainha","Lidia","Alice")):
            L(f"  {cn:25s}  {a.get_actor_label()}  at {a.get_actor_location()}")
except Exception as e:
    L(f"  err loading L_Arena: {e}")
L("DIAG END")
