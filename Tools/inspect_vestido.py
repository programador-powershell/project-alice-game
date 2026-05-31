"""Inspeciona alice-vestido.glb: meshes, verts, materiais/texturas embutidas, dims, armature."""
import bpy, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")

meshes = [o for o in bpy.data.objects if o.type=='MESH']
arms = [o for o in bpy.data.objects if o.type=='ARMATURE']
print("VEST meshes=%d armatures=%d" % (len(meshes), len(arms)))
for m in meshes:
    vg = len(m.vertex_groups)
    print("VEST mesh '%s' verts=%d mats=%d vgroups=%d dims=(%.2f,%.2f,%.2f)" % (
        m.name, len(m.data.vertices), len(m.data.materials), vg,
        m.dimensions.x, m.dimensions.y, m.dimensions.z))
    for mat in m.data.materials:
        if mat:
            tex = []
            if mat.use_nodes:
                for n in mat.node_tree.nodes:
                    if n.type=='TEX_IMAGE' and n.image:
                        tex.append(n.image.name)
            print("   mat '%s' textures=%s" % (mat.name, tex))
for a in arms:
    print("VEST armature '%s' bones=%d" % (a.name, len(a.data.bones)))
print("VEST DONE")
