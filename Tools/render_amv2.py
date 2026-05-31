import bpy, os, math, mathutils
OUT = r"D:\amv2.png"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_mixamo.fbx", automatic_bone_orientation=True)
m = next((o for o in bpy.data.objects if o.type=='MESH'), None)
pts=[m.matrix_world @ mathutils.Vector(c) for c in m.bound_box]
xs=[p.x for p in pts]; ys=[p.y for p in pts]; zs=[p.z for p in pts]
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2
size=max(max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs))
cam_d=bpy.data.cameras.new("C"); cam=bpy.data.objects.new("C",cam_d); bpy.context.collection.objects.link(cam)
cam.location=mathutils.Vector((cx, cy-size*1.7, cz)); cam.rotation_euler=(math.radians(90),0,0)
bpy.context.scene.camera=cam
ld=bpy.data.lights.new("S",'SUN'); ld.energy=3.0
lo=bpy.data.objects.new("S",ld); bpy.context.collection.objects.link(lo); lo.rotation_euler=(math.radians(50),0,math.radians(30))
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.color_type='TEXTURE'
sc.render.resolution_x=500; sc.render.resolution_y=800
sc.render.filepath=OUT
bpy.ops.render.render(write_still=True)
print("AMV2 done")
