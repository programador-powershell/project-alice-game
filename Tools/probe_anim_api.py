"""Descobre os nomes corretos de factories/classes de anim no UE 5.7."""
import unreal
L = lambda s: unreal.log(f"[API] {s}")

for name in ["BlendSpaceFactory1D","BlendSpaceFactoryNew","BlendSpaceFactory",
             "AnimBlueprintFactory","AnimBlueprint","BlendSpace1D","BlendSpace"]:
    has = hasattr(unreal, name)
    L(f"  unreal.{name} = {'EXISTE' if has else 'NAO'}")

# lista todas que tem 'BlendSpace' ou 'AnimBlueprint' no nome
import unreal as u
allnames = [n for n in dir(u) if 'BlendSpace' in n or 'AnimBlueprint' in n or 'AnimationAsset' in n]
L(f"  relacionados: {allnames}")
L("END")
