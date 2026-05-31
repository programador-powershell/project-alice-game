"""Blender (sem PIL): le heightmap PNG nativo -> displace grid = terreno caminhavel.
Argv: <hm_png> <out_fbx> <out_render> <label> <relief_m>
"""
import bpy, sys, math

argv = sys.argv[sys.argv.index("--")+1:]
HM, OUT_FBX, OUT_REND, LABEL = argv[0], argv[1], argv[2], argv[3]
RELIEF = float(argv[4]) if len(argv)>4 else 5.0
P=lambda s:print("TD "+s)

bpy.ops.wm.read_factory_settings(use_empty=True)

# carrega heightmap como imagem Blender
img = bpy.data.images.load(HM)
W,H = img.size
px = list(img.pixels)  # RGBA flat
P(f"hm {W}x{H} relief={RELIEF}")

INVERT = ("--invert" in sys.argv)
def height_at(u,v):
    # u,v em 0..1
    x=int(u*(W-1)); y=int(v*(H-1))
    idx=(y*W + x)*4
    h=px[idx]  # canal R (0..1)
    return (1.0-h) if INVERT else h

# grid alta-res
SUB=300
bpy.ops.mesh.primitive_grid_add(x_subdivisions=SUB, y_subdivisions=SUB, size=40.0)
grid=bpy.context.active_object; grid.name="Terreno_"+LABEL
me=grid.data
for v in me.vertices:
    u=(v.co.x/40.0+0.5); w=(v.co.y/40.0+0.5)
    u=max(0,min(1,u)); w=max(0,min(1,w))
    v.co.z = height_at(u,w)*RELIEF
P("displaced")
for p in me.polygons: p.use_smooth=True
sol=grid.modifiers.new("S",'SOLIDIFY'); sol.thickness=2.0; sol.offset=-1.0
bpy.ops.object.modifier_apply(modifier="S")

# export
bpy.ops.object.select_all(action='DESELECT'); grid.select_set(True)
bpy.ops.export_scene.fbx(filepath=OUT_FBX, use_selection=True, object_types={'MESH'},
    apply_unit_scale=True, mesh_smooth_type='FACE')
P(f"fbx {OUT_FBX}")

# render clay iso
mat=bpy.data.materials.new("c"); mat.diffuse_color=(0.8,0.8,0.82,1); grid.data.materials.append(mat)
ld=bpy.data.lights.new("S",'SUN'); ld.energy=4.0
lo=bpy.data.objects.new("S",ld); bpy.context.collection.objects.link(lo); lo.rotation_euler=(math.radians(50),0,math.radians(40))
cd=bpy.data.cameras.new("C"); cam=bpy.data.objects.new("C",cd); bpy.context.collection.objects.link(cam)
cam.location=(36,-36,30); cam.rotation_euler=(math.radians(55),0,math.radians(45))
bpy.context.scene.camera=cam
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'
sc.render.resolution_x=900; sc.render.resolution_y=700; sc.render.filepath=OUT_REND
bpy.ops.render.render(write_still=True)
P(f"render {OUT_REND}")
P("TDDONE")
