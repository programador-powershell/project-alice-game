# 04 — Color Palettes & VFX Briefs
**Project Alice** | Dark-Fantasy Soulslike | UE5.7 Niagara / Lumen  
*Source: Bíblia Técnica de Cores (8 palette sheets) + VFX reference sheets*

---

## 1. Master Palette DNA

The global color language is built on a **near-black base** (`#0A0A0F` – `#14101A`) with **saturated jewel-tone accent layers** per area. Gold (`#C9962A` – `#E8B84B`) is the universal edge-lighting and UI metal. Contrast & legibility rule: every area has exactly one dominant hue that owns its mid-range luminosity, everything else is either near-black shadow or bright accent spark.

---

## 2. Per-Area Palette Table

| # | Area / Scene | Name | Dominant Hex Swatches | Mood |
|---|---|---|---|---|
| 1 | **Origin — Riverbank** (Cena 01) | Riverbank Gold | `#6B5728` `#9B7D3A` `#C9962A` `#3B2A14` `#1A1208` | Nostalgic warmth, decaying daylight, pre-fall sepia |
| 2 | **Cheshire Forest / Toca** (Cena 02) | Cheshire Forest Purple/Teal | `#2A1A3E` `#4B2D6B` `#1A3A35` `#3D7A6B` `#0F0F1A` | Oppressive magic, bioluminescent undergrowth, teal underglow |
| 3 | **Clockwork Abyss / Abismo Temporal** (Cena 03) | Clockwork Blue | `#1A2B4A` `#2D4A7A` `#4A7AB5` `#8AB4D4` `#C8D8E8` | Cold machinery, temporal dissonance, steel-blue precision |
| 4 | **Distorted Interior** (Cena 04) | Interior Distorted | `#1A1228` `#2E1A3A` `#0A0A14` `#5A3A6B` `#8B5E9A` | Psychological dread, deep violet compression, no warmth |
| 5 | **Ruptura da Sala** (Cena 05) | Vortex Purple/Magenta | `#3A0A4A` `#6B1A7A` `#A020C0` `#C840E8` `#F060FF` | Reality fracture, neon corruption bloom, electric magenta |
| 6 | **Limiar / Passagem** (Cena 06) | Threshold Teal | `#0A1A1A` `#1A3A3A` `#2A6060` `#4A9090` `#80C0C0` | Liminal dread, cold aqua mist, transition anxiety |
| 7 | **Corredor Branco / Temporal** (Cena 07) | Ethereal White/Gold | `#E8E0D0` `#C8B870` `#A09060` `#FFFFFF` `#1A1A2A` | Fractured time, bleached light, spectral gold veins |
| 8 | **Caminho Desfigurado** (Cena 08) | Shadow Void | `#0A0814` `#1A1228` `#2A1A3A` `#503A5A` `#8060A0` | Existential void, corrupted-self mirror, desaturated purple |
| 9 | **Floresta do Cheshire / Revelação** (Cena 09) | Cheshire Forest Teal + Cyan | `#0F2A2A` `#1A5050` `#20A080` `#40D0A0` `#7AFFD0` | Bioluminescent danger, cat-grin cyan, predatory beauty |
| 10 | **Cogumelo / Lagarta** (Cena 10 + 13) | Mushroom Blue | `#0A1428` `#1A2850` `#2040A0` `#4060D0` `#60A0F0` | Psychedelic calm-to-threat, blue smoke, spore depth |
| 11 | **Chapeleiro / Sala de Chá** (Cena 11 + 14) | Hatter Green | `#0A1A0A` `#1A3A1A` `#2A6A2A` `#50A050` `#80D080` | Manic hospitality, viridian poison, green-gold highlight |
| 12 | **Rainha de Copas / Boss Arena** (Cenas 12 + 15) | Queen Crimson | `#1A0000` `#3A0808` `#7A1010` `#C01818` `#FF2020` | Execution authority, hot crimson, black-shadow dominance |
| 13 | **Caminho Entre Ruína e Luz** (Cena 16) | Transition Silver | `#1A1A28` `#3A3A5A` `#6A6A9A` `#A0A0C0` `#D0D0E8` | Hope threading dread, silver-violet dawn, motif convergence |
| 14 | **Encontro Final** (Cena 17) | Reunion White/Floral | `#FAFAF8` `#E8E0D8` `#D0C8B8` `#B8A890` `#9890A0` | Catharsis, de-saturated bloom, soft white petals, emotional resolution |

