# Art Direction Brief — 3D Model Reference Sheets
## Project Alice — UE5.7 Dark-Gothic Soulslike

> Generated from 28 PNG reference sheets in `C:\Users\pslo9\OneDrive\Documentos\img\Model 3D\`
> Purpose: drive UE material tints + confirm GLB–image matching at `E:\temp_glb_import\`

---

## PLAYER CHARACTER

### Alice-3D — Alice Liddell (Base / Default)
- **Category:** player
- **Silhouette & Proportions:** Slim humanoid female, ~1.65 m scale, full gothic-lolita dress with multi-layer skirt flaring to knee-mid-calf; voluminous black curly hair to mid-back; knee-high platform boots add ~5 cm.
- **Dominant Colors:** Midnight navy `#1A1F35`, antique ivory/cream `#D4C9A8`, old gold trim `#9C7A3C`, dark charcoal bodice `#1C1C1C`.
- **Key Identifying Features:** Heavily embroidered corset bodice; layered ruffle skirt with gold lace border; elbow-length gloves; choker necklace; no weapon in hand — pure silhouette reference.
- **Material Cues:** Silk/taffeta dress layers, fine gold metallic thread embroidery, leather boots, subtle wear/distress on hems; no emissive.
- **GLB Match:** `SM_Alice_3D.glb`

---

### alice-faca-cozinha — Alice Liddell (Kitchen Knife / Combat Stance)
- **Category:** dress-variant (player combat skin)
- **Silhouette & Proportions:** Same body as Alice-3D; dress shortened to thigh-length asymmetric hem revealing more of striped stockings; two kitchen knives held dual-wield; posture more aggressive.
- **Dominant Colors:** Dark navy `#1A1F35`, cream `#D4C9A8`, blood-red stains `#8B1A1A`, old gold `#9C7A3C`.
- **Key Identifying Features:** Blood-smeared layered skirt; dual butcher-style knives with dark blades; corset more battered; same gold trim as base Alice but with rust/stain overlays.
- **Material Cues:** Same taffeta/silk base; procedural blood decals recommended; blade is dark steel with slight edge wear.
- **GLB Match:** No dedicated GLB found — likely shares `SM_Alice_3D.glb` mesh with a swap material set. Check for `SM_Alice_faca.glb`.

---

### alice-chapeleiro — Alice Liddell (Mad Hatter Dress Variant)
- **Category:** dress-variant (player skin — Hatter theme)
- **Silhouette & Proportions:** Same female humanoid; skirt shorter/more irregular hem; miniature dark top hat angled on head; taller platform laced boots to thigh.
- **Dominant Colors:** Forest/moss green `#2D4A2A`, olive gold `#7A6B3A`, aged cream `#C8B98A`, dark brown `#2A1F10`.
- **Key Identifying Features:** Mini tilted top hat with card and clock details; playing-card motif prints on skirt panels; clock-face embroideries; striped thigh-highs; leather laced boots.
- **Material Cues:** Heavy brocade cloth, tarnished brass clockwork accents, worn velvet hat; no emissive but subtle warm candle-light tint implied.
- **GLB Match:** No dedicated GLB found — likely `SM_Alice_chapeleiro.glb` or material variant. Check for this filename.

---

### alice-coelho — Alice Liddell (White Rabbit Dress Variant)
- **Category:** dress-variant (player skin — Rabbit theme)
- **Silhouette & Proportions:** Same base; adds dark bunny/rabbit ears on headband; hanging pocket watch accessory at hip; same multi-layer gothic lolita dress; knee-high laced boots.
- **Dominant Colors:** Deep navy `#1A2040`, antique gold `#9C7A3C`, cream `#D4C9A8`, dark charcoal `#1C1C1C`.
- **Key Identifying Features:** Rabbit ear accessories (black, not white — corrupted); gold pocket watch dangling from waist chain; spade/diamond suit embroidery; gold gear/clockwork prints on dress.
- **Material Cues:** Same taffeta dress; brass/gold pocket watch metal; leather ear headband; subtle clock glow on watch face possible.
- **GLB Match:** No dedicated GLB found — check `SM_Alice_coelho.glb`.

