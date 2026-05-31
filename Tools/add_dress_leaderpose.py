"""Add SK_AliceDress como SkeletalMeshComponent child do BP_Alice,
com Leader Pose Component = mesh corpo. Vestido segue anim do corpo.
Usa SubobjectDataSubsystem (UE5.7)."""
import unreal
L = lambda s: unreal.log(f"[LP] {s}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
dress = unreal.load_asset("/Game/Alice/Characters/AliceDress2/SK_AliceDress")
L(f"bp={'OK' if bp else 'NULL'} dress={'OK' if dress else 'NULL'}")

sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
handles = sds.k2_gather_subobject_data_for_blueprint(bp)
L(f"subobjects={len(handles)}")

# acha o root component (CharacterMesh0 / Mesh) p/ parentear
root_handle=None
dress_exists=False
for h in handles:
    d=sds.k2_find_subobject_data_from_handle(h)
    obj=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(d)
    if obj:
        n=obj.get_name()
        if "DressMeshComp" in n: dress_exists=True
        if n in ("CharacterMesh0","Mesh") or (hasattr(obj,'get_class') and obj.get_class().get_name()=="SkeletalMeshComponent" and "Visual" not in n):
            if root_handle is None: root_handle=h

if dress_exists:
    L("DressMeshComp ja existe, skip add")
else:
    # add novo SkeletalMeshComponent
    sub_params=unreal.AddNewSubobjectParams(
        parent_handle=handles[0],
        new_class=unreal.SkeletalMeshComponent,
        blueprint_context=bp)
    new_handle, fail = sds.add_new_subobject(sub_params)
    if str(fail)!="":
        L(f"add fail: {fail}")
    else:
        sds.rename_subobject(new_handle, unreal.Text("DressMeshComp"))
        nd=sds.k2_find_subobject_data_from_handle(new_handle)
        comp=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(nd)
        comp.set_editor_property("skeletal_mesh_asset", dress)
        L("DressMeshComp criado + mesh=SK_AliceDress")

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP salvo")
L("NOTA: Leader Pose set em runtime no C++/BeginPlay OU set_leader_pose_component no construction")
L("DONE")
