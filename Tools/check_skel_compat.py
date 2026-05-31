"""Confirma se o esqueleto dos T-Pose rigados == esqueleto dos anims (mixamorig),
e se Alice-T-Pose (so armature) bate com alice-vestido em altura/proporcao."""
import bpy, os, mathutils

def bones_of(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try: bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=True)
    except Exception as e: return None, str(e)
    arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
    if not arm: return None, "no armature"
    return [b.name for b in arm.data.bones], None

# 1. esqueleto de um anim
an, _ = bones_of(r"E:\References\model\anims\Standing Idle.fbx")
print("ANIM_BONES n=%d sample=%s" % (len(an) if an else 0, an[:6] if an else None))

# 2. esqueleto de um T-Pose rigado (coelho)
cb, _ = bones_of(r"E:\References\3D\coelho-vestidoT-Pose.fbx")
print("COELHO_BONES n=%d sample=%s" % (len(cb) if cb else 0, cb[:6] if cb else None))

# 3. esqueleto Alice-T-Pose (so armature)
ab, _ = bones_of(r"E:\References\3D\Alice-T-Pose.fbx")
print("ALICE_TPOSE_BONES n=%d sample=%s" % (len(ab) if ab else 0, ab[:6] if ab else None))

# match?
if an and cb:
    print("ANIM==COELHO ? %s" % (set(an)==set(cb)))
if an and ab:
    print("ANIM==ALICE_TPOSE ? %s" % (set(an)==set(ab)))
print("SKELCHK DONE")
