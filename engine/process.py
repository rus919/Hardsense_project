import pyMeow as pm
import ctypes as ctypes
import time

class Process():
    DEBUG_MODE = True
    
    csgo = pm.open_process(processName="csgo.exe")
    csgo_client = pm.get_module(csgo, "client.dll")["base"]
    csgo_engine = pm.get_module(csgo, "engine.dll")["base"]

    ntdll = ctypes.windll.ntdll
    k32 = ctypes.windll.kernel32
    u32 = ctypes.windll.user32