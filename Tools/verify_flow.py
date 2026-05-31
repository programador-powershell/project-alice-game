import unreal
LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def check(mappath, cls, prop):
    if not unreal.EditorAssetLibrary.does_asset_exist(mappath):
        print("FLOW %s MISSING" % mappath); return
    LES.load_level(mappath)
    found = False
    for a in EAS.get_all_level_actors():
        if isinstance(a, cls):
            found = True
            print("FLOW %s %s=%s" % (mappath.split('/')[-1], prop, a.get_editor_property(prop)))
    if not found:
        print("FLOW %s no-%s" % (mappath.split('/')[-1], cls.__name__))


check("/Game/Alice/Maps/L_MargemDoRio", unreal.PortalActor, "target_level")
check("/Game/Alice/Maps/L_Vortice", unreal.PortalActor, "target_level")
check("/Game/Alice/Maps/L_InteriorDeCha", unreal.PortalActor, "target_level")
check("/Game/Alice/Maps/L_TocaMecanica", unreal.PortalActor, "target_level")
check("/Game/Alice/Maps/L_Ruinas", unreal.PortalActor, "target_level")
check("/Game/Alice/Maps/L_PatioReal", unreal.BossCharacter, "next_level_name")
print("FLOW DONE")