### Universal Cross-Area Rules
- **Shadow base**: always `#0A0A0F` – `#14101A`; never pure black
- **Gold accent**: `#C9962A` – `#E8B84B` — used on ALL UI chrome, weapon edges, Gothic filigree
- **Corruption tint**: dark violet `#2A0A3A` bleeds into every area as Alice's sanity drops
- **Lumen GI bias**: each area has a single dominant bounce-light color; mix only at border transitions

---

## 3. Per-Character Costume Colors

| Costume | Primary | Secondary | Accent / FX |
|---|---|---|---|
| Alice — Base / Coelho Branco | `#F0ECE8` white dress | `#1A1228` black corset | `#8080D0` blue-violet petals |
| Alice — Cheshire | `#2A1A3E` deep purple | `#4B2D6B` violet | `#20D0A0` teal sparks |
| Alice — Chapeleiro | `#1A3A1A` dark green | `#50A050` viridian | `#C09820` gold/amber |
| Alice — Lagarta Azul | `#0A1428` midnight | `#2040A0` cobalt | `#60A0F0` electric blue smoke |
| Alice — Rainha de Copas | `#1A0000` near-black | `#7A1010` deep crimson | `#FF2020` blood-red bloom |

---

## 4. VFX Briefs — Niagara Design Targets

### 4.1 ROSE DRIFT (Signature Dodge — Core Mechanic)

> "Alice rapidamente se transforma em um turbilhão de pétalas, atravessando o espaço." — In-game description

**Concept parity:** Equivalent to Black Myth Wukong's dodge clone — the game's most-seen VFX, must be instant-read AND beautiful at 60 fps.

#### 4.1.1 Trigger & Timing

| Phase | Duration | What Happens |
|---|---|---|
| **0 — Input** | 0 ms | No wind-up; instant on press |
| **1 — Dissolve** | 0–80 ms | Alice's mesh dissolves FROM periphery inward — dress hem first, then skirt body, then torso, head last |
| **2 — Petal Burst** | 80–180 ms | Full petal cloud at origin point; peak density frame |
| **3 — Drift Travel** | 180–350 ms | Cloud streams directionally; reads as elongated teardrop in motion |
| **4 — Reconstitution** | 350–480 ms | Petals compress at destination; Alice reforms torso-first |
| **5 — After-image Fade** | 480–700 ms | Ghost silhouette at origin lingers, fades to 0 opacity |

#### 4.1.2 Petal Properties (per costume — Niagara emitter override table)

| Costume | Petal Color | Petal Alpha | Secondary Particle | Notes |
|---|---|---|---|---|
| Coelho Branco (default) | `#D0CCE8` pale blue-violet | 0.7 | Faint blue temporal distortions, temporary | Coolest / most elegant |
| Cheshire | `#8B1A8B` deep rose + `#20D0A0` teal sparks | 0.8 | Teal wisps and shadows surge | Dark + luminous contrast |
| Chapeleiro | `#50A050` green + `#C09820` gold tea objects | 0.75 | Tea cups, clock fragments orbit | Most chaotic / Hatter energy |
| Lagarta Azul | `#4060D0` cobalt + `#80C0F0` smoke | 0.85 | Blue smoke columns + petal forms | Smoky / heaviest emitter |
| Rainha de Copas | `#C01818` blood crimson + `#FF2020` bright | 0.9 | Blood-tinted petals, brief gore sparks | Most aggressive / dangerous read |

#### 4.1.3 Petal Shape & Physical Properties

