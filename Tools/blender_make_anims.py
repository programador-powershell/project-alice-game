"""
Author best-effort animation clips on Eve's Mixamo rig and export one FBX per clip to
E:\model\anims\ for import to UE. Clips: Idle, Walk, Run, Attack, Dodge, Hit, Death.
(Blind-authored on standard mixamorig bone names; iterate after seeing in-engine.)
"""
import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"E:\model\Eve.fbx")

arm = next((o for o in bpy.data.objects if o.type == 'ARMATURE'), None)
if not arm:
    print("ANIM ERROR: no armature")
    raise SystemExit

OUT = r"E:\model\anims"
os.makedirs(OUT, exist_ok=True)

B = "mixamorig:"
bpy.context.view_layer.objects.active = arm


def rad(d):
    return math.radians(d)


def key(bone, f, x=0.0, y=0.0, z=0.0):
    pb = arm.pose.bones.get(B + bone)
    if not pb:
        return
    pb.rotation_mode = 'XYZ'
    pb.rotation_euler = (rad(x), rad(y), rad(z))
    pb.keyframe_insert('rotation_euler', frame=f)


def keyloc(bone, f, x=0.0, y=0.0, z=0.0):
    pb = arm.pose.bones.get(B + bone)
    if not pb:
        return
    pb.location = (x, y, z)
    pb.keyframe_insert('location', frame=f)


def start(name):
    arm.animation_data_clear()
    arm.animation_data_create()
    act = bpy.data.actions.new(name)
    arm.animation_data.action = act
    # reset the bones we touch to rest at frame 1
    for b in ["Hips", "Spine", "Spine1", "Spine2", "Neck", "Head",
              "LeftArm", "LeftForeArm", "RightArm", "RightForeArm",
              "LeftUpLeg", "LeftLeg", "RightUpLeg", "RightLeg"]:
        key(b, 1, 0, 0, 0)
    return act


def export(name, last):
    sc = bpy.context.scene
    sc.frame_start = 1
    sc.frame_end = last
    for o in bpy.data.objects:
        o.select_set(o.type in ('ARMATURE', 'MESH'))
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.fbx(
        filepath=os.path.join(OUT, name + ".fbx"),
        use_selection=True, add_leaf_bones=False, bake_anim=True,
        bake_anim_use_all_actions=False, bake_anim_step=1.0,
        object_types={'ARMATURE', 'MESH'})
    print("ANIM exported %s (1-%d)" % (name, last))


# ---- Skeletal mesh (mesh + armature, rest pose) for a Blender-consistent skeleton ----
arm.animation_data_clear()
for _o in bpy.data.objects:
    _o.select_set(_o.type in ('ARMATURE', 'MESH'))
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, "Eve_Skel.fbx"), use_selection=True,
                         add_leaf_bones=False, bake_anim=False, object_types={'ARMATURE', 'MESH'})
print("ANIM exported Eve_Skel (mesh+armature)")

# ---- IDLE (60f loop): lower arms from T-pose, gentle sway ----
start("Eve_Idle")
for f in (1, 60):
    key("LeftArm", f, 0, 0, 62); key("RightArm", f, 0, 0, -62)
    key("LeftForeArm", f, 0, 0, 10); key("RightForeArm", f, 0, 0, -10)
key("Spine", 30, 4, 0, 0)
key("LeftArm", 30, 0, 0, 66); key("RightArm", 30, 0, 0, -66)
export("Eve_Idle", 60)

# ---- WALK (30f loop): arms down + alternating leg/arm swing ----
start("Eve_Walk")
for f in (1, 30):
    key("LeftArm", f, 0, 0, 62); key("RightArm", f, 0, 0, -62)
# phase A (f1) and mirror (f15), back to A (f30)
key("LeftUpLeg", 1, 28, 0, 0); key("RightUpLeg", 1, -28, 0, 0)
key("LeftLeg", 1, -10, 0, 0); key("RightLeg", 1, 35, 0, 0)
key("LeftArm", 1, -22, 0, 62); key("RightArm", 1, 22, 0, -62)
key("LeftUpLeg", 15, -28, 0, 0); key("RightUpLeg", 15, 28, 0, 0)
key("LeftLeg", 15, 35, 0, 0); key("RightLeg", 15, -10, 0, 0)
key("LeftArm", 15, 22, 0, 62); key("RightArm", 15, -22, 0, -62)
key("LeftUpLeg", 30, 28, 0, 0); key("RightUpLeg", 30, -28, 0, 0)
key("LeftLeg", 30, -10, 0, 0); key("RightLeg", 30, 35, 0, 0)
key("LeftArm", 30, -22, 0, 62); key("RightArm", 30, 22, 0, -62)
export("Eve_Walk", 30)

