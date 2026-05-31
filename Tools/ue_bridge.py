"""Bridge externo → UnrealEditor (Remote Execution UDP/TCP 6766).
Uso:
  python ue_bridge.py "import unreal; unreal.log('hi')"
  python ue_bridge.py @path/to/script.py
Retorna stdout + LogPython do editor.
"""
import sys, os, time, json
# força UTF-8 no stdout (Windows console default = cp1252 quebra com emoji)
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
try: sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

UE_PY_DIR = r"E:\UE_5.7\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python"
if UE_PY_DIR not in sys.path:
    sys.path.insert(0, UE_PY_DIR)
import remote_execution as re

def main():
    if len(sys.argv) < 2:
        print("uso: python ue_bridge.py '<comando>' OR '@arquivo.py'", file=sys.stderr); sys.exit(2)
    arg = sys.argv[1]
    if arg.startswith("@"):
        with open(arg[1:], "r", encoding="utf-8") as f:
            code = f.read()
        mode = re.MODE_EXEC_FILE  # arquivo multi-linha
    else:
        code = arg
        mode = re.MODE_EXEC_STATEMENT

    cfg = re.RemoteExecutionConfig()  # usa defaults (239.0.0.1:6766)
    rx = re.RemoteExecution(cfg)
    rx.start()
    # aguarda descobrir o editor (broadcast multicast a cada ~1s)
    deadline = time.time() + 5.0
    while not rx.remote_nodes and time.time() < deadline:
        time.sleep(0.2)
    if not rx.remote_nodes:
        print("ERRO: nenhum UnrealEditor respondeu no multicast 239.0.0.1:6766 em 5s.", file=sys.stderr)
        print("Confira: Edit→Project Settings→Python→Enable Remote Execution ☑ e editor aberto.", file=sys.stderr)
        rx.stop(); sys.exit(3)
    node_id = rx.remote_nodes[0]["node_id"]
    rx.open_command_connection(node_id)
    try:
        out = rx.run_command(code, unattended=True, exec_mode=mode, raise_on_failure=False)
    finally:
        rx.close_command_connection(); rx.stop()
    # out = {'success', 'result', 'output': [{'output','type'}], 'command'}
    success = out.get("success", False)
    print(f"[bridge] success={success}")
    for item in (out.get("output") or []):
        t = item.get("type",""); o = item.get("output","").rstrip()
        if o: print(f"  [{t}] {o}")
    if not success:
        print(f"[bridge] result: {out.get('result')}", file=sys.stderr); sys.exit(1)

if __name__ == "__main__":
    main()