- **Shape**: Stylized 5-petal rose bloom, ~3–8 cm world-space, slight transparency gradient toward tip edge
- **Count**: 120–200 petals at peak burst (optimize with GPU instancing)
- **Tumble**: Each petal has independent rotational velocity (15–90 °/s random), no two spin the same axis
- **Velocity inherit**: 40 % of Alice's movement vector transferred to petal stream; creates visible directionality
- **Curl noise**: Apply low-frequency curl noise field (0.5 Hz) to petal cluster for organic drift, NOT straight-line travel
- **Scale**: Petals start at 120 % scale on burst, decay to 60 % by end of drift, re-expand slightly on reconstitution

#### 4.1.4 After-Image (Silhouette Ghost)

- Render Alice's full skeletal pose at dodge-start as a **translucent unlit mesh** — no albedo texture, solid color only
- Color: `#6060A0` blue-grey (default), shifts per costume (Cheshire: `#3A0A5A` deep violet; Queen: `#600000` dark red)
- Opacity curve: 60 % at spawn → 0 % at 700 ms, ease-out cubic
- **No normal map on ghost** — pure silhouette, emissive rim only
- Rim emissive: `#A0A0FF` at 0.8 intensity, 2-px screen-space thickness
- The ghost MUST remain at world-space origin — does not follow Alice's travel; this is the deception/confusion mechanic

#### 4.1.5 Trail

- Particle ribbon ribbon emitter along travel path
- Color: gradient from dominant petal color → transparent, length 0.8 m at peak travel
- Bloom: HDR over-bright petal tips (emissive value 1.5) produce natural bloom via Lumen without extra passes
- No depth-fade required — petals occlude naturally in scene geometry

#### 4.1.6 Perfect Dodge Variant (Bloom Escape / Nível 5 upgrade)

- **At perfect dodge**: secondary burst of 50 additional petals at origin, radius 1.2 m outward, decelerating (simulates shockwave)
- Time-dilation: 0.15× time scale for 200 ms on hit-frame (requires game-side call)
- Ghost holds at full 60 % opacity for extended 1200 ms (enemy is frozen in perception)
- Additional FX: brief ring of petals at ground plane, `#FFEEAA` gold tint — marks the "sacred moment" of perfect timing

#### 4.1.7 Upgrade Progression (Niagara parameter gates)

| Level | Change |
|---|---|
| 1 — Basic | Single burst, short trail, simple ghost |
| 2 — Pétalas Residuais | Ghost leaves 8 petal particles persisting 2 s on ground |
| 3 — Espinho Floral | Rose thorns visible in petal cluster; slight damage emitter on enemies |
| 4 — Chuva de Pétalas | Trailing petals rain down for 3 s after dash, slow decay |
| 5 — Bloom Escape / Drift Perfeito | Full perfect-dodge burst (see 4.1.6) + full 4 s petal rain |

---

### 4.2 Dress Transformation (Sistema de Skill Baseado no Vestido)

> Each skill use corrupts Alice's dress by a fixed increment; at 100 % corruption the dress reverts to normal, sanity partially restored.

#### 4.2.1 Corruption Visual Progression

| Corruption Level | Dress State | Visual Markers |
|---|---|---|
| 0 % — Normal | Pristine white Victorian | Clean fabric, minor gold lace, no aberration |
| 20 % | Slight staining | Hem darkens (`#2A1A3E` violet-black creep), subtle vein patterns appear at skirt edges |
| 40 % | Partial corruption | Dark tendrils climb to waist; fabric tears reveal luminous underlay of the active Boss's color |
| 60 % | Heavy corruption | Upper body consumed; only head/shoulders retain white; active Boss color dominates bodice |
| 80 % | Near-total | Dress is almost fully replaced by Boss aesthetic; glowing runes, distorted silhouette |
| 100 % | Full corruption → Reset | Peak Boss visual + flash-white reset sequence |

#### 4.2.2 Boss-Linked Corruption Colors

