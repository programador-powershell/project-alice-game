import sys, unreal
sys.path.append(r"E:\Alice\Tools")
import ImportMenuArt, CreateMainMenu
try:
    ImportMenuArt.main()
except Exception as e:
    unreal.log_error("ImportMenuArt FAIL: %s" % e)
    print("ImportMenuArt FAIL", e)
try:
    CreateMainMenu.main()
except Exception as e:
    unreal.log_error("CreateMainMenu FAIL: %s" % e)
    print("CreateMainMenu FAIL", e)
print("BUILD_MENU_DONE")
