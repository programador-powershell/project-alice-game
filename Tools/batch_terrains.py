"""Gera heightmap (ComfyUI python) de TODOS os 11 tiles relevo.
Roda fora do Blender (tem PIL+DepthAnything). So heightmaps; Blender displace vem depois.
"""
import sys, os
from PIL import Image, ImageFilter
import numpy as np

RELEVO=r"E:\References\img\relevo"
OUT=r"E:\References\3D\heightmaps"
os.makedirs(OUT, exist_ok=True)

# tile file -> nome area
TILES={
 "ChatGPT Image 25 de mai. de 2026, 03_07_24 (1).png":"margem",
 "ChatGPT Image 25 de mai. de 2026, 03_07_25 (8).png":"interior",
 "ChatGPT Image 25 de mai. de 2026, 03_07_25 (5).png":"vortice",
 "ChatGPT Image 25 de mai. de 2026, 03_07_25 (10).png":"toca",
 "ChatGPT Image 25 de mai. de 2026, 03_07_24 (2).png":"arena",
 "ChatGPT Image 25 de mai. de 2026, 03_07_24 (4).png":"floresta",
 "ChatGPT Image 25 de mai. de 2026, 03_07_25 (6).png":"salao",
 "ChatGPT Image 25 de mai. de 2026, 03_07_25 (7).png":"nevoa",
 "ChatGPT Image 25 de mai. de 2026, 03_07_24 (3).png":"patio",
 "ChatGPT Image 25 de mai. de 2026, 03_07_25 (9).png":"ruinas",
 "campo etereo.png":"campo",
}

from transformers import pipeline
import torch
dev=0 if torch.cuda.is_available() else -1
pipe=pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Large-hf", device=dev)
print(f"BT model loaded dev={dev}")

for fn,area in TILES.items():
    p=os.path.join(RELEVO,fn)
    if not os.path.exists(p):
        print(f"BT [{area}] MISSING {fn}"); continue
    im=Image.open(p).convert("RGB")
    out=pipe(im)
    arr=np.asarray(out["depth"],dtype=np.float32)
    arr=arr-arr.min()
    if arr.max()>0: arr=arr/arr.max()
    hm=Image.fromarray((arr*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)).resize((512,512))
    dst=os.path.join(OUT,f"hm_{area}.png")
    hm.save(dst)
    print(f"BT [{area}] -> {dst}")
print("BTDONE")
