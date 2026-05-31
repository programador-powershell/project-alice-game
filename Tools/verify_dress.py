"""Verify M_AliceDress graph wired + applied to SK_Alice. Writes UTF-8 report."""
import unreal
out = []
m = unreal.load_asset("/Game/Alice/Materials/M_AliceDress")
out.append("M_AliceDress loaded=%s" % (m is not None))
if m:
    def chk(prop):
        try:
            inp = m.get_editor_property(prop)
            ex = inp.get_editor_property("expression") if inp else None
            out.append("  %-16s connected=%s" % (prop, ex is not None))
        except Exception as e:
            out.append("  %-16s ERR %s" % (prop, e))
    for p in ["base_color", "emissive_color", "opacity_mask", "roughness"]:
        chk(p)
    try:
        out.append("  expr_count=%d" % len(m.get_expressions()))
    except Exception as e:
        out.append("  expr_count ERR %s" % e)
    try:
        out.append("  blend=%s two_sided=%s clip=%.2f" % (
            m.get_editor_property("blend_mode"),
            m.get_editor_property("two_sided"),
            m.get_editor_property("opacity_mask_clip_value")))
    except Exception as e:
        out.append("  props ERR %s" % e)
    # list scalar/vector params present
    try:
        names = [e.get_editor_property("parameter_name") for e in m.get_expressions()
                 if hasattr(e, "get_editor_property") and "Parameter" in e.get_class().get_name()]
        out.append("  params=%s" % [str(n) for n in names])
    except Exception as e:
        out.append("  params ERR %s" % e)

sk = unreal.load_asset("/Game/Alice/Characters/AliceRig/SK_Alice")
if sk:
    try:
        mats = sk.get_editor_property("materials")
        names = [(sm.get_editor_property("material_interface").get_name()
                  if sm.get_editor_property("material_interface") else "None") for sm in mats]
        out.append("SK_Alice slots=%d mats=%s" % (len(mats), names))
    except Exception as e:
        out.append("SK_Alice mats ERR %s" % e)

txt = "\n".join(out)
with open(r"E:\Alice\dress_verify.txt", "w", encoding="utf-8") as f:
    f.write(txt)
print("VERIFY DONE\n" + txt)
