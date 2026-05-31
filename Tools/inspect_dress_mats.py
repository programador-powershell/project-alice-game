"""Inspeciona alice-vestido.glb: tem multiplos materiais (corpo vs vestido)?
Se sim, da pra separar por material (selecionar faces que usam mat 'corpo' e deletar).
Se 1 mat soh, nao da headless — precisa pintar mascara manual."""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
m=next(o for o in bpy.data.objects if o.type=='MESH')
print(f"IM mesh '{m.name}' verts={len(m.data.vertices)} mats={len(m.data.materials)}")
for i,mat in enumerate(m.data.materials):
    if mat:
        n=mat.name
        # conta faces que usam este material
        nfaces=sum(1 for p in m.data.polygons if p.material_index==i)
        print(f"IM mat[{i}] = '{n}' faces={nfaces}")
        # texturas
        if mat.use_nodes:
            for nd in mat.node_tree.nodes:
                if nd.type=='TEX_IMAGE' and nd.image:
                    print(f"IM    tex: {nd.image.name}")
print("IM DONE")
