"""PILOTO: tile relevo Vortice -> heightmap -> terreno caminhavel (grid displaced).
Argv: <tile_png> <out_fbx> <out_render> <label>
Metodo: grayscale + blur -> displace grid 400x400 + base solida. Render clay top+persp.
"""
import bpy, sys, os, math, mathutils
from PIL import Image, ImageFilter, ImageOps
import numpy as np

argv = sys.argv[sys.argv.index("--")+1:]
TILE, OUT_FBX, OUT_REND, LABEL = argv[0], argv[1], argv[2], argv[3]
P=lambda s:print("TR "+s)

# 1. tile -> heightmap (grayscale, blur, normaliza, crop bordas brancas)
im = Image.open(TILE).convert("L")
# auto-crop fundo branco/cinza claro uniforme (borda do diorama)
im = ImageOps.autocontrast(im, cutoff=2)
im = im.filter(ImageFilter.GaussianBlur(3))
im = im.resize((400,400))
arr = np.asarray(im, dtype=np.float32)/255.0
P(f"heightmap {arr.shape} min={arr.min():.2f} max={arr.max():.2f}")

# 2. grid displaced
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=400, y_subdivisions=400, size=20.0)
grid = bpy.context.active_object
grid.name = "Terreno"
me = grid.data
W = 400
RELIEF = 4.0  # altura max do relevo (m)
for v in me.vertices:
    # mapeia x,y do vert (-10..10) -> pixel
    px = int((v.co.x/20.0 + 0.5)*(W-1))
    py = int((0.5 - v.co.y/20.0)*(W-1))  # flip Y
    px=max(0,min(W-1,px)); py=max(0,min(W-1,py))
    v.co.z = arr[py,px]*RELIEF
P("grid displaced")

# 3. suaviza shading + base solida (solidify p/ ter fundo, caminhavel)
for p in me.polygons: p.use_smooth = True
sol = grid.modifiers.new("Sol",'SOLIDIFY'); sol.thickness=1.5; sol.offset=-1.0
bpy.ops.object.modifier_apply(modifier="Sol")

# 4. export FBX
bpy.ops.object.select_all(action='DESELECT')
grid.select_set(True)
bpy.ops.export_scene.fbx(filepath=OUT_FBX, use_selection=True, object_types={'MESH'},
    apply_unit_scale=True, mesh_smooth_type='FACE')
P(f"export {OUT_FBX}")

# 5. render clay top + persp
mat = bpy.data.materials.new("clay"); mat.use_nodes=False; mat.diffuse_color=(0.8,0.8,0.82,1)
grid.data.materials.append(mat)
# luz
ld=bpy.data.lights.new("S",'SUN'); ld.energy=4.0
lo=bpy.data.objects.new("S",ld); bpy.context.collection.objects.link(lo); lo.rotation_euler=(math.radians(50),0,math.radians(40))
# camera iso
cd=bpy.data.cameras.new("C"); cam=bpy.data.objects.new("C",cd); bpy.context.collection.objects.link(cam)
cam.location=(18,-18,16); cam.rotation_euler=(math.radians(55),0,math.radians(45))
bpy.context.scene.camera=cam
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'
sc.render.resolution_x=900; sc.render.resolution_y=700
sc.render.filepath=OUT_REND
bpy.ops.render.render(write_still=True)
P(f"render {OUT_REND}")
P("TRDONE")
