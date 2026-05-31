"""Le estado AO VIVO do PIE: pawn, mesh rotation runtime, camera location vs pawn.
Roda enquanto PIE ativo. Verdade real (nao asset)."""
import unreal
L=lambda s:unreal.log(f"[LV] {s}")

# pega world PIE
ges=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
w=ges.get_game_world() if hasattr(ges,'get_game_world') else None
if not w:
    try: w=unreal.EditorLevelLibrary.get_game_world()
    except: w=None
L(f"game_world={w}")
if not w: L("sem PIE world"); raise SystemExit

pawn=unreal.GameplayStatics.get_player_pawn(w,0)
L(f"pawn={pawn.get_name() if pawn else None}")
if pawn:
    L(f"pawn loc={pawn.get_actor_location()}")
    mesh=pawn.get_component_by_class(unreal.SkeletalMeshComponent)
    if mesh:
        L(f"mesh world_rot={mesh.get_world_rotation()}")
        L(f"mesh rel_rot={mesh.get_relative_rotation()}")
        L(f"mesh sk={mesh.get_skeletal_mesh_asset().get_name() if mesh.get_skeletal_mesh_asset() else None}")
        L(f"mesh anim_mode={mesh.get_editor_property('animation_mode')}")
    cam=unreal.GameplayStatics.get_player_camera_manager(w,0)
    if cam:
        L(f"cam loc={cam.get_camera_location()}")
        L(f"dist cam->pawn={(cam.get_camera_location()-pawn.get_actor_location()).size():.0f}")
L("END")
