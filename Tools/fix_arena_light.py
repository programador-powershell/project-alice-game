"""Diagnostica intensidade das luzes do L_Arena e DA UM BOOST garantido:
Sun forte + SkyLight forte + ExponentialHeightFog leve + auto-exposure travado.
'Tudo escuro' resolvido."""
import unreal
L = lambda s: unreal.log(f"[FL] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()

def comp_of(actor, cls):
    return actor.get_component_by_class(cls)

for a in actors:
    cn = a.get_class().get_name()
    if "DirectionalLight" in cn:
        c = comp_of(a, unreal.DirectionalLightComponent)
        if c:
            old = c.get_editor_property("intensity")
            c.set_editor_property("intensity", 6.0)  # lux forte (dia)
            c.set_editor_property("light_color", unreal.Color(255,245,225,255))
            a.set_actor_rotation(unreal.Rotator(-45, 30, 0), False)
            L(f"Sun intensity {old} -> 6.0, angulo -45/30")
    elif "SkyLight" in cn:
        c = comp_of(a, unreal.SkyLightComponent)
        if c:
            old = c.get_editor_property("intensity")
            c.set_editor_property("intensity", 3.0)
            try: c.set_editor_property("source_type", unreal.SkyLightSourceType.SLS_CAPTURED_SCENE)
            except Exception: pass
            c.recapture_sky()
            L(f"SkyLight intensity {old} -> 3.0 + recapture")
    elif "PointLight" in cn:
        c = comp_of(a, unreal.PointLightComponent)
        if c:
            c.set_editor_property("intensity", 8000.0)
            c.set_editor_property("attenuation_radius", 1200.0)

# garante um SkyAtmosphere (ceu real) se nao tiver
has_atmo = any("SkyAtmosphere" in a.get_class().get_name() for a in actors)
if not has_atmo:
    atmo = eas.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0,0,0))
    L("SkyAtmosphere criado")

# PostProcessVolume com exposicao fixa (sem escurecer por auto-exposure)
ppv = None
for a in actors:
    if "PostProcessVolume" in a.get_class().get_name():
        ppv = a; break
if not ppv:
    ppv = eas.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0,0,0))
    L("PostProcessVolume criado")
ppv.set_editor_property("unbound", True)
settings = ppv.get_editor_property("settings")
settings.set_editor_property("override_auto_exposure_method", True)
settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
settings.set_editor_property("override_auto_exposure_bias", True)
settings.set_editor_property("auto_exposure_bias", 11.0)  # EV100 manual ~dia
ppv.set_editor_property("settings", settings)
L("PostProcess: exposicao MANUAL bias=11 (sem auto-escurecer)")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L("L_Arena salvo — da Play, deve estar claro")
L("END")