---

### alice-gato — Alice Liddell (Cheshire Cat Dress Variant)
- **Category:** dress-variant (player skin — Cheshire theme)
- **Silhouette & Proportions:** Same humanoid; cat ears (dark with inner highlight); dress heavily ruffled and frayed at hem asymmetrically; boots same laced style.
- **Dominant Colors:** Deep purple `#3A1A5C`, violet `#6B35A8`, black `#0D0D0D`, amethyst `#9B4DBF`.
- **Key Identifying Features:** Cat ear accessories; Cheshire cat face/grin motifs printed across skirt; purple emissive fringe on dress hem and sleeves; semi-transparent layered purple tulle.
- **Material Cues:** Purple silk/velvet with emissive glow on printed cat-face details; translucent tulle overlayers; dark leather boots; strong emissive bloom recommended on trim.
- **GLB Match:** No dedicated GLB found — check `SM_Alice_gato.glb`.

---

### alice-lagarta — Alice Liddell (Blue Caterpillar Dress Variant)
- **Category:** dress-variant (player skin — Caterpillar/Lagarta theme)
- **Silhouette & Proportions:** Same humanoid; dress most dramatically altered — longer trailing asymmetric back, heavily plated/segmented look to bodice; no hat; hair loose.
- **Dominant Colors:** Dark indigo `#0D1A40`, deep blue `#1A3A6B`, electric blue emissive `#1E6FFF`, black `#080808`.
- **Key Identifying Features:** Segmented/plated bodice reminiscent of caterpillar rings; blue flame/smoke emissive wisps rising from dress edges; sapphire gem accents on bodice panels; longer trailing skirt.
- **Material Cues:** Heavy layered cloth with chitin-like plated segments; strong blue emissive on edges (particle + emissive map); gem cabochon inserts.
- **GLB Match:** No dedicated GLB found — check `SM_Alice_lagarta.glb`.

---

### alice-rainha — Alice Liddell (Queen of Hearts Dress Variant)
- **Category:** dress-variant (player skin — Queen theme)
- **Silhouette & Proportions:** Same humanoid; dress widest/most dramatic; small dark crown headpiece; most regal stance.
- **Dominant Colors:** Crimson `#8B0000`, dark red `#5C0000`, black `#0D0D0D`, gold `#9C7A3C`.
- **Key Identifying Features:** Heart motifs densely covering dress; thorned vine/bramble trim details; dark crown with ruby-red gems; most ornate gold trim of all variants; thigh-high boots visible under skirt split.
- **Material Cues:** Heavy brocade with heart-patterned jacquard weave; metal crown; jewel gem inserts; no emissive but deep red velvet sheen.
- **GLB Match:** No dedicated GLB found — check `SM_Alice_rainha.glb`.

---

## LIDIA LIDDELL

### Lidia-3D — Lídia Liddell (NPC / Companion Form)
- **Category:** dress-variant (NPC / secondary player character)
- **Silhouette & Proportions:** Slim humanoid female, similar height to Alice; long full-length Victorian dress; bun updo hair with ornamental pins; more demure posture; Mary-Jane style flat shoes.
- **Dominant Colors:** Victorian navy `#1F2F50`, antique white/cream `#EDE0C4`, bone lace `#D9CDB0`, black ribbon `#1A1A1A`.
- **Key Identifying Features:** Large bow at back waist; lace collar and cuffs; layered petticoat skirt; no weapons; flat black shoes (contrasts Alice's heeled boots); overall cleaner/less worn look.
- **Material Cues:** Fine cotton/linen dress; delicate lace trim; satin bow; no emissive; pristine compared to Alice's battle-worn look.
- **GLB Match:** `SM_Lidia_3D.glb`

---

### Lidia_Boss — Lídia Liddell (Final Boss / Rainha do Coração Partido Form)
- **Category:** main-boss
- **Silhouette & Proportions:** Same humanoid base as Lidia-3D but dramatically expanded; long floor-length black gown with heavy train; thorn crown; holds both a dagger (faca) and a massive odachi simultaneously; hair loose/wild waist-length blonde.
- **Dominant Colors:** Pitch black `#080808`, blood red `#8B0000`, tarnished gold `#7A5C25`, pale blonde hair `#D4B86A`.
- **Key Identifying Features:** Gothic thorn crown; dual-wielded signature weapons (faca + odachi); gown covered in chain/crucifix jewelry draping; extensive blood staining on dress; heart motifs in red metal; the most silhouette-dominant character in the roster.
- **Material Cues:** Heavy black silk gown; ornate gold/tarnished metal chains; metal crucifix pendants; blade steel; strong red emissive on heart gems recommended; hair partially translucent at tips.
- **GLB Match:** `SM_Lidia_Boss.glb` (check spelling variants: `SM_Lidia_boss.glb`)

---

## MAIN BOSSES

### chapeleiro — Mad Hatter Boss (Chapeleiro Maluco)
- **Category:** main-boss
- **Silhouette & Proportions:** Tall slim humanoid male, ~1.85 m; extremely tall top hat adds ~40 cm vertical; long tattered tailcoat; unnaturally long gnarled fingers/claws; slight forward lean.
- **Dominant Colors:** Dark forest green `#1F3A1A`, tarnished gold `#7A6230`, mud brown `#3A2510`, aged bone `#C8B090`.
- **Key Identifying Features:** Massive wide-brim top hat (dark green felt, clockwork embellishments); skeletal grinning face (wide rictus smile); tattered Victorian tailcoat with watch-chain accessories; bare clawed hands with visible bones/sinew; tea-party iconography printed on coat.
- **Material Cues:** Worn velvet felt hat; weathered brocade tailcoat; exposed sinew/bone on hands; brass metal clasps; no emissive but green ambient SSS on skin suggested.
- **GLB Match:** `SM_chapeleiro.glb` (check for `SM_Chapeleiro.glb`)

---

### coelho-boss — White Rabbit Boss (Coelho Branco Boss Form)
- **Category:** main-boss
- **Silhouette & Proportions:** Humanoid rabbit, stocky/compact ~1.5 m (shorter than human bosses); upright bipedal stance; long upright rabbit ears dominate silhouette; no tail visible from front.
- **Dominant Colors:** Dark navy suit `#1A2A45`, aged white rabbit fur `#D8D0C0`, grey-blue `#7A8090`, tarnished gold `#9C7A3C`.
- **Key Identifying Features:** Anthropomorphic rabbit head (white/grey fur, wide empty eyes); formal Victorian double-breasted dark suit; glowing blue pocket watch hanging from chest chain; waistcoat with filigree buttons; black leather gloves.
- **Material Cues:** Fur shader needed on head/hands (short-length, grey-white); fine wool/tweed suit cloth; gold metal watch with emissive blue clock face; leather gloves.
- **GLB Match:** `SM_coelho_boss.glb`

---

### lagarta-boss — Blue Caterpillar Boss (Lagarta Azul Boss)
- **Category:** main-boss
- **Silhouette & Proportions:** Non-humanoid; massive vertical column/tower shape ~3–4 m tall; fat segmented worm body filling most of frame; tiny vestigial upper limbs; human-like face emerging from top; sits/levitates upright.
- **Dominant Colors:** Deep slate blue `#1A2A4A`, dark indigo `#0D1530`, tarnished gold `#7A6230`, smoke blue-grey `#4A5A70`.
- **Key Identifying Features:** Enormous segmented caterpillar body (wrinkled/folded skin); human-ish face at top with vacant expression; hookah pipe in one small hand; jeweled/chained decorations along spine ridge; smoke wisps from mouth/pipe.
- **Material Cues:** Heavy subsurface-scatter skin for segmented body (dark blue SSS); metal chain and jewel trim; hookah glass/metal; particle smoke emitter; gold metallic segments along back ridge.
- **GLB Match:** `SM_lagarta_boss.glb` (check case variants)

---

### rainha-boss — Queen of Hearts Boss (Rainha de Copas)
- **Category:** main-boss
- **Silhouette & Proportions:** Tall regal humanoid female, ~1.8 m plus crown adding ~30 cm; dramatic flared shoulder armor; wide trailing gown; most imposing vertical silhouette of all humanoid bosses.
- **Dominant Colors:** Crimson `#8B0000`, dark red `#5C0000`, black `#0A0808`, gold `#9C7A3C`.
- **Key Identifying Features:** Elaborate multi-pronged metal crown (dark iron with blood-red gems); massive armored pauldrons; full-length ballgown with heart iconography covering surface; heart-gem chest piece; long flowing cape/train; no weapon in ref hand but implied.
- **Material Cues:** Heavy armored pauldrons (dark iron, red enamel fills); velvet/silk gown beneath armor; heart-shaped emissive gems on chest; crown metal with red gem emissive; deep velvet cape.
- **GLB Match:** `SM_rainha_boss.glb` (check case)

---

### xicara-boss — Teacup Boss (Xícara Boss)
- **Category:** main-boss
- **Silhouette & Proportions:** Non-humanoid; roughly 1–1.5 m tall oversized teacup body mounted on spider/crab-like insectoid legs; face integrated into cup body; lid acts as head/cap.
- **Dominant Colors:** Cracked porcelain white `#E8E0D0`, rust/tarnish brown `#5A3A20`, aged gold `#7A6230`, dark shadow fill `#1A1410`.
- **Key Identifying Features:** Giant teacup with cracked face and hollow eye-socket holes; multiple articulated spider-like legs (dark metal/bone); teacup lid as cranium; flower/rose decal motifs visible on cup surface (faded); handle still present on side.
- **Material Cues:** Cracked porcelain material (high roughness, crack normal map); dark iron/bone legs; tarnished gold handle; suggested subsurface glow through cracks (interior emissive); chipped glaze detail.
- **GLB Match:** `SM_xicara_boss.glb` (check case: `SM_Xicara_boss.glb`)

---

### boss-soldado — Ace of Spades Soldier Boss (Boss Soldado)
- **Category:** main-boss
- **Silhouette & Proportions:** Tall humanoid male, ~1.9 m; broad-shouldered; wears long trailing tattered red cape; top hat (corrupted/crushed version); skull face; dual bladed weapons.
- **Dominant Colors:** Blood red `#6B0A0A`, bone white `#D4C8B0`, dark iron `#2A2A2A`, aged gold `#7A6230`.
- **Key Identifying Features:** Skeletal/skull face (visible through armor gaps); Ace of Spades symbol on chest plate; playing-card motif armor and tattered cape; red stained cloth beneath; dual long blades; top hat (corrupted Hatter variant).
- **Material Cues:** Battle-worn plate armor (dark iron, bloodstained); bone/skull face (SSS); red velvet/silk cape (shredded); gold trim on armor; card-print on fabric sections.
- **GLB Match:** `SM_boss_soldado.glb` (check case)

---

## MINI-BOSSES

### coelho — White Rabbit (Mob/Mini-Boss Tier — smaller form)
- **Category:** mini-boss
- **Silhouette & Proportions:** Same anthropomorphic rabbit as coelho-boss but noticeably smaller, ~1.2 m, stubbier proportions; more cartoony/toy-like scale; holds pocket watch.
- **Dominant Colors:** Pale grey-white `#C8C0B0`, dusty purple coat `#4A2A6B`, aged gold `#9C7A3C`, boot brown `#3A2510`.
- **Key Identifying Features:** Rabbit head (larger relative to body than boss version); shorter purple/grey Victorian coat; visible pocket watch on chain; small but upright bipedal; less menacing expression.
- **Material Cues:** Short fur on head/paws; worn cloth coat; brass watch chain; scuffed leather boots; all non-emissive.
- **GLB Match:** `SM_coelho.glb` (check case)

---

## MOBS (STANDARD ENEMIES)

### mob-biscoito — Gingerbread Cookie Mob (Biscoito)
- **Category:** mob
- **Silhouette & Proportions:** Short humanoid, ~0.9 m; stocky biscuit/gingerbread man shape; rounded head, stubby limbs; holds candy-cane staff/club.
- **Dominant Colors:** Gingerbread brown `#7A4520`, cream icing `#EDE0C0`, candy-cane red/white stripe `#C83030`, crimson eye glow `#8B0000`.
- **Key Identifying Features:** Classic gingerbread-man silhouette with sinister face; icing-sugar trim along edges; glowing red dot eyes; candy-cane weapon in right hand; textured baked-dough surface.
- **Material Cues:** Baked/ceramic surface texture (cookie roughness high, slight SSS orange); piped icing as specular white; candy cane painted plastic/sugar look; red emissive eyes.
- **GLB Match:** `SM_mob_biscoito.glb` (check case: `SM_mob_Biscoito.glb`)

---

### mob-bule — Teapot Spider Mob (Bule)
- **Category:** mob
- **Silhouette & Proportions:** Non-humanoid; roughly 0.8 m tall; teapot body on 6-8 spider-style legs; skull face on pot face; lid as cap.
- **Dominant Colors:** Cracked porcelain white-grey `#D0C8B8`, dark iron legs `#2A2420`, tarnish gold `#7A6230`, rust brown `#5A3020`.
- **Key Identifying Features:** Smaller version of xicara-boss concept; teapot (not cup) body shape with spout and handle; skull-face on body; articulated dark metal spider legs; cracked/aged porcelain; flower/vine faded decal.
- **Material Cues:** Cracked porcelain (same material family as xicara-boss, simpler); dark iron/bone legs; tarnished gold spout and handle rim; interior faint emissive through cracks (optional).
- **GLB Match:** `SM_mob_bule.glb` (check case)

---

### mob-carta — Flying Card Mob (Carta Volante)
- **Category:** mob
- **Silhouette & Proportions:** Non-humanoid flat creature; ~0.6 m tall card body; two large feathered/bone wings extend ~1 m span; bird-claw legs hang below; aspect ratio of a playing card (tall rectangle).
- **Dominant Colors:** Aged card white `#E0D8C8`, faded red `#8B3A3A`, dark grey `#3A3A3A`, bone wing `#C8B890`.
- **Key Identifying Features:** Playing card body (Ace of Diamonds front, red back); large skeletal/feathered wings sprouting from upper card edges; raptor-claw feet dangling; no head — card IS the body; purple emissive crystal tip ornaments hanging below.
- **Material Cues:** Aged paper/card stock with subtle card-print (albedo); bone/feather wings (separate material, off-white, SSS); dark iron talon claws; small purple emissive crystal pendants.
- **GLB Match:** `SM_mob_carta.glb` (check case)

---

### mob-soldado — Card Soldier Mob (Soldado Padrão)
- **Category:** mob
- **Silhouette & Proportions:** Humanoid, ~1.7 m; bulky due to oversized playing-card shield body worn as torso; rounded helmet; holding ornate mace/scepter; wide stance.
- **Dominant Colors:** Aged card white `#D8D0C0`, dark iron `#282828`, blood red `#7A1A1A`, tarnished gold `#7A6230`.
- **Key Identifying Features:** Heart-suit playing card as body/shield/torso (integrated, not held); medieval rounded helmet; elaborately decorated mace with orb top; blood-spatter on card surface; red heart suit printed center.
- **Material Cues:** Card-stock albedo on torso shield (aged paper look with print); dark iron armor limbs; gold metal on mace; painted heart symbol.
- **GLB Match:** `SM_mob_soldado.glb` (check case)

---

## WEAPONS

### weapon-bengala-cha-eterno — Bengala do Chá Eterno (Mad Hatter Cane)
- **Category:** weapon
- **Silhouette & Proportions:** ~1.4 m tall walking-stick/staff; ornate top shaped like inverted teacup with miniature hat; long straight shaft; transforms into a curved dark blade (modo transformado).
- **Dominant Colors:** Tarnished gold `#7A6230`, dark green `#1F3A1A`, aged bone `#C8B090`, dark blade `#1A1A2A`.
- **Key Identifying Features:** Miniature mad-hatter top hat + teacup head at top; clock and tea-party iconography along shaft; chain/tassel hanging ornaments; blade form: dark curved dagger with gold filigree.
- **Material Cues:** Gold metal shaft (tarnished); green velvet wraps; brass clockwork inlays; transformed blade = dark forged steel with gold edge inlay; no emissive in base form.
- **GLB Match:** `SM_weapon_bengala_cha_eterno.glb` (check underscores vs hyphens)

---

### weapon-foice-lagarta-azul — Foice da Lagarta Azul (Blue Caterpillar Scythe)
- **Category:** weapon
- **Silhouette & Proportions:** ~1.6 m reach; large asymmetric scythe blade; long ornate staff; dramatic flared crescent blade with trailing energy wisps; transforms into extended spear-like form.
- **Dominant Colors:** Deep black `#0D0D14`, electric blue emissive `#1E6FFF`, tarnished gold `#7A6230`, indigo `#1A1A4A`.
- **Key Identifying Features:** Massive curved scythe blade with blue flame/energy edge; ornate caterpillar-motif staff with jewel inserts; blue emissive smoke trails from blade edge; hookah-pipe inspired handle ornament at base; gold chain wrap.
- **Material Cues:** Dark forged steel blade; strong blue emissive on blade edge (bloom recommended); gold filigree metal on staff; jewel cabochon inserts (blue sapphire); particle blue smoke effect.
- **GLB Match:** `SM_weapon_foice_lagarta_azul.glb`

---

### weapon-guillotine-heartbreaker — Guillotine Heartbreaker (Queen of Hearts Weapon)
- **Category:** weapon
- **Silhouette & Proportions:** ~1.8 m tall; full ceremonial guillotine frame shape used as weapon; top crossbar with blade and heart motif; chain-suspended banner/fabric panel; transforms into massive curved blade.
- **Dominant Colors:** Dark iron `#1A1A1A`, blood red `#8B0000`, crimson emissive `#CC0000`, aged gold `#7A6230`.
- **Key Identifying Features:** Ornate guillotine frame (arched top); glowing heart gem at apex; blood-red velvet banner with card suit symbols; heavy chain attachments; blade drop visible in transformed mode as massive war-cleaver.
- **Material Cues:** Dark forged iron frame; heart gem = strong red emissive; red velvet banner cloth; gold metal trim; chain iron links; blood-stained blade edge.
- **GLB Match:** `SM_weapon_guillotine_heartbreaker.glb` (check underscores)

---

### weapon-relogio-coelho-branco — Relógio do Coelho Branco (White Rabbit Clock Weapon)
- **Category:** weapon
- **Silhouette & Proportions:** ~1.2 m staff with oversized pocket-watch head (base form); transforms into long elegant rapier/lance with trailing ghostly blade extension.
- **Dominant Colors:** Aged ivory `#E8E0C8`, tarnished gold `#9C7A3C`, pearl white `#F0EAE0`, ghostly blue-white `#A0C0E0`.
- **Key Identifying Features:** Large Roman-numeral pocket watch face at top (12 o'clock dominant); watch hands as blade elements; pearl/bone inlay on grip; transformed form elongates into ghostly blue-white energy lance; time-crack particle effects.
- **Material Cues:** Ivory/bone grip (smooth, slight SSS); gold metal watch case (tarnished); glass watch face with emissive ghostly glow; transformed energy blade = translucent blue-white emissive.
- **GLB Match:** `SM_weapon_relogio_coelho_branco.glb`

---

### weapon-sorriso-cheshire — Sorriso de Cheshire (Cheshire Cat Dagger)
- **Category:** weapon
- **Silhouette & Proportions:** ~0.9 m long wide curved dagger/kris-like blade; ornate crossguard with cat face; no transforms visible in still ref; elaborate pommel.
- **Dominant Colors:** Deep purple `#3A1A5C`, violet `#6B35A8`, black `#0A0A0F`, amethyst emissive `#9B4DBF`.
- **Key Identifying Features:** Cheshire cat grinning face integrated into crossguard/guard; wide wavy/curved blade (kris silhouette); purple crystalline emissive along blade fuller; cat motif carvings along blade; large ornate pommel with cat eye gem.
- **Material Cues:** Dark metal blade with purple emissive fuller channel; ornate gold/purple crossguard with cat face (could be separate metal ID); cat eye gem = strong purple emissive; overall heavy bloom on purple channels.
- **GLB Match:** `SM_weapon_sorriso_cheshire.glb` (check underscores)

---

### armas — Arsenal da Insanidade (All-Weapons Overview Sheet)
- **Category:** weapon (reference overview sheet, all 5 weapons)
- **Silhouette & Proportions:** Composite sheet showing all 5 Alice weapons side-by-side with front/side/back and transformed modes: (1) Relógio, (2) Sorriso de Cheshire, (3) Bengala do Chá Eterno, (4) Foice da Lagarta Azul, (5) Guillotine Heartbreaker. Scale reference for relative weapon sizes. Foice is tallest (~1.6 m), Relógio shortest (~1.2 m), Guillotine widest.
- **Dominant Colors:** See individual weapon entries above.
- **Key Identifying Features:** Confirms transform state for each weapon. Cheshire dagger transforms to a longer single-edge sword. Bengala transforms to a downward-curved dagger. Overview confirms particle/emissive active states.
- **Material Cues:** Same as individual entries; overview confirms color temperature — Relógio = cool blue-white, Cheshire = deep purple, Bengala = warm gold-green, Foice = electric blue, Guillotine = hot red.
- **GLB Match:** No single GLB — this is a reference sheet only. See individual weapon GLB entries.

---

## LIDIA BOSS WEAPONS

### faca-lidia-boss — Faca de Cozinha (Lidia Boss Knife)
- **Category:** weapon (Lidia Boss exclusive)
- **Silhouette & Proportions:** ~0.35 m single-blade chef's knife; traditional cooking knife profile; wide belly near tip; no transform in this ref; four throwing-knife silhouettes also shown (thinner, ~0.25 m).
- **Dominant Colors:** Matte black blade `#1A1A1A`, dark red handle `#5C1A1A`, ruby red gem inlays `#CC1A1A`, obsidian `#0D0D0D`.
- **Key Identifying Features:** Damascus-style textured black blade; dark red handle wrapped with red cord/chain; small ruby/red gemstone inlays at bolster; throwing knife variants shown without handles (blade-only projectiles); "Rainha do Coração Partido" line lore badge visible.
- **Material Cues:** Dark damascus steel (high-frequency normal, near-black albedo); dark red leather/cord handle wrap; red gem emissive inlays at bolster; throwing variants = pure dark steel.
- **GLB Match:** `SM_faca_lidia_boss.glb` (check case: `SM_Faca_Lidia_Boss.glb`)

---

### odachi-lidia-boss — Odachi/Nodachi (Lidia Boss Great Sword)
- **Category:** weapon (Lidia Boss exclusive)
- **Silhouette & Proportions:** ~1.8–2.0 m massive curved blade (odachi/nodachi profile); extremely long single-edge; slight curve; crossguard with ornate decoration; long grip for two-hand use; slender silhouette but immense reach.
- **Dominant Colors:** Matte black blade `#0D0D0D`, dark red blood stain `#6B0A0A`, tarnished gold crossguard `#7A6230`, deep crimson handle `#5C1A1A`.
- **Key Identifying Features:** Enormous length — longest blade in roster; dark black blade with blood-groove; ornate tsubas/crossguard with heart and thorn motifs; long handle with red cord wrap; red gem accent at pommel; same lore line as faca.
- **Material Cues:** Near-black polished steel (low roughness on face, high roughness on spine); red lacquer/cord handle; gold tarnished metal crossguard; red emissive gem at pommel; blood stain decal on blade.
- **GLB Match:** `SM_odachi_lidia_boss.glb` (check case: `SM_Odachi_Lidia_Boss.glb`)

---

## GLB MATCH SUMMARY TABLE

| Image Filename | Best-Guess GLB at E:\temp_glb_import\ | Confidence |
|---|---|---|
| Alice-3D | `SM_Alice_3D.glb` | HIGH |
| Lidia-3D | `SM_Lidia_3D.glb` | HIGH |
| Lidia_Boss | `SM_Lidia_Boss.glb` | HIGH |
| alice-chapeleiro | `SM_Alice_chapeleiro.glb` | MEDIUM (no GLB listed for variants) |
| alice-coelho | `SM_Alice_coelho.glb` | MEDIUM |
| alice-gato | `SM_Alice_gato.glb` | MEDIUM |
| alice-lagarta | `SM_Alice_lagarta.glb` | MEDIUM |
| alice-rainha | `SM_Alice_rainha.glb` | MEDIUM |
| alice-faca-cozinha | `SM_Alice_3D.glb` (shared mesh?) | LOW |
| boss-soldado | `SM_boss_soldado.glb` | HIGH |
| chapeleiro | `SM_chapeleiro.glb` | HIGH |
| coelho | `SM_coelho.glb` | HIGH |
| coelho-boss | `SM_coelho_boss.glb` | HIGH |
| lagarta-boss | `SM_lagarta_boss.glb` | HIGH |
| rainha-boss | `SM_rainha_boss.glb` | HIGH |
| xicara-boss | `SM_xicara_boss.glb` | HIGH |
| mob-biscoito | `SM_mob_biscoito.glb` | HIGH |
| mob-bule | `SM_mob_bule.glb` | HIGH |
| mob-carta | `SM_mob_carta.glb` | HIGH |
| mob-soldado | `SM_mob_soldado.glb` | HIGH |
| weapon-bengala-cha-eterno | `SM_weapon_bengala_cha_eterno.glb` | HIGH |
| weapon-foice-lagarta-azul | `SM_weapon_foice_lagarta_azul.glb` | HIGH |
| weapon-guillotine-heartbreaker | `SM_weapon_guillotine_heartbreaker.glb` | HIGH |
| weapon-relogio-coelho-branco | `SM_weapon_relogio_coelho_branco.glb` | HIGH |
| weapon-sorriso-cheshire | `SM_weapon_sorriso_cheshire.glb` | HIGH |
| armas | No GLB (overview sheet) | N/A |
| faca-lidia-boss | `SM_faca_lidia_boss.glb` | MEDIUM |
| odachi-lidia-boss | `SM_odachi_lidia_boss.glb` | MEDIUM |

> **Note on Alice dress variants (alice-chapeleiro, alice-coelho, alice-gato, alice-lagarta, alice-rainha, alice-faca-cozinha):** The provided GLB list at E:\temp_glb_import only names `SM_Alice_3D.glb` explicitly. These 6 variants may share the same mesh with material-only swaps, or they may be separate GLBs not yet listed. Verify at import time.
> **Note on Lidia weapons (faca-lidia-boss, odachi-lidia-boss):** These were not in the confirmed GLB list; filenames are inferred from image names.
