"""Conserta WorldBase (14x12m -> cobre mundo) + luz + render iso pra ver tudo.
Roads provam layout espalhado correto (Interior -375,0 ate Campo 375,500)."""
import unreal
L=lambda s:unreal.log(f"[FR] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

cube=unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
# remove WorldBase velho (14m) + recria grande
for a in eas.get_all_level_actors():
    if a.get_actor_label()=="WorldBase": eas.destroy_actor(a)
# mundo: X de -500 a 500 (1000m), Y de -75 a 575 (650m). centro (0,250). folga -> 1600x1400
base=eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 25000, -30))
base.set_actor_label("WorldBase")
base.static_mesh_component.set_static_mesh(cube)
# cubo=100cm. scale X=1600/1=16... nao: cubo 1m, quero 1600m -> scale 1600? cubo engine=100cm=1m, scale 1=1m. quero 1600m=scale 1600? nao, 100cm cube com scale16 =16m. ENGINE cube=100cm. scale X => X*100cm. quero 160000cm=1600m -> scale 1600? NAO: scale16=1600cm=16m. PRECISA scale1600/...
# cube 100cm * scale = tamanho. 1600m=160000cm. scale=160000/100=1600
base.set_actor_scale3d(unreal.Vector(16, 14, 0.5))  # 16*100cm=16m... ERRADO
L("ABORT — recalc scale")
L("END")
