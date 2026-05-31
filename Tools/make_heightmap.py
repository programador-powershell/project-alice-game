"""ComfyUI python (tem PIL+torch+DepthAnything): tile relevo -> heightmap PNG limpo.
Usa Depth-Anything-V2-Large (cacheado) p/ profundidade real do diorama.
Argv: <tile> <out_hm_png>
"""
import sys
from PIL import Image, ImageFilter, ImageOps
import numpy as np

TILE, OUT = sys.argv[1], sys.argv[2]
print(f"HM tile={TILE}")

im = Image.open(TILE).convert("RGB")
# Depth-Anything profundidade
try:
    from transformers import pipeline
    import torch
    dev = 0 if torch.cuda.is_available() else -1
    pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Large-hf", device=dev)
    out = pipe(im)
    depth = out["depth"]
    arr = np.asarray(depth, dtype=np.float32)
    print(f"HM depth via DepthAnything shape={arr.shape}")
except Exception as e:
    print(f"HM depth FAIL ({e}) -> fallback grayscale")
    arr = np.asarray(im.convert("L"), dtype=np.float32)

# normaliza 0..1
arr = arr - arr.min()
if arr.max()>0: arr = arr/arr.max()
# diorama: relevo alto = claro. Depth-Anything: perto=alto. Pode precisar inverter.
# heightmap final: blur leve + resize 512
hm = Image.fromarray((arr*255).astype(np.uint8))
hm = hm.filter(ImageFilter.GaussianBlur(2))
hm = hm.resize((512,512))
hm.save(OUT)
print(f"HM saved {OUT}")
print("HMDONE")
