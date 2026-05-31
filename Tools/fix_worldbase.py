"""Corrige WorldBase: cubo engine=100cm=1u. scale=metros direto (NAO /100).
Cobre todo o mundo + folga."""
import unreal
L = lambda s: unreal.log(f"[FB] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

S=250.0
xs=[-2*S,-1*S,0,1*S,2*S]; ys=[0,1*S,2*S,3*S]
cx=(min(xs)+max(xs))/2*100; cy=(min(ys)+max(ys))/2*100
spanx=(max(xs)-min(xs)+500)  # m, +folga
spany=(max(ys)-min(ys)+500)

base=None
for a in eas.get_all_level_actors():
    if a.get_actor_label()=="WorldBase": base=a; break
if not base:
    cube=unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    base=eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(cx,cy,-60))
    base.set_actor_label("WorldBase")
    base.static_mesh_component.set_static_mesh(cube)

base.set_actor_location(unreal.Vector(cx,cy,-60),False,False)
# cubo 100cm. scale = span_em_metros (1 scale = 1m). thin Z.
base.set_actor_scale3d(unreal.Vector(spanx, spany, 1.0))
L(f"WorldBase corrigido = {spanx:.0f}x{spany:.0f}m @ centro({cx/100:.0f},{cy/100:.0f})")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L("salvo")
L("END")
