import unreal
def meths(cls, name):
    try:
        return name + ":\n  " + "\n  ".join(sorted(m for m in dir(cls) if not m.startswith("_")))
    except Exception as e:
        return name + " ERR " + str(e)
txt = "\n\n".join([
    meths(unreal.RenderingLibrary, "RenderingLibrary"),
])
with open(r"E:\Alice\api_probe.txt", "w", encoding="utf-8") as f:
    f.write(txt)
print("PROBE DONE")