| Boss / Skill Set | Corruption Hue | Accent | FX Character |
|---|---|---|---|
| Coelho Branco (Fracture do Tempo) | `#8080D0` – `#4040A0` blue-violet | Clock fragments, time distortions | Temporal ripples, slow-zone field |
| Gato Cheshire (Passo Sombrio) | `#4B2D6B` – `#8B1A8B` deep violet | Fade patches, invisible zones | Disappearance glitch, teal sparks |
| Chapeleiro (Rabbido das Caos) | `#1A5A1A` – `#50A050` viridian | Tea-stain brown patches, gear icons | Chaos fractal, rotating debris |
| Lagarta Azul (Fumaça do Sonho) | `#1A2850` – `#2040A0` cobalt | Blue smoke tendrils embedded in fabric | Smoke weave, floating runes |
| Rainha de Copas (Corte Real) | `#3A0808` – `#C01818` blood crimson | Card suit symbols, thorn lace | Blood drip particles, court thorns |

#### 4.2.3 Transition FX (Skill Cast → Corruption Advance)

- On each skill use: **procedural fabric shader tick** — corruption boundary advances 2–4 % along a Voronoi noise seam
- Particle burst at corruption boundary: 12–20 micro-particles in Boss color, rising upward 0.3 m then fade
- Sound + screen aberration: brief chromatic aberration (0.5-frame) at seam; red channel shifts +2 px
- Reset sequence (100 % → 0 %): full white flash (HDR 2.0 white) → white particle burst (180 petals, inward implosion) → dress dissolves and reconstitutes pristine; 1.2 s total

---

### 4.3 Skill Acquisition (Obter Skill — "Novo Poder Adquirido")

**Reference image:** Alice holding glowing hands out, scene lit by swirling purple particles rising from below — "Passo Sombrio" (Cheshire skill) example.

#### 4.3.1 Visual Sequence

1. **Boss death → Petal rain** (0–1 s): Boss defeated, petals fall as delírio (delirium) drops, each petal a translucent jewel in that Boss's color; 80–120 petals, gentle drift with curl noise
2. **Power absorption** (1–3 s): Petals converge toward Alice's outstretched hands; velocity field pulls inward from 2 m radius
3. **Hand burst** (3–3.4 s): Concentrated glow at both palms; dominant Boss color at HDR 1.8 intensity; small arcs between fingers
4. **Dress infusion** (3.4–5 s): Color ripples travel from hands down to dress hem; Voronoi seam of Boss color washes across fabric
5. **Acquisition complete** (5 s): UI card appears; ambient petal haze settles, 8 residual petals orbit Alice at 0.8 m radius for 4 s

#### 4.3.2 Color by Boss Skill

| Skill | Hand Glow | Petal Color | Dress Ripple |
|---|---|---|---|
| Fracture do Tempo | `#8080D0` blue-violet | `#D0D0FF` pale lavender | Blue-white wash |
| Passo Sombrio | `#8B1A8B` deep violet + `#20D0A0` teal | `#A040C0` vivid purple | Purple void wash |
| Rabbido das Caos | `#50A050` + `#C09820` gold | `#80FF80` bright green | Green-gold wash |
| Fumaça do Sonho | `#2040A0` + `#60A0F0` | `#4080D0` cobalt | Blue smoke tendrils |
| Corte Real | `#C01818` + `#FF2020` | `#FF4040` blood rose | Crimson flood |

#### 4.3.3 Niagara Emitter Stack

- **Emitter A — Petal Rain**: GPU, 100 particles, spawn rate 80/s for 1 s, curl noise, Boss color
- **Emitter B — Convergence Field**: velocity attractor point at Alice's center, activates at 1 s
- **Emitter C — Hand Spark**: 20 arc particles, sphere spawn around each hand bone, HDR emissive
- **Emitter D — Dress Ripple**: Material parameter collection driven; calls `BP_CorruptionTick` with +1 level
- **Emitter E — Ambient Orbit**: 8 long-life petals (10 s), orbit around character root at 0.8 m, sine wave altitude oscillation ±0.1 m

