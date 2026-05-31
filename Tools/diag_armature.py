"""Diagnostica a armature Alice-T-Pose: posicoes dos bones (esta achatada/degenerada?).
E testa auto-weight com ENVELOPE em vez de heat (heat falha em scan/non-manifold)."""
import bpy, mathutils
P = lambda s: print("DA " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\Alice-T-Pose.fbx", automatic_bone_orientation=True)
arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
P("bones=%d dims=(%.3f,%.3f,%.3f) scale=%s" % (len(arm.data.bones), arm.dimensions.x, arm.dimensions.y, arm.dimensions.z, tuple(arm.scale)))
# posicoes head/tail de alguns bones-chave
for bn in ("mixamorig:Hips","mixamorig:Spine","mixamorig:Head","mixamorig:LeftHand","mixamorig:LeftFoot","mixamorig:RightFoot"):
    b = arm.data.bones.get(bn)
    if b:
        h=b.head_local; t=b.tail_local
        P("  %s head=(%.3f,%.3f,%.3f) tail=(%.3f,%.3f,%.3f) len=%.3f" % (bn,h.x,h.y,h.z,t.x,t.y,t.z,b.length))
P("DADONE")
