"""Importa ILHA_walk.fbx no UE como Static Mesh (Nanite), cria L_MundoIlha,
posiciona, add luz+sky+nav+PlayerStart Interior, GameMode.
Coelho fica como player. Pronto pra Alt+P andar."""
import unreal
L=lambda s:unreal.log(f"[II] {s}")
tools=unreal.AssetToolsHelpers.get_asset_tools()

# 1. Import FBX como Static Mesh (escala metros->cm, 100x)
DST="/Game/Alice/World"
unreal.EditorAssetLibrary.make_directory(DST)
t=unreal.AssetImportTask()
t.filename=r"E:\References\3D\ILHA_walk.fbx"
t.destination_path=DST; t.destination_name="SM_Ilha"
t.replace_existing=True; t.automated=True; t.save=True
o=unreal.FbxImportUI()
o.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
o.import_mesh=True; o.import_as_skeletal=False
o.import_materials=False; o.import_textures=False
o.static_mesh_import_data.set_editor_property("import_uniform_scale", 100.0)  # m->cm
o.static_mesh_import_data.set_editor_property("combine_meshes", False)  # cada terreno = 1 SM
o.static_mesh_import_data.set_editor_property("generate_lightmap_u_vs", True)
t.options=o
tools.import_asset_tasks([t])
ar=unreal.AssetRegistryHelpers.get_asset_registry()
sms=[a for a in ar.get_assets_by_path(DST, recursive=True) if str(a.asset_class_path.asset_name)=="StaticMesh"]
L(f"static meshes importados={len(sms)}")
for a in sms: L(f"  {a.asset_name}")

# 2. cria L_MundoIlha
unreal.EditorLoadingAndSavingUtils.new_blank_map(True)
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# 3. spawna cada static mesh no level
for a in sms:
    sm=unreal.load_asset(str(a.package_name))
    if not sm: continue
    actor=eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
    actor.static_mesh_component.set_static_mesh(sm)
    actor.set_actor_label(str(a.asset_name))
    # collision
    actor.static_mesh_component.set_collision_profile_name("BlockAll")
L("terrenos spawnados no level")

# 4. luz
sun=eas.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,50000), unreal.Rotator(-50,40,0))
sun.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property("intensity",7.0)
sky=eas.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,40000))
try: sky.get_component_by_class(unreal.SkyLightComponent).set_editor_property("intensity",2.5)
except: pass
eas.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0))
ppv=eas.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0,0,0))
ppv.set_editor_property("unbound", True)
st=ppv.get_editor_property("settings")
st.set_editor_property("override_auto_exposure_method", True)
st.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
st.set_editor_property("override_auto_exposure_bias", True)
st.set_editor_property("auto_exposure_bias", 11.0)
ppv.set_editor_property("settings", st)
L("luz+sky+exposicao manual")

# 5. PlayerStart no Interior (-90,-90)m = (-9000,-9000) cm, Z elevado pra cair no terreno
ps=eas.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(-9000,-9000,1500), unreal.Rotator(0,0,0))
L("PlayerStart no Interior (-90,-90)m")

# 6. NavMeshBoundsVolume cobrindo ilha principal (-130 a +110 X, -130 a +190 Y, Z folga)
nav=eas.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(-1000, 3000, 0))
nav.set_actor_scale3d(unreal.Vector(280, 360, 50))  # *100cm
nav.set_actor_label("WorldNav")
L("NavMeshBoundsVolume add")

# 7. salvar como L_MundoIlha
ok=unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(False, False)
unreal.EditorLoadingAndSavingUtils.save_current_level()
# salvar com nome
result=unreal.EditorLoadingAndSavingUtils.save_map(unreal.EditorLevelLibrary.get_editor_world(), "/Game/Alice/Maps/L_MundoIlha")
L(f"save L_MundoIlha={result}")
L("DONE")
