import math
# import ctypes
# from ctypes import windll, Structure, c_float, c_uint32, c_uint64, c_char, sizeof, pointer, c_long, c_uint8, create_string_buffer, create_unicode_buffer, c_uint16, c_int32 
from ctypes import Structure, c_float, windll
from requests import get
import threading
import pyMeow as meow
from engine.process import Process

class Offsets:
    pass

class Vector3(Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]

class Colors:
    orange = meow.get_color("orange")
    black = meow.get_color("black")
    purple = meow.get_color("purple")
    white = meow.get_color("white")
    cyan = meow.get_color("cyan")
    red = meow.get_color("red")
    green = meow.get_color("green")
    pink = meow.get_color("pink")
    crosshair = meow.new_color(255, 0, 255, 255)
    recoil = meow.new_color(0, 0, 255, 155)

def esp():
    while meow.overlay_loop():
        
        meow.begin_drawing()
        
        meow.draw_text(text = "HARDSENSE", posX = 5, posY = 5, fontSize = 10, color = meow.get_color("red"))
        meow.draw_fps(50, 50)
        
        meow.end_drawing()

def main():
    try:
        haze = get(
            "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
        ).json()

        [setattr(Offsets, k, v) for k, v in haze["signatures"].items()]
        [setattr(Offsets, k, v) for k, v in haze["netvars"].items()]
    except:
        print("Unable to fetch Offsets")
        exit(0)
    
    try:
        csgo = Process('csgo.exe')
        client_dll = csgo.get_module("client.dll")
        engine_dll = csgo.get_module("engine.dll")

    except Exception as err:
        print(err)
        exit(0)
    meow.overlay_init(fps=144, title='test')
    

if __name__ == "__main__":    
    main()
    # print('[*]VirtualTables')
    # print('    VClient:            ' + hex(vt.client.table))
    # print('    VClientEntityList:  ' + hex(vt.entity.table))
    # print('    VEngineClient:      ' + hex(vt.engine.table))
    # print('    VEngineCvar:        ' + hex(vt.cvar.table))
    # # print('    InputSystemVersion: ' + hex(vt.input.table))
    # print('[*]Offsets')
    # print('    EntityList:         ' + hex(nv.dwEntityList))
    # print('    ClientState:        ' + hex(nv.dwClientState))
    # print('    GetLocalPlayer:     ' + hex(nv.dwGetLocalPlayer))
    # print('    GetViewAngles:      ' + hex(nv.dwViewAngles))
    # print('    GetMaxClients:      ' + hex(nv.dwMaxClients))
    # print('    IsInGame:           ' + hex(nv.dwState))
    # print('[*]NetVars')
    # print('    m_iHealth:          ' + hex(nv.m_iHealth))
    # print('    m_vecViewOffset:    ' + hex(nv.m_vecViewOffset))
    # print('    m_lifeState:        ' + hex(nv.m_lifeState))
    # print('    m_nTickBase:        ' + hex(nv.m_nTickBase))
    # print('    m_vecPunch:         ' + hex(nv.m_vecPunch))
    # print('    m_iTeamNum:         ' + hex(nv.m_iTeamNum))
    # print('    m_vecOrigin:        ' + hex(nv.m_vecOrigin))
    # print('    m_hActiveWeapon:    ' + hex(nv.m_hActiveWeapon))
    # print('    m_iShotsFired:      ' + hex(nv.m_iShotsFired))
    # print('    m_iCrossHairID:     ' + hex(nv.m_iCrossHairID))
    # print('    m_dwBoneMatrix:     ' + hex(nv.m_dwBoneMatrix))
    # # print('    1:     ' + Player.get_view_matrix())
    # print('    1:     ' + hex(clientdll))
        
    
    esp()
    