#### 4.3.4 Screen FX

- Radial vignette darkens to 80 % at absorption moment
- Brief color-grade LUT shift to Boss's dominant color (50 % blend, 0.3 s)
- Cinematic letterbox optional if cutscene flag set

---

### 4.4 Debuff Skill (Sistema de Skill e Corrupção do Vestido)

> Each time Alice uses a Skill, her dress is consumed by the associated Boss's power. The more she uses it, the deeper the corruption — and the more powerful but visually deteriorated she becomes.

#### 4.4.1 Visual Language of the Debuff State

The debuff is the **corruption system itself** — no separate debuff VFX pop; instead, the dress acts as the persistent health bar for Alice's sanity/integrity.

- **Visual feedback loop**: corruption level is always readable on the dress without any UI (art-driven readability)
- **Shader approach**: dual-layer fabric material — Layer 0 (pristine white Victorian), Layer 1 (Boss corruption overlay); blend weight driven by `f_CorruptionLevel` 0.0–1.0
- **Seam particle emitter** (persistent): At current corruption boundary, 4 micro-particles/s rise continuously — color = active Boss hue, scale = 0.02 m; these are the "alive" edge of corruption
- **Pulsation**: at every 20 % threshold crossing, dress emissive pulses once (Boss color, 0.5 s ease-out); signals danger escalation

#### 4.4.2 Per-Skill Corruption Increment

| Skill | Mana Cost | Corruption per Cast | Intensity |
|---|---|---|---|
| Fracture do Tempo (Coelho) | High | ~8–12 % | Temporal — mild visual |
| Passo Sombrio (Cheshire) | Medium | ~10 % | Spatial — moderate |
| Rabbido das Caos (Chapeleiro) | Medium | ~10 % | Chaotic — visible |
| Fumaça do Sonho (Lagarta) | Medium | ~10 % | Atmospheric — subtle |
| Corte Real (Rainha) | Low | ~15–20 % | Lethal — rapid |

#### 4.4.3 On-Skill-Cast Flash

Whenever a skill is cast, a brief VFX confirms the power + cost:

1. **Frame 0**: Hand pose locks; dominant Boss glow emits from palms (HDR 1.6, 3 frames)
2. **Frames 1–8**: Skill effect fires (see per-skill below)
3. **Frames 8–12**: Dress seam advances; micro-burst of 8 particles at seam edge
4. **Frames 12–20**: Decay; ambient Boss color settles on newly corrupted fabric zone

#### 4.4.4 Skill-Specific Cast VFX

| Skill | Cast Signature |
|---|---|
| Fracture do Tempo | Clock-ring expands outward at ground plane; `#8080D0` rings; time-crystal shards freeze in air |
| Passo Sombrio | Alice's silhouette multiplies (2 ghost copies) then snaps away; `#4B2D6B` fade |
| Rabbido das Caos | Chaos burst: 40 small objects (tea cups, cards, gears) explode outward; `#50A050` arcs |
| Fumaça do Sonho | Cobalt smoke column rises 2 m; dreamlike delay on enemy particles; `#2040A0` mist |
| Corte Real | Crimson slash mark appears in air (ribbon emitter); card-suit silhouette blooms; `#C01818` |

---

## 5. Finishing Rules (Materiais e Acabamento)

From the Bíblia Técnica master sheet (Image 1, Section 8):

| Material | Treatment |
|---|---|
| **Velvet** | Subsurface scattering, `#1A0A28` deep purple base, anisotropic sheen |
| **Porcelain** | High specular `0.95`, minimal roughness `0.05`, slight SSS |
| **Bronze** | `#8B5E28` base, `0.4` roughness, `0.9` metallic, verdigris in recesses |
| **Rot/Gold** | `#C9962A` metallic, worn edge `#8B6B14`, roughness gradient 0.1→0.6 |
| **Lace** | Opacity mask texture, `#F0E8D8` off-white, emissive at 0.1 for ethereal areas |
| **Metallic Gloss** | `#2A2A3A` dark chrome, `0.1` roughness, mirror-like |
| **Enchanted Wood** | `#2A1A0A` brown, subtle emissive green `#204020` vein in recesses |
| **Marble Linho** | `#E8E0D0` ivory, thin color veins per area, `0.15` roughness |
| **Latão** | `#C09040`, `0.5` roughness, `0.85` metallic, aged green edge |
| **Hm Oxidized** | Near-black `#1A1A14`, strong verdigris `#204030` overlay, rough `0.8` |

