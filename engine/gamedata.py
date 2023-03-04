from engine.process import *
from enum import IntEnum

class processInfo():

    def GetWindowText(handle, length=100):
        window_text = ctypes.create_string_buffer(length)
        Process.u32.GetWindowTextA(
            handle,
            ctypes.byref(window_text),
            length
        )
        return window_text.value
    
    gameFocused = False
    
    def checkGameFocus():
        while True:
            if not processInfo.GetWindowText( Process.u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
                processInfo.gameFocused = False
                Process.k32.Sleep(1000) # 2 seconds delay for optimisation
            else:
                processInfo.gameFocused = True

def Weapon(index, name):
    if index == 42: name = "Knife"
    return name