# ---- RUN (22f loop): bigger swing + forward lean ----
start("Eve_Run")
for f in (1, 22):
    key("Spine", f, 14, 0, 0)
    key("LeftArm", f, 0, 0, 55); key("RightArm", f, 0, 0, -55)
    key("LeftForeArm", f, -70, 0, 0); key("RightForeArm", f, -70, 0, 0)
key("LeftUpLeg", 1, 45, 0, 0); key("RightUpLeg", 1, -40, 0, 0)
key("LeftLeg", 1, -15, 0, 0); key("RightLeg", 1, 70, 0, 0)
key("LeftArm", 1, -40, 0, 55); key("RightArm", 1, 40, 0, -55)
key("LeftUpLeg", 11, -40, 0, 0); key("RightUpLeg", 11, 45, 0, 0)
key("LeftLeg", 11, 70, 0, 0); key("RightLeg", 11, -15, 0, 0)
key("LeftArm", 11, 40, 0, 55); key("RightArm", 11, -40, 0, -55)
key("LeftUpLeg", 22, 45, 0, 0); key("RightUpLeg", 22, -40, 0, 0)
key("LeftLeg", 22, -15, 0, 0); key("RightLeg", 22, 70, 0, 0)
key("LeftArm", 22, -40, 0, 55); key("RightArm", 22, 40, 0, -55)
export("Eve_Run", 22)

# ---- ATTACK (20f): right arm raise then chop across ----
start("Eve_Attack")
for f in (1, 20):
    key("LeftArm", f, 0, 0, 62)
key("RightArm", 1, 0, 0, -62)
key("RightArm", 6, -120, 0, -30); key("RightForeArm", 6, -50, 0, 0)
key("Spine", 6, 0, 0, -20)
key("RightArm", 12, 40, 0, -90); key("RightForeArm", 12, -10, 0, 0)
key("Spine", 12, 0, 0, 25)
key("RightArm", 20, 0, 0, -62); key("Spine", 20, 0, 0, 0)
export("Eve_Attack", 20)

# ---- DODGE (24f): crouch + full spin via hips ----
start("Eve_Dodge")
for f in (1, 24):
    key("LeftArm", f, 0, 0, 62); key("RightArm", f, 0, 0, -62)
key("Hips", 1, 0, 0, 0); key("Hips", 12, 0, 180, 0); key("Hips", 24, 0, 360, 0)
key("Spine", 6, 25, 0, 0); key("Spine", 12, 35, 0, 0); key("Spine", 18, 25, 0, 0)
key("LeftUpLeg", 12, 50, 0, 0); key("RightUpLeg", 12, 50, 0, 0)
export("Eve_Dodge", 24)

# ---- HIT (12f): torso + head jerk back ----
start("Eve_Hit")
for f in (1, 12):
    key("LeftArm", f, 0, 0, 62); key("RightArm", f, 0, 0, -62)
key("Spine", 4, -22, 0, 0); key("Head", 4, -20, 0, 0)
key("Spine", 12, 0, 0, 0); key("Head", 12, 0, 0, 0)
export("Eve_Hit", 12)

# ---- DEATH (34f): fold forward, collapse ----
start("Eve_Death")
key("Hips", 1, 0, 0, 0)
key("Hips", 20, 70, 0, 0); key("Spine", 20, 30, 0, 0); key("Spine1", 20, 25, 0, 0)
key("LeftUpLeg", 20, 60, 0, 0); key("RightUpLeg", 20, 60, 0, 0)
key("Hips", 34, 88, 0, 0); key("Spine", 34, 35, 0, 0)
key("LeftArm", 34, -20, 0, 62); key("RightArm", 34, 20, 0, -62)
export("Eve_Death", 34)

print("ANIM ALL DONE")
