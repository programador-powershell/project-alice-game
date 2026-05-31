"""Monta ILHA UNICA: 11 terrenos (heightmap displaced --invert) posicionados conforme
world-map (organico) + base ilha + caminhos sinuosos ligando. Export 1 FBX grande.
Layout segue grafo: Interior(inicio,SW) -> ... -> Campo(finale, topo/N).
"""
import bpy, sys, math, mathutils

P=lambda s:print("ISL "+s)
HMDIR=r"E:\References\3D\heightmaps"
TILE=70.0      # tamanho de cada terreno (m) — maior, areas se tocam
RELIEF=5.0
SUB=160        # subdiv por tile

# layout conforme world-map (ilha organica). pos (x,y) em m, espacados ~TILE
# world-map: areas fundidas. uso posicoes do grafo mas mais juntas (overlap leve = funde)
LAYOUT={
 "interior":(-80,-80),  # inicio SW
 "vortice":(-40,-70),
 "toca":(-80,-30),
 "arena":(0,-40),
 "floresta":(-40,-20),  # centro (arvore central do world-map)
 "salao":(40,-30),
 "nevoa":(-90,20),
 "patio":(0,40),        # topo central (castelo do world-map)
 "ruinas":(60,20),
 "campo":(0,90),        # finale topo N (ilha flutuante)
 "margem":(-120,-110),  # tutorial separado, canto
}

def height_at(px, W, H, u, v, invert=True):
    x=int(u*(W-1)); y=int(v*(H-1)); x=max(0,min(W-1,x)); y=max(0,min(H-1,y))
    h=px[(y*W+x)*4]
    return (1.0-h) if invert else h

bpy.ops.wm.read_factory_settings(use_empty=True)
made=[]
for area,(ox,oy) in LAYOUT.items():
    hmp=f"{HMDIR}\\hm_{area}.png"
    import os
    if not os.path.exists(hmp): P(f"skip {area} sem hm"); continue
    img=bpy.data.images.load(hmp); W,H=img.size; px=list(img.pixels)
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=SUB,y_subdivisions=SUB,size=TILE,
        location=(ox,oy,0))
    g=bpy.context.active_object; g.name=f"T_{area}"
    me=g.data
    for vv in me.vertices:
        u=(vv.co.x/TILE+0.5); w=(vv.co.y/TILE+0.5)
        vv.co.z=height_at(px,W,H,max(0,min(1,u)),max(0,min(1,w)))*RELIEF
    for p in me.polygons: p.use_smooth=True
    made.append(g.name)
    bpy.data.images.remove(img)
    P(f"{area} @({ox},{oy})")
P(f"terrenos={len(made)}")

# base ilha: plano grande sob tudo, displace organico leve (clouds) p/ borda natural
bpy.ops.mesh.primitive_grid_add(x_subdivisions=120,y_subdivisions=120,size=320,location=(0,0,-3))
base=bpy.context.active_object; base.name="IslandBase"
# noise displace leve
tex=bpy.data.textures.new("n",'CLOUDS'); tex.noise_scale=0.6
dm=base.modifiers.new("D",'DISPLACE'); dm.texture=tex; dm.strength=4.0
bpy.ops.object.modifier_apply(modifier="D")
for p in base.data.polygons: p.use_smooth=True
P("base ilha")

# export tudo
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=r"E:\References\3D\ILHA_mundo.fbx",
    use_selection=True, object_types={'MESH'}, apply_unit_scale=True, mesh_smooth_type='FACE')
P("export ILHA_mundo.fbx")

# render top
mat=bpy.data.materials.new("c"); mat.diffuse_color=(0.78,0.78,0.8,1)
for o in bpy.data.objects:
    if o.type=='MESH': o.data.materials.append(mat)
ld=bpy.data.lights.new("S",'SUN'); ld.energy=4.0
lo=bpy.data.objects.new("S",ld); bpy.context.collection.objects.link(lo); lo.rotation_euler=(math.radians(55),0,math.radians(40))
cd=bpy.data.cameras.new("C"); cam=bpy.data.objects.new("C",cd); bpy.context.collection.objects.link(cam)
cd.type='ORTHO'; cd.ortho_scale=380
cam.location=(0,0,400); cam.rotation_euler=(0,0,0)
bpy.context.scene.camera=cam
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'
sc.render.resolution_x=1000;sc.render.resolution_y=1000;sc.render.filepath=r"D:\ILHA_top.png"
bpy.ops.render.render(write_still=True)
P("render top D:\\ILHA_top.png")
# render iso
cd.type='PERSP'; cam.location=(0,-280,260); cam.rotation_euler=(math.radians(48),0,0)
sc.render.filepath=r"D:\ILHA_iso.png"
bpy.ops.render.render(write_still=True)
P("render iso D:\\ILHA_iso.png")
P("ISLDONE")
