"""Conecta as 10 areas do L_Mundo com PONTES (corredores) nas arestas do grafo
do roteiro + chao base sob tudo. Seamless: anda de uma area a outra por terra.
Mesh = cubo engine esticado. Material pedra simples."""
import unreal, math
L = lambda s: unreal.log(f"[CW] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# centros (m) — mesmo layout do build_world
S=250.0
C = {
 "Interior":(-2*S,0),"Vortice":(-1*S,0),"Toca":(0,0),"Arena":(1*S,0),"Floresta":(2*S,0),
 "Salao":(1*S,1*S),"Nevoa":(2*S,1*S),"Patio":(1*S,2*S),"Ruinas":(2*S,2*S),"Campo":(2*S,3*S),
}
edges = [
 ("Interior","Vortice"),("Vortice","Toca"),("Toca","Arena"),("Arena","Floresta"),
 ("Arena","Salao"),("Floresta","Nevoa"),("Nevoa","Salao"),
 ("Salao","Patio"),("Patio","Ruinas"),("Patio","Campo"),("Ruinas","Campo"),
]

cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
L(f"cube={'OK' if cube else 'MISS'}")

# material pedra (reusa um existente do projeto, senao None)
mat = None
for mp in ("/Game/Alice/Materials/M_Stone","/Game/Alice/Materials/M_AliceDress"):
    m=unreal.EditorAssetLibrary.load_asset(mp)
    if m: mat=m; break

ROADW = 8.0  # largura corredor (m)
made=0
for a,b in edges:
    ax,ay=C[a]; bx,by=C[b]
    midx=(ax+bx)/2*100; midy=(ay+by)/2*100
    dx=bx-ax; dy=by-ay
    length=math.hypot(dx,dy)  # m
    yaw=math.degrees(math.atan2(dy,dx))
    act=eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(midx,midy,-20))
    act.set_actor_label(f"Road_{a}_{b}")
    smc=act.static_mesh_component
    smc.set_static_mesh(cube)
    if mat: smc.set_material(0,mat)
    # cubo engine=100cm. escala: comprimento x larg x fino
    act.set_actor_scale3d(unreal.Vector(length/1.0, ROADW, 0.4))
    act.set_actor_rotation(unreal.Rotator(0,yaw,0),False)
    made+=1
    L(f"  road {a}->{b} len={length:.0f}m yaw={yaw:.0f}")

# chao base grande sob tudo (capta quedas)
xs=[v[0] for v in C.values()]; ys=[v[1] for v in C.values()]
cx=(min(xs)+max(xs))/2*100; cy=(min(ys)+max(ys))/2*100
spanx=(max(xs)-min(xs)+400); spany=(max(ys)-min(ys)+400)  # +folga
base=eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(cx,cy,-60))
base.set_actor_label("WorldBase")
bsmc=base.static_mesh_component
bsmc.set_static_mesh(cube)
if mat: bsmc.set_material(0,mat)
base.set_actor_scale3d(unreal.Vector(spanx/100.0, spany/100.0, 0.5))
L(f"WorldBase {spanx/100:.0f}x{spany/100:.0f}m")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L(f"L_Mundo salvo. pontes={made} + base")
L("END")
