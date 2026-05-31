"""Bind Eve skeletal mesh + the 7 clips onto BP_Alice so the player is animated."""
import unreal

EAL = unreal.EditorAssetLibrary
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
sk = unreal.load_asset("/Game/Alice/Characters/EveB/SK_EveB") or unreal.load_asset("/Game/Alice/Characters/Eve/SK_Eve")

ANIMS = {
    "anim_idle": "A_Eve_Idle", "anim_walk": "A_Eve_Walk", "anim_run": "A_Eve_Run",
    "anim_attack": "A_Eve_Attack", "anim_dodge": "A_Eve_Dodge",
    "anim_hit": "A_Eve_Hit", "anim_death": "A_Eve_Death",
}

if not bp or not sk:
    unreal.log_warning("[Alice] ASSIGN: missing BP_Alice or SK_Eve")
else:
    cdo = unreal.get_default_object(bp.generated_class())
    # Skeletal mesh on the inherited ACharacter "Mesh" component
    try:
        meshcomp = cdo.get_editor_property("mesh")
        meshcomp.set_skeletal_mesh_asset(sk)
        unreal.log("[Alice] ASSIGN set SK_Eve on Mesh")
    except Exception as e:
        unreal.log_warning("[Alice] ASSIGN mesh: %s" % e)
    # Clear the static proxy so the procedural-rigid path is dormant for the player
    try:
        cdo.set_editor_property("visual_mesh_asset", None)
    except Exception as e:
        unreal.log_warning("[Alice] ASSIGN visual clear: %s" % e)
    # Assign clips
    for prop, aname in ANIMS.items():
        a = unreal.load_asset("/Game/Alice/Animations/%s" % aname)
        if not a:
            unreal.log_warning("[Alice] ASSIGN missing anim %s" % aname)
            continue
        cls = a.get_class().get_name()
        unreal.log("[Alice] ASSIGN %s class=%s" % (aname, cls))
        if isinstance(a, unreal.AnimSequence):
            try:
                cdo.set_editor_property(prop, a)
            except Exception as e:
                unreal.log_warning("[Alice] ASSIGN %s set fail: %s" % (prop, e))
        else:
            unreal.log_warning("[Alice] %s is %s (not AnimSequence) - skipped" % (aname, cls))
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    except Exception as e:
        unreal.log_warning("[Alice] ASSIGN compile/save: %s" % e)
    unreal.log("[Alice] ASSIGN DONE")
