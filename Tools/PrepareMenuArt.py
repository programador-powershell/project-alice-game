from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"E:\References\img\cenas\cena18.png")
OUT_DIR = ROOT / "Content" / "UI" / "MainMenu" / "SourceArt"
BG_OUT = OUT_DIR / "menu_cheshire_clean.png"
ICON_OUT = OUT_DIR / "autosave_icon.png"


def cover_resize(img: Image.Image, size):
    target_w, target_h = size
    source_w, source_h = img.size
    target_ratio = target_w / target_h
    source_ratio = source_w / source_h
    if source_ratio > target_ratio:
        new_w = int(source_h * target_ratio)
        left = (source_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, source_h))
    else:
        new_h = int(source_w / target_ratio)
        top = (source_h - new_h) // 2
        img = img.crop((0, top, source_w, top + new_h))
    return img.resize(size, Image.Resampling.LANCZOS)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    src = Image.open(SOURCE).convert("RGBA")
    w, h = src.size
    bg_crop = src.crop((max(0, int(w * 0.025)), max(0, int(h * 0.085)), min(w, int(w * 0.975)), min(h, int(h * 0.885))))
    bg = cover_resize(bg_crop, (1920, 1080))
    bg = ImageEnhance.Brightness(bg).enhance(0.82)
    bg = ImageEnhance.Contrast(bg).enhance(1.12)
    bg.save(BG_OUT)

    icon_crop = src.crop((max(0, int(w * 0.012)), max(0, int(h * 0.865)), min(w, int(w * 0.090)), min(h, int(h * 0.985))))
    icon = cover_resize(icon_crop, (256, 256))
    icon = ImageEnhance.Brightness(icon).enhance(1.15)
    icon = ImageEnhance.Contrast(icon).enhance(1.25)
    alpha = icon.convert("L").point(lambda value: max(0, min(255, int((value - 18) * 2.6))))
    icon.putalpha(alpha.filter(ImageFilter.GaussianBlur(0.2)))
    icon.save(ICON_OUT)
    print("source=%s" % str(src.size))
    print("background=%s exists=%s" % (BG_OUT, BG_OUT.exists()))
    print("icon=%s exists=%s" % (ICON_OUT, ICON_OUT.exists()))


if __name__ == "__main__":
    main()
