"""Adiciona samples ao BS_CoelhoLoco (idle/walk/run no eixo Speed) e confirma ABP."""
import unreal
L = lambda s: unreal.log(f"[BS] {s}")

DST = "/Game/Alice/AnimCoelho"
bs = unreal.load_asset(f"{DST}/BS_CoelhoLoco")
L(f"BS = {'OK' if bs else 'MISS'}")
idle = unreal.load_asset(f"{DST}/C_Idle")
walk = unreal.load_asset(f"{DST}/C_Walk")
run  = unreal.load_asset(f"{DST}/C_Run")

if bs:
    # tenta add_sample (assinatura pode variar)
    added = 0
    for clip, spd in [(idle,0.0),(walk,150.0),(run,550.0)]:
        if not clip: continue
        try:
            bs.add_sample(clip, unreal.Vector(spd,0,0))
            added += 1
        except Exception as e:
            L(f"  add_sample({spd}) v1 err: {e}")
            try:
                bs.add_sample(clip, spd)  # 1D pode aceitar float
                added += 1
            except Exception as e2:
                L(f"  add_sample({spd}) v2 err: {e2}")
    L(f"samples adicionados: {added}")
    unreal.EditorAssetLibrary.save_loaded_asset(bs, only_if_is_dirty=False)

abp = unreal.load_asset(f"{DST}/ABP_Coelho")
L(f"ABP_Coelho = {'OK' if abp else 'MISS'}")
L("END")
