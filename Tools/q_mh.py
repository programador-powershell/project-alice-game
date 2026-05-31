import unreal
mh = sorted([a for a in dir(unreal) if 'metahuman' in a.lower()])
print("MH_CLASSES_COUNT", len(mh))
print("MH_CLASSES", mh[:60])
EAL = unreal.EditorAssetLibrary
for d in ['/Game/MetaHumans', '/Game/MetaHuman', '/MetaHuman', '/Game/Characters', '/MetaHumanCharacter']:
    try:
        print("DIR", d, EAL.does_directory_exist(d))
    except Exception as e:
        print("DIR", d, "ERR", e)
# look for any MetaHumanCharacter assets engine-wide via asset registry (limited scan)
try:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    cls_names = ['MetaHumanCharacter', 'MetaHumanWardrobeItem', 'MetaHumanCharacterPalette']
    for cn in cls_names:
        f = unreal.ARFilter(class_names=[cn], recursive_classes=True)
        a = ar.get_assets(f)
        print("ASSETS", cn, len(a))
        for x in a[:5]:
            print("   ", x.package_name)
except Exception as e:
    print("AR ERR", e)
