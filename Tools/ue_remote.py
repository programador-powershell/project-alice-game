"""Talk to a LIVE Unreal Editor via Remote Execution (port 6766).
Requires: editor open + Project Settings > Plugins > Python > "Enable Remote Execution".
Run with UE's bundled python:
  & "E:\\UE_5.7\\Engine\\Binaries\\ThirdParty\\Python3\\Win64\\python.exe" E:\\Alice\\Tools\\ue_remote.py "<python code>"
or pass a .py file path with --file.
"""
import sys, time, os
sys.path.append(r"E:\UE_5.7\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python")
from remote_execution import RemoteExecution, RemoteExecutionConfig, MODE_EXEC_FILE  # noqa


def run(code, discover_timeout=15.0):
    cfg = RemoteExecutionConfig()
    # Windows multicast discovery is more reliable bound to all adapters.
    cfg.multicast_bind_address = os.environ.get("UE_MC_BIND", "0.0.0.0")
    rec = RemoteExecution(cfg)
    rec.start()
    node = None
    t0 = time.time()
    while time.time() - t0 < discover_timeout:
        nodes = rec.remote_nodes
        if nodes:
            node = nodes[0]
            break
        time.sleep(0.25)
    if not node:
        rec.stop()
        print("UE_REMOTE: NO_NODE (editor open? Remote Execution enabled? port 6766?)")
        return 2
    nid = node.get("node_id") or node.get("nodeId")
    print("UE_REMOTE: node=%s" % nid)
    rec.open_command_connection(nid)
    try:
        res = rec.run_command(code, unattended=True, exec_mode=MODE_EXEC_FILE)
        print("UE_REMOTE: success=%s" % res.get("success"))
        out = res.get("output")
        if isinstance(out, list):
            for o in out:
                print("  [%s] %s" % (o.get("type"), o.get("output")))
        else:
            print("  output=%s" % out)
        if res.get("result"):
            print("  result=%s" % res.get("result"))
    finally:
        rec.close_command_connection()
        rec.stop()
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--file":
        with open(args[1], "r", encoding="utf-8") as f:
            code = f.read()
    elif args:
        code = args[0]
    else:
        code = "import unreal; print('UE remote alive:', unreal.SystemLibrary.get_engine_version())"
    sys.exit(run(code))