---

## 6. Illumination Per Area (Niagara + Lumen Notes)

| Area | Key Light Color | Fill / GI | Accent / Emissive |
|---|---|---|---|
| Riverbank Gold | `#E8A040` warm amber | `#402A10` dark earth | `#C9962A` gold rim |
| Cheshire Forest | `#102A20` near-black teal | `#1A3A35` deep teal | `#20D0A0` biolum cyan |
| Clockwork Abyss | `#8AB4D4` cold blue-white | `#1A2B4A` deep navy | `#C8D8E8` steel highlight |
| Interior Distorted | `#5A3A6B` low violet | `#1A1228` void purple | `#8B5E9A` scattered |
| Vortex Purple | `#A020C0` electric purple | `#3A0A4A` deep void | `#F060FF` neon bloom |
| Threshold Teal | `#2A6060` mid teal | `#0A1A1A` near-black | `#80C0C0` aqua mist |
| Ethereal White | `#FFFFFF` full white | `#E8E0D0` warm diffuse | `#C8B870` gold thread |
| Queen Crimson | `#C01818` hot red | `#1A0000` blood shadow | `#FF2020` execution red |

---

## 7. Niagara System Architecture Recommendations

```
NiagaraSystem_RoseDrift/
  ├── NS_Petals_Burst         (GPU, 200 particles, per-costume color override)
  ├── NS_Petals_Trail         (Ribbon, CPU, 0.8 m max length)
  ├── NS_AfterImage_Ghost     (Single instance, unlit mesh, opacity curve)
  ├── NS_GroundRain           (Level 2+ upgrade gate, 8 persistent ground petals)
  └── NS_PerfectDodge_Ring    (Level 5 only, radial burst, time-scale call)

NiagaraSystem_SkillAcquisition/
  ├── NS_PetalRain_Boss       (color driven by DT_BossColors data table)
  ├── NS_HandSpark            (bound to hand bones via attachment)
  ├── NS_DressRipple          (material param call, not particle)
  └── NS_OrbitPetals          (8 particles, sine altitude, 10 s life)

NiagaraSystem_CorruptionEdge/
  └── NS_SeamParticles        (4/s persistent emitter, seam position driven by shader UV)

NiagaraSystem_SkillCast_[BossName]/
  (one system per skill, unique cast signature — see §4.4.4)
```

---

## 8. Key Design Principles

1. **Rose Drift is the heartbeat**: Every player will see it every 10–15 seconds. It must be cheap, beautiful, and instantly legible. Prioritize GPU particle count, never CPU.
2. **Dress = Living UI**: No separate corruption meter UI required if dress shader is correct. Art direction carries the information.
3. **One dominant hue per area**: Never blend two area hues in the same shot. Corruption tint (`#2A0A3A`) is the only cross-area bleeder.
4. **Gold as the universal grammar**: UI, weapons, filigree all share the same gold family (`#C9962A` – `#E8B84B`). It grounds the player across all areas.
5. **After-image is the lie**: The ghost silhouette must read as Alice for at least 400 ms before enemies can distinguish. Opacity curve is gameplay-critical, not cosmetic.
6. **HDR bloom is free in Lumen**: Let petal emissive values go over 1.0. Never manually add glow passes.

---

*Document version: 1.0 — 2026-05-29*  
*Sources: Bíblia Técnica de Cores (8 sheets, 2026-05-25), VFX Reference Sheets (2026-05-21)*
