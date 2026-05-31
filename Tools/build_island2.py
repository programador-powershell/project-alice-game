"""Ilha CAMINHAVEL: terrenos grandes que se TOCAM (sem gap), base que preenche entre,
layout topologia world-map (castelo Patio topo-N, Campo ilha mais ao N, Interior SW).
Margem = ilha separada (tutorial). Export 1 FBX.
"""
import bpy, math, os
P=lambda s:print("I2 "+s)
HMDIR=r"E:\References\3D\heightmaps"
TILE=80.0      # cada terreno 80m (se tocam: centros 70-80m)
RELIEF=8.0
SUB=140

# layout world-map: ilha principal compacta, Margem solta no canto
# eixos: -Y = sul (inicio), +Y = norte (finale). centro=arvore floresta.
LAYOUT={
 # ilha principal (Interior -> Campo)
 "interior": ( -90, -90, 0),   # SW, inicio
 "vortice":  ( -30, -80, 0),   # leste de Interior
 "toca":     ( -90, -10, 0),   # norte de Interior
 "arena":    (  30, -50, 0),   # SE
 "floresta": ( -20, -10, 0),   # centro (arvore world-map)
 "salao":    (  70, -10, 0),   # E
 "nevoa":    ( -80,  60, 0),   # NW
 "ruinas":   (  70,  60, 0),   # NE
 "patio":    (   0,  70, 0),   # N (castelo world-map topo)
 "campo":    (   0, 150, 5),   # N+ (ilha flutuante destacada — Z elevado)
 # tutorial separado
 "margem":   (-220,-180, 0),   # SW longe (ilha solta)
}

def hpx(px,W,H,u,v,invert=True):
    x=max(0,min(W-1,int(u*(W-1)))); y=max(0,min(H-1,int(v*(H-1))))
    h=px[(y*W+x)*4]
    return (1.0-h) if invert else h

bpy.ops.wm.read_factory_settings(use_empty=True)
ok=0
for area,(ox,oy,oz) in LAYOUT.items():
    hmp=f"{HMDIR}\\hm_{area}.png"
    if not os.path.exists(hmp): P(f"skip {area}"); continue
    img=bpy.data.images.load(hmp); W,H=img.size; px=list(img.pixels)
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=SUB,y_subdivisions=SUB,size=TILE,location=(ox,oy,oz))
    g=bpy.context.active_object; g.name=f"T_{area}"
    me=g.data
    for v in me.vertices:
        u=(v.co.x/TILE+0.5); w=(v.co.y/TILE+0.5)
        v.co.z=hpx(px,W,H,u,w)*RELIEF
    for p in me.polygons: p.use_smooth=True
    bpy.data.images.remove(img)
    ok+=1; P(f"{area} @({ox},{oy},{oz})")
P(f"terrenos={ok}")

# BASE ilha principal grande organica (preenche entre terrenos, da pra andar)
# bounds da ilha principal: x -130 a 110, y -130 a 190
bpy.ops.mesh.primitive_grid_add(x_subdivisions=120,y_subdivisions=120,size=340,location=(-10,30,-2))
base=bpy.context.active_object; base.name="IslandBase"
# borda organica via wave/noise leve nas margens
tex=bpy.data.textures.new("n",'CLOUDS'); tex.noise_scale=0.5
dm=base.modifiers.new("D",'DISPLACE'); dm.texture=tex; dm.strength=3.5
bpy.ops.object.modifier_apply(modifier="D")
for p in base.data.polygons: p.use_smooth=True
P("IslandBase 340x340m sob ilha principal")

# ilha pequena pra Margem (tutorial separado)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=40,y_subdivisions=40,size=100,location=(-220,-180,-2))
mb=bpy.context.active_object; mb.name="MargemBase"
tex2=bpy.data.textures.new("n2",'CLOUDS'); tex2.noise_scale=0.4
dm2=mb.modifiers.new("D2",'DISPLACE'); dm2.texture=tex2; dm2.strength=2.5
bpy.ops.object.modifier_apply(modifier="D2")
P("MargemBase ilha tutorial")

# export
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=r"E:\References\3D\ILHA_walk.fbx",
    use_selection=True, object_types={'MESH'}, apply_unit_scale=True, mesh_smooth_type='FACE')
P("export ILHA_walk.fbx")

# render top/iso
mat=bpy.data.materials.new("c"); mat.diffuse_color=(0.78,0.78,0.8,1)
for o in bpy.data.objects:
    if o.type=='MESH': o.data.materials.append(mat)
ld=bpy.data.lights.new("S",'SUN'); ld.energy=4.0
lo=bpy.data.objects.new("S",ld); bpy.context.collection.objects.link(lo); lo.rotation_euler=(math.radians(55),0,math.radians(40))
cd=bpy.data.cameras.new("C"); cam=bpy.data.objects.new("C",cd); bpy.context.collection.objects.link(cam)
cd.type='ORTHO'; cd.ortho_scale=480
cam.location=(-10,30,500); cam.rotation_euler=(0,0,0)
bpy.context.scene.camera=cam
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.color_type='SINGLE'; sc.display.shading.single_color=(0.78,0.78,0.8)
sc.render.resolution_x=1100;sc.render.resolution_y=1100;sc.render.filepath=r"D:\ILHA2_top.png"
bpy.ops.render.render(write_still=True)
cd.type='PERSP'; cam.location=(-10,-310,260); cam.rotation_euler=(math.radians(48),0,0)
sc.render.filepath=r"D:\ILHA2_iso.png"
bpy.ops.render.render(write_still=True)
P("renders OK")
P("I2DONE")
