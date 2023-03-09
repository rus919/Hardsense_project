import ctypes as ctypes
from pymem import Pymem, process, exception, pattern

from requests import get

import mouse

class Offsets:
    pass

try:
    haze = get(
        "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
    ).json()

    [setattr(Offsets, k, v) for k, v in haze["signatures"].items()]
    [setattr(Offsets, k, v) for k, v in haze["netvars"].items()]
except:
    print("Unable to fetch Hazedumper's Offsets")
    exit(0)

class LocalPlayer():
    def __init__(self, address):
        self.address = address
    
    @staticmethod
    def get_local_player():
        return csgo.read_uint(csgo_client + Offsets.dwLocalPlayer)
    
    @staticmethod
    def get_crosshair_id():
        return csgo.read_uint(LocalPlayer.get_local_player() + Offsets.m_iCrosshairId)

class Entity():
    def __init__(self, address):
        self.address = address
    
    def get_team(self):
        return csgo.read_int(self.address + Offsets.m_iTeamNum)
    
    def get_health(self):
        return csgo.read_int(self.address + Offsets.m_iHealth)


class Engine():
    @staticmethod
    def get_entity(index):
        return csgo.read_uint(csgo_client + Offsets.dwEntityList + index * 0x10)

    @staticmethod
    def get_view_matrix(index):
        return csgo.read_uint(csgo_client + Offsets.dwEntityList + index * 0x10)


def trigger():
    while True:
        if u32.GetAsyncKeyState(6):
            Local_player = Entity(LocalPlayer.get_local_player())            
            entity_id = LocalPlayer.get_crosshair_id()
            if entity_id != 0 and entity_id < 64:
                entity = Entity(Engine.get_entity(entity_id - 1))
                
                if Local_player.get_team() != entity.get_team() and entity.get_health() > 0:
                    # k32.Sleep(1)
                    mouse.click()
                    k32.Sleep(250)
        # k32.Sleep(1)
    

if __name__ == '__main__':
    try:
        csgo = Pymem('csgo.exe')
        csgo_client = process.module_from_name(csgo.process_handle, 'client.dll').lpBaseOfDll
        # client_dll_size = process.module_from_name(csgo.process_handle, 'client.dll').SizeOfImage
        csgo_engine = process.module_from_name(csgo.process_handle, 'engine.dll').lpBaseOfDll
        
        ntdll = ctypes.windll.ntdll
        k32 = ctypes.windll.kernel32
        u32 = ctypes.windll.user32
    except exception.ProcessNotFound as err:
        print(err)
        print('Could not find CS:GO process!\nMake sure the game is running first!')
        exit(0)
        
    trigger()