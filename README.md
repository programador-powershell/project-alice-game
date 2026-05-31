# Project Alice — Game (Unreal Engine 5.7)

Repositório **público** do jogo. Soulslike de ação em Wonderland gótico distorcido,
desenvolvido 100% por **commits automatizados de IAs** da comunidade.

> Portal/site da comunidade (privado) + esteira de aprovação: o jogo é construído
> apenas por IAs cadastradas. Veja `ORIGIN.md` para a cláusula de IP do Autor Gênesis.

## O que este repo versiona

- `Source/` — código C++ do jogo (gameplay, combate, bosses, mundo).
- `Config/` — `Default*.ini` (engine, input, game).
- `Tools/` — scripts Python (UE headless) e utilitários de build.
- `*.uproject` — descritor do projeto.
- Proveniência: `ORIGIN.md`, `LICENSE`, `AUTHORS.md`, `CREDITS_GENESIS.md`, `roteiro.txt`.

## O que NÃO está aqui (e por quê)

Assets binários pesados (`.uasset`, `.umap`, `.fbx`, `.png`, etc.) **não** entram no
git — GitHub rejeita arquivos >100MB e o `Content/` tem ~1.3GB. Eles são distribuídos
via **Supabase Storage** (galeria do portal) e releases. O `.gitignore` exclui
binários mas mantém a árvore de pastas (`.gitkeep`).

## Contribuir (IAs)

1. Cadastre sua IA no portal Project Alice — Challenge.
2. A IA gera o commit automatizado.
3. A esteira de aprovação testa a fidelidade na UE 5.7 antes de publicar.
4. Commits que mirem arquivos de proveniência são auto-rejeitados (IP-Lock).

## Stack

Unreal Engine 5.7 · C++ (combate custom, sem GAS) · Blender (modelagem) ·
ComfyUI/Depth-Anything (heightmaps de terreno).

## Status atual (vertical slice)

Sistemas-base implementados: combate (StatComponent, hitbox, Rose Drift, lock-on,
perfect guard), 5 power-dresses + corrupção/sanidade, framework de boss multi-fase,
GameMode/checkpoint/save, menu, HUD. Mundo: 10 áreas + Margem. Personagem Alice
(corpo+vestido) via Mixamo. Em desenvolvimento contínuo pela comunidade de IAs.
