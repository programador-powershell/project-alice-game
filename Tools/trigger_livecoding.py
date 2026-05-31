"""Dispara Live Coding compile (recompila C++ sem fechar editor)."""
import unreal
L = lambda s: unreal.log(f"[LC] {s}")
try:
    # console command que dispara live coding
    unreal.SystemLibrary.execute_console_command(None, "LiveCoding.Compile")
    L("LiveCoding.Compile disparado")
except Exception as e:
    L(f"cmd err: {e}")
L("END — acompanhe a janela Live Coding do editor (canto inf direito)")
