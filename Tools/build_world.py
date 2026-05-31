"""Monta L_Mundo = mundo unico com 10 areas como streaming sublevels,
posicionadas por auto-layout do grafo (sem sobreposicao, espaco 250m).
Margem do Rio fica separado (portal entra aqui)."""
import unreal
L = lambda s: unreal.log(f"[W] {s}")

# auto-layout do grafo do roteiro (metros). Interior=inicio.
# espaco 250m >> maior mapa (76m) = zero sobreposicao
S = 250.0
layout = {
    "L_InteriorDeCha": (-2*S,  0),   # inicio (aterrissagem)
    "L_Vortice":       (-1*S,  0),
    "L_TocaMecanica":  ( 0*S,  0),   # Coelho boss
    "L_Arena":         ( 1*S,  0),
    "L_FlorestaCheshire":(2*S, 0),
    "L_SalaoCha":      ( 1*S,  1*S),
    "L_NevoaCogumelos":( 2*S,  1*S),
    "L_PatioReal":     ( 1*S,  2*S),
    "L_Ruinas":        ( 2*S,  2*S),
    "L_CampoEtereo":   ( 2*S,  3*S),  # finale
}

# cria mundo vazio
unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
world = unreal.EditorLevelLibrary.get_editor_world() if hasattr(unreal.EditorLevelLibrary,'get_editor_world') else None
L("mundo vazio criado")

added=0
for lvl, (x,y) in layout.items():
    pkg = f"/Game/Alice/Maps/{lvl}"
    t = unreal.Transform()
    t.translation = unreal.Vector(x*100.0, y*100.0, 0.0)  # m->cm
    try:
        sl = unreal.EditorLevelUtils.add_level_to_world_with_transform(
            unreal.EditorLevelLibrary.get_editor_world(),
            pkg, unreal.LevelStreamingAlwaysLoaded, t)
        if sl:
            added+=1
            L(f"  + {lvl} @ ({x:.0f},{y:.0f})m")
        else:
            L(f"  FALHOU {lvl}")
    except Exception as e:
        L(f"  ERR {lvl}: {e}")

# salva como L_Mundo
unreal.EditorLoadingAndSavingUtils.save_map(
    unreal.EditorLevelLibrary.get_editor_world(), "/Game/Alice/Maps/L_Mundo")
L(f"L_Mundo salvo, areas={added}/10")
L("END")
