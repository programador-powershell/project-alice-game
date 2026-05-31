"""Renderiza alice_mixamo.fbx (Blender EEVEE) frontal pra ver se e nua ou vestida.
Salva PNG pra eu confirmar visualmente."""
import bpy, os, math, mathutils
OUT = r"D:\alice_mixamo_view.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_mixamo.fbx", automatic_bone_orientation=True)
m = next((o for o in bpy.data.objects if o.type=='MESH'), None)

# bounds + camera
pts=[m.matrix_world @ mathutils.Vector(c) for c in m.bound_box]
xs=[p.x for p in pts]; ys=[p.y for p in pts]; zs=[p.z for p in pts]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2
size=max(max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs))

cam_d = bpy.data.cameras.new("C"); cam=bpy.data.objects.new("C",cam_d)
bpy.context.collection.objects.link(cam)
# frente: olha no eixo -Y (ou +Y dependendo) - usa o maior eixo horizontal
cam.location = mathutils.Vector((cx, cy - size*1.6, cz))
cam.rotation_euler = (math.radians(90),0,0)
bpy.context.scene.camera = cam

light_d=bpy.data.lights.new("S",'SUN'); light_d.energy=3.0
light=bpy.data.objects.new("S",light_d); bpy.context.collection.objects.link(light)
light.rotation_euler=(math.radians(50),0,math.radians(30))

sc=bpy.context.scene
sc.render.engine='BLENDER_EEVEE' if 'BLENDER_EEVEE' in [e.identifier for e in bpy.types.RenderEngine.__subclasses__()] else 'BLENDER_EEVEE_NEXT'
try: sc.render.engine='BLENDER_EEVEE'
except: pass
sc.render.resolution_x=600; sc.render.resolution_y=900
sc.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("AMV rendered -> %s" % OUT)
