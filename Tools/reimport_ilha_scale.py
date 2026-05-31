"""Reimporta ilha SEM import_uniform_scale (FBX ja em escala correta).
Refaz spawn no level + nav certo."""
import unreal
L=lambda s:unreal.log(f"[RI] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()

# delete velhos
import os
DST="/Game/Alice/World"
if unreal.EditorAssetLibrary.does_directory_exist(DST):
    for a in unreal.EditorAssetLibrary.list_assets(DST, recursive=True):
        try: unreal.EditorAssetLibrary.delete_asset(a)
        except: pass

# reimport sem scale=100. FBX export_scene.fbx do Blender ja aplica apply_unit_scale,
# UE deveria importar em cm respeitando isso.
t=unreal.AssetImportTask()
t.filename=r"E:\References\3D\ILHA_walk.fbx"
t.destination_path=DST; t.destination_name="SM_Ilha"
t.replace_existing=True; t.automated=True; t.save=True
o=unreal.FbxImportUI()
o.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
o.import_mesh=True; o.import_as_skeletal=False
o.import_materials=False; o.import_textures=False
o.static_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)  # SEM multiplicador
o.static_mesh_import_data.set_editor_property("combine_meshes", False)
o.static_mesh_import_data.set_editor_property("generate_lightmap_u_vs", True)
t.options=o
tools.import_asset_tasks([t])
ar=unreal.AssetRegistryHelpers.get_asset_registry()
sms=[a for a in ar.get_assets_by_path(DST, recursive=True) if str(a.asset_class_path.asset_name)=="StaticMesh"]
L(f"sms reimportados={len(sms)}")

# limpa level antigo + spawna fresh
unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_MundoIlha")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in list(eas.get_all_level_actors()):
    cn=a.get_class().get_name()
    if cn=="StaticMeshActor" or "NavMesh" in cn or "PlayerStart" in cn:
        eas.destroy_actor(a)
L("limpo level antigo")

for a in sms:
    sm=unreal.load_asset(str(a.package_name))
    if not sm: continue
    actor=eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
    actor.static_mesh_component.set_static_mesh(sm)
    actor.set_actor_label(str(a.asset_name))
    actor.static_mesh_component.set_collision_profile_name("BlockAll")

# bounds reais agora
acts=eas.get_all_level_actors()
all_b=[]
for a in acts:
    if a.get_class().get_name()=="StaticMeshActor":
        try:
            o,e=a.get_actor_bounds(False); all_b.append((o,e))
        except: pass
if all_b:
    minx=min(o.x-e.x for o,e in all_b); maxx=max(o.x+e.x for o,e in all_b)
    miny=min(o.y-e.y for o,e in all_b); maxy=max(o.y+e.y for o,e in all_b)
    minz=min(o.z-e.z for o,e in all_b); maxz=max(o.z+e.z for o,e in all_b)
    L(f"ilha REAL: X[{minx/100:.0f},{maxx/100:.0f}]m Y[{miny/100:.0f},{maxy/100:.0f}]m Z[{minz/100:.0f},{maxz/100:.0f}]m")
    cx=(minx+maxx)/2; cy=(miny+maxy)/2; cz=(minz+maxz)/2
    # PlayerStart no Interior. T_interior agora deve estar perto de (-90,-90)m sem o x100 bug
    ti=next((a for a in acts if a.get_actor_label()=="SM_Ilha_T_interior"), None)
    if ti:
        oi,ei=ti.get_actor_bounds(False)
        ps_loc=unreal.Vector(oi.x, oi.y, oi.z+ei.z+200)  # 2m acima
        ps=eas.spawn_actor_from_class(unreal.PlayerStart, ps_loc, unreal.Rotator(0,0,0))
        L(f"PlayerStart @ ({ps_loc.x/100:.0f},{ps_loc.y/100:.0f},{ps_loc.z/100:.0f})m (T_interior topo+2m)")
    # NavBounds proporcional
    nav=eas.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(cx,cy,cz))
    sx=(maxx-minx)/200+5; sy=(maxy-miny)/200+5; sz=(maxz-minz)/200+10
    nav.set_actor_scale3d(unreal.Vector(sx,sy,sz))
    nav.set_actor_label("WorldNav")
    L(f"NavBounds scale=({sx:.0f},{sy:.0f},{sz:.0f})")

unreal.EditorLoadingAndSavingUtils.save_current_level()
unreal.SystemLibrary.execute_console_command(None, "RebuildNavigation")
L("salvo + nav rebuild")
L("END")
