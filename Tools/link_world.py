"""1) Portal no fim de L_MargemDoRio -> L_Mundo
   2) BP_AliceGameMode no World Settings do L_Mundo
   3) NavMeshBoundsVolume cobrindo o mundo
"""
import unreal
L = lambda s: unreal.log(f"[LW] {s}")

# === 1. Portal na Margem ===
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_MargemDoRio")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
# acha classe APortalActor
portal_cls = unreal.load_class(None, "/Script/Alice.PortalActor")
L(f"PortalActor class = {'OK' if portal_cls else 'MISS'}")
# remove portais antigos
for a in eas.get_all_level_actors():
    if "Portal" in a.get_class().get_name():
        eas.destroy_actor(a)
# acha fim da margem (maior Y, ou perto do PlayerStart + frente). usa centro+offset
ps=None
for a in eas.get_all_level_actors():
    if "PlayerStart" in a.get_class().get_name(): ps=a; break
loc = unreal.Vector(0,800,150)
if ps:
    p=ps.get_actor_location(); loc=unreal.Vector(p.x, p.y+1200, p.z)
if portal_cls:
    portal = eas.spawn_actor_from_class(portal_cls, loc)
    portal.set_actor_label("Portal_ToMundo")
    portal.set_editor_property("target_level", "L_Mundo")
    L(f"Portal_ToMundo @ {loc} -> L_Mundo")
unreal.EditorLoadingAndSavingUtils.save_current_level()
L("Margem salva")

# === 2+3. GameMode + NavMesh no L_Mundo ===
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas2 = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
# GameMode via WorldSettings
ws=None
for a in eas2.get_all_level_actors():
    if "WorldSettings" in a.get_class().get_name(): ws=a; break
gm = unreal.load_class(None, "/Game/Alice/Blueprints/BP_AliceGameMode.BP_AliceGameMode_C")
if not gm:
    gm = unreal.load_class(None, "/Script/Alice.AliceGameMode")
if ws and gm:
    ws.set_editor_property("default_game_mode", gm)
    L(f"GameMode setado no WorldSettings")
else:
    L(f"GameMode/WS faltou: ws={ws is not None} gm={gm is not None}")

# NavMesh: precisa NavMeshBoundsVolume. spawn + escala
navcls = unreal.NavMeshBoundsVolume
nav = eas2.spawn_actor_from_class(navcls, unreal.Vector(0,37500,0))
# escala via brush? NavMeshBoundsVolume usa brush; set scale do actor aproxima
nav.set_actor_scale3d(unreal.Vector(160, 140, 30))  # ~ cobre 1500x1250m
nav.set_actor_label("WorldNav")
L("NavMeshBoundsVolume add")
# RecastNavMesh
has_recast = any("RecastNavMesh" in a.get_class().get_name() for a in eas2.get_all_level_actors())
if not has_recast:
    try:
        rc = eas2.spawn_actor_from_class(unreal.RecastNavMesh, unreal.Vector(0,0,0))
        L("RecastNavMesh add")
    except Exception as e:
        L(f"recast: {e}")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L("L_Mundo salvo c/ GameMode+Nav")
L("END")
