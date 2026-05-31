"""Compara NOMES de bones: Alice-T-Pose (rig oficial da Alice) vs Standing Idle (anim).
Se os 49 do Alice forem subconjunto dos 65 do anim (mesmos nomes mixamorig), os anims
funcionam no rig da Alice (UE mapeia por nome; dedos extras ignorados)."""
import bpy

def bones_of(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False)
    arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
    return set(b.name for b in arm.data.bones) if arm else set()

alice = bones_of(r"E:\References\3D\Alice-T-Pose.fbx")
anim  = bones_of(r"E:\References\model\anims\Standing Idle.fbx")

print("CMP alice_bones=%d anim_bones=%d" % (len(alice), len(anim)))
print("CMP alice_subset_de_anim? %s" % alice.issubset(anim))
faltam = alice - anim
extra = anim - alice
print("CMP no_alice_mas_nao_anim(%d): %s" % (len(faltam), sorted(faltam)[:10]))
print("CMP no_anim_mas_nao_alice(%d): %s" % (len(extra), sorted(extra)[:15]))
print("CMP DONE")
