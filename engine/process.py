import pyMeow as pm
import ctypes as ctypes

class Process():
    csgo = pm.open_process(processName="csgo.exe")
    client_dll = pm.get_module(csgo, "client.dll")["base"]
    engine_dll = pm.get_module(csgo, "engine.dll")["base"]

    ntdll = ctypes.windll.ntdll
    k32 = ctypes.windll.kernel32
    u32 = ctypes.windll.user32