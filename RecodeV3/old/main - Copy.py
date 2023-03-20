import re
from turtle import screensize
from hardsense.keyauth import api

import sys
import os
import hashlib
from datetime import datetime
import json as jsond
import secrets

import math
import ctypes
from ctypes import *


import io

from dataclasses import dataclass

ntdll = windll.ntdll
k32 = windll.kernel32
u32 = windll.user32

# av = secrets.token_hex(nbytes=64)
# ctypes.windll.kernel32.SetConsoleTitleW(av)
# os.system('cls')

# def getchecksum():
#     md5_hash = hashlib.md5()
#     file = open(''.join(sys.argv), "rb")
#     md5_hash.update(file.read())
#     digest = md5_hash.hexdigest()
#     return digest

# keyauthapp = api(
#     name = "Test",
#     ownerid = "fYlaoJpYcM",
#     secret = "0c1369c66e7371f151c8d3991042227e14f9a23b772da2d85cd82f18507277c8",
#     version = "1.0",
#     hash_to_check = getchecksum()
# )

# try:
#     if os.path.isfile('auth.json'): #Checking if the auth file exist
#         if jsond.load(open("auth.json"))["authusername"] == "": #Checks if the authusername is empty or not
#             print("1. Login")
#             print("2. Register")
#             ans=input("Select Option: ")
#             if ans=="1": 
#                 user = input('Username: ')
#                 password = input('Password: ')
#                 keyauthapp.login(user,password)
#                 authfile = jsond.load(open("auth.json"))
#                 authfile["authusername"] = user
#                 authfile["authpassword"] = password
#                 jsond.dump(authfile, open('auth.json', 'w'), sort_keys=False, indent=4)
#             elif ans=="2":
#                 user = input('Create username: ')
#                 password = input('Create password: ')
#                 license = input('Enter license key: ')
#                 keyauthapp.register(user,password,license) 
#                 authfile = jsond.load(open("auth.json"))
#                 authfile["authusername"] = user
#                 authfile["authpassword"] = password
#                 jsond.dump(authfile, open('auth.json', 'w'), sort_keys=False, indent=4)
#             else:
#                 print("\nNot Valid Option") 
#                 os._exit(1) 
#         else:
#             try: #2. Auto login
#                 with open('auth.json', 'r') as f:
#                     authfile = jsond.load(f)
#                     authuser = authfile.get('authusername')
#                     authpass = authfile.get('authpassword')
#                     keyauthapp.login(authuser,authpass)
#             except Exception as e: #Error stuff
#                 print(e)
#     else: #Creating auth file bc its missing
#         try:
#             f = open("auth.json", "a") #Writing content
#             f.write("""{
#     "authusername": "",
#     "authpassword": ""
# }""")
#             f.close()
#             print ("""
# 1. Login
# 2. Register
#             """)#Again skipping auto-login bc the file is empty/missing
#             ans=input("Select Option: ") 
#             if ans=="1": 
#                 user = input('Username: ')
#                 password = input('Password: ')
#                 keyauthapp.login(user,password)
#                 authfile = jsond.load(open("auth.json"))
#                 authfile["authusername"] = user
#                 authfile["authpassword"] = password
#                 jsond.dump(authfile, open('auth.json', 'w'), sort_keys=False, indent=4)
#             elif ans=="2":
#                 user = input('Create username: ')
#                 password = input('Create password: ')
#                 license = input('Enter license key: ')
#                 keyauthapp.register(user,password,license) 
#                 authfile = jsond.load(open("auth.json"))
#                 authfile["authusername"] = user
#                 authfile["authpassword"] = password
#                 jsond.dump(authfile, open('auth.json', 'w'), sort_keys=False, indent=4)
#             else:
#                 print("\nNot Valid Option") 
#                 os._exit(1) 
#         except Exception as e: #Error stuff
#             print(e)
#             os._exit(1) 
# except Exception as e: #Error stuff
#     print(e)
#     os._exit(1)

# k32.Sleep(1)
# os.system('cls')
# print("User: " + keyauthapp.user_data.username)
# print("Subscription ends: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.expires)).strftime('%d/%m/%Y'))
# print("HWID: " + keyauthapp.user_data.hwid)

# if keyauthapp.check() == True:

from hardsense.config import *

    
global_trigger = True
g_aimbot_rcs = 1
g_aimbot_head = 0
g_aimbot_fov = 0.0 / 180.0
g_aimbot_smooth = 0.0

g_previous_tick = 0
g_current_tick = 0

g_old_punch = 0

import hardsense.offsets as offset

class Vector3(Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]

class PROCESSENTRY32(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("cntUsage", c_uint32),
        ("th32ProcessID", c_uint32),
        ("th32DefaultHeapID", c_uint64),
        ("th32ModuleID", c_uint32),
        ("cntThreads", c_uint32),
        ("th32ParentProcessID", c_uint32),
        ("pcPriClassBase", c_uint32),
        ("dwFlags", c_uint32),
        ("szExeFile", c_char * 260)
    ]

class Process:
    @staticmethod
    def get_process_handle(name):
        handle = 0
        entry = PROCESSENTRY32()
        snap = k32.CreateToolhelp32Snapshot(0x00000002, 0)
        entry.dwSize = sizeof(PROCESSENTRY32)
        while k32.Process32Next(snap, pointer(entry)):
            if entry.szExeFile == name.encode("ascii", "ignore"):
                handle = k32.OpenProcess(0x430, 0, entry.th32ProcessID)
                break
        k32.CloseHandle(snap)
        return handle

    @staticmethod
    def get_process_peb(handle, wow64):
        buffer = (c_uint64 * 6)(0)
        if wow64:
            if ntdll.NtQueryInformationProcess(handle, 26, pointer(buffer), 8, 0) == 0:
                return buffer[0]
        else:
            if ntdll.NtQueryInformationProcess(handle, 0, pointer(buffer), 48, 0) == 0:
                return buffer[1]
        return 0

    def __init__(self, name):
        self.mem = self.get_process_handle(name)
        if self.mem == 0:
            raise Exception("Process [" + name + "] not found!")
        self.peb = self.get_process_peb(self.mem, True)
        if self.peb == 0:
            self.peb = self.get_process_peb(self.mem, False)
            self.wow64 = False
        else:
            self.wow64 = True

    def is_running(self):
        buffer = c_uint32()
        k32.GetExitCodeProcess(self.mem, pointer(buffer))
        return buffer.value == 0x103

    def read_vec3(self, address):
        buffer = Vector3()
        ntdll.NtReadVirtualMemory(self.mem, c_long(address), pointer(buffer), 12, 0)
        return buffer

    def read_unicode(self, address, length=120):
        buffer = create_unicode_buffer(length)
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_float(self, address, length=4):
        buffer = c_float()
        ntdll.NtReadVirtualMemory(self.mem, c_long(address), pointer(buffer), length, 0)
        return buffer.value
    
    def read_string(self, address, length=120):
        buffer = create_string_buffer(length)
        ntdll.NtReadVirtualMemory(self.mem, address, buffer, length, 0)
        return buffer.value

    def read_i8(self, address, length=1):
        buffer = c_uint8()
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_i16(self, address, length=2):
        buffer = c_uint16()
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_i32(self, address, length=4):
        buffer = c_uint32()
        ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
        return buffer.value

    def read_i64(self, address, length=8):
        buffer = c_uint64()
        ntdll.NtReadVirtualMemory(self.mem, c_uint64(address), pointer(buffer), length, 0)
        return buffer.value

    def get_module(self, name):
        if self.wow64:
            a0 = [0x04, 0x0C, 0x14, 0x28, 0x10]
        else:
            a0 = [0x08, 0x18, 0x20, 0x50, 0x20]
        a1 = self.read_i64(self.read_i64(self.peb + a0[1], a0[0]) + a0[2], a0[0])
        a2 = self.read_i64(a1 + a0[0], a0[0])
        while a1 != a2:
            val = self.read_unicode(self.read_i64(a1 + a0[3], a0[0]))
            if str(val).lower() == name.lower():
                return self.read_i64(a1 + a0[4], a0[0])
            a1 = self.read_i64(a1, a0[0])
        raise Exception("Module [" + name + "] not found!")

@dataclass
class Vec3:
    x: float
    y: float
    z: float

class Player:
    def __init__(self, address):
        self.address = address

    def get_team_num(self):
        return mem.read_i32(self.address + offset.m_iTeamNum)

    def get_health(self):
        return mem.read_i32(self.address + offset.m_iHealth)

    def get_life_state(self):
        return mem.read_i32(self.address + offset.m_lifeState)

    def get_tick_count(self):
        return mem.read_i32(self.address + offset.m_nTickBase)

    def get_shots_fired(self):
        return mem.read_i32(self.address + offset.m_iShotsFired)

    def get_cross_index(self):
        return mem.read_i32(self.address + offset.m_iCrossHairID)

    def get_origin(self):
        return mem.read_vec3(self.address + offset.m_vecOrigin)

    def get_vec_view(self):
        return mem.read_vec3(self.address + offset.m_vecViewOffset)
    
    def get_dormant(self):
        return mem.read_i32(self.address + offset.m_bSpottedByMask)

    def check_dormant_esp(self):
        return mem.read_i8(self.address + offset.m_bDormant)

    def get_eye_pos(self):
        v = self.get_vec_view()
        o = self.get_origin()
        return Vector3(v.x + o.x, v.y + o.y, v.z + o.z)

    def get_pos(self):
        x = mem.read_float(self.address + offset.m_vecOrigin)
        y = mem.read_float(self.address + offset.m_vecOrigin + 0x4)
        z = mem.read_float(self.address + offset.m_vecOrigin + 0x8)
        return Vec3(x, y, z)

    def get_vec_punch(self):
        return mem.read_vec3(self.address + (offset.m_Local + 0x70)) #vecPunch

    def get_bone_pos(self, index):
        a0 = 0x30 * index
        a1 = mem.read_i32(self.address + offset.m_dwBoneMatrix)
        return Vector3(
            mem.read_float(a1 + a0 + 0x0C),
            mem.read_float(a1 + a0 + 0x1C),
            mem.read_float(a1 + a0 + 0x2C)
        )

    def is_valid(self):
        health = self.get_health()
        return self.address != 0 and self.get_life_state() == 0 and 0 < health < 1338

    def is_on_ground(self):
        return mem.read_i32(self.address + offset.m_fFlags) & (1 << 0)

    def get_weapon(self):
        a0 = mem.read_i32(self.address + offset.m_hActiveWeapon)
        return mem.read_i32(nv.dwEntityList + ((a0 & 0xFFF) - 1) * 0x10)
    
    def get_weapon_id(self):
        return mem.read_i32(self.get_weapon() + offset.m_iItemDefinitionIndex)
    
    # def get_weapon_owner(self):
    #     return mem.read_i32(self.address + offset.m_hOwnerEntity)
    def get_scope(self):
        return mem.read_i32(self.address + offset.m_bIsScoped)
    def has_defuser(self):
        return mem.read_i8(self.address + offset.m_bHasDefuser)
    # def get_accountID(self):
    #     return mem.read_i32(self.address + offset.m_iAccountID)

class NetVarList:
    def __init__(self):
        self.clientdll = mem.get_module("client.dll")
        self.enginedll = mem.get_module("engine.dll") 

        self.dwEntityList = self.clientdll + offset.dwEntityList
        self.dwClientState = mem.read_i32(self.enginedll + offset.dwClientState)
        self.dwGetLocalPlayer = offset.dwClientState_GetLocalPlayer
        self.dwViewAngles = offset.dwClientState_ViewAngles
        self.dwMaxClients = offset.dwClientState_MaxPlayer
        self.dwState = offset.dwClientState_State
        self.test2 = hex(offset.dwClientState)

class Entity:
    @staticmethod
    def get_client_entity(index):
        return Player(mem.read_i32(nv.dwEntityList + index * 0x10))            

class Engine:
    
    @staticmethod
    def get_local_player():
        return mem.read_i32(nv.dwClientState + nv.dwGetLocalPlayer)

    @staticmethod
    def get_view_angles():
        return mem.read_vec3(nv.dwClientState + nv.dwViewAngles)

    @staticmethod
    def get_max_clients():
        return mem.read_i32(nv.dwClientState + nv.dwMaxClients)

    @staticmethod
    def is_in_game():
        return mem.read_i8(nv.dwClientState + nv.dwState) >> 2

    def get_matrix():
        matrix = []
        for i in range(16):
            matrix.append(mem.read_float(nv.clientdll + offset.dwViewMatrix+0x4*i))
        return matrix

    # def get_map():
    #     return mem.read_string(nv.dwClientState + 0x28C) # hardcoded hazedumper

    # def get_map_directory():
    #     return mem.read_string(nv.dwClientState + 0x188) # hardcoded hazedumper

class Math:
    @staticmethod
    def sin_cos(radians):
        return [math.sin(radians), math.cos(radians)]

    @staticmethod
    def rad2deg(x):
        return x * 3.141592654

    @staticmethod
    def deg2rad(x):
        return x * 0.017453293

    @staticmethod
    def angle_vec(angles):
        s = Math.sin_cos(Math.deg2rad(angles.x))
        y = Math.sin_cos(Math.deg2rad(angles.y))
        return Vector3(s[1] * y[1], s[1] * y[0], -s[0])

    @staticmethod
    def vec_normalize(vec):
        radius = 1.0 / (math.sqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z) + 1.192092896e-07)
        vec.x *= radius
        vec.y *= radius
        vec.z *= radius
        return vec

    @staticmethod
    def vec_angles(forward):
        if forward.y == 0.00 and forward.x == 0.00:
            yaw = 0
            pitch = 270.0 if forward.z > 0.00 else 90.0
        else:
            yaw = math.atan2(forward.y, forward.x) * 57.295779513
            if yaw < 0.00:
                yaw += 360.0
            tmp = math.sqrt(forward.x * forward.x + forward.y * forward.y)
            pitch = math.atan2(-forward.z, tmp) * 57.295779513
            if pitch < 0.00:
                pitch += 360.0
        return Vector3(pitch, yaw, 0.00)

    @staticmethod
    def vec_clamp(v):
        if 89.0 < v.x <= 180.0:
            v.x = 89.0
        if v.x > 180.0:
            v.x -= 360.0
        if v.x < -89.0:
            v.x = -89.0
        v.y = math.fmod(v.y + 180.0, 360.0) - 180.0
        v.z = 0.00
        return v

    @staticmethod
    def vec_dot(v0, v1):
        return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

    @staticmethod
    def vec_length(v):
        return v.x * v.x + v.y * v.y + v.z * v.z

    @staticmethod
    def get_fov(va, angle):
        a0 = Math.angle_vec(va)
        a1 = Math.angle_vec(angle)
        return Math.rad2deg(math.acos(Math.vec_dot(a0, a1) / Math.vec_length(a0)))


def get_target_angle(local_p, target, bone_id):
    m = target.get_bone_pos(bone_id)
    c = local_p.get_eye_pos()
    c.x = m.x - c.x
    c.y = m.y - c.y
    c.z = m.z - c.z
    c = Math.vec_angles(Math.vec_normalize(c))
    if g_aimbot_rcs == 1 and local_p.get_shots_fired() > 1:
        p = local_p.get_vec_punch()
        c.x -= p.x * 2.0
        c.y -= p.y * 2.0
        c.z -= p.z * 2.0
    return Math.vec_clamp(c)

_target = Player(0)
_target_bone = 0
# 79 = left leg | 72 = right leg | 78 = left knee | 71 = right knee | 6 = upper chest | 41 = left shoulder | 11 = right shoulder | 77 left pelvis | 70 right pelvis | 42 = left elbow | 12 = right elbow
# _bones = [72, 79, 78, 71, 77, 70, 6, 41, 42, 12, 11, 5, 4, 3, 0, 7, 8]
_bones = [5, 4, 3, 0, 7, 8]
_aimbot_exclude = [43, 44, 45, 46, 47, 48, 31, 42, 49, 59, 500, 505, 506, 507, 508, 509, 512, 514, 515, 516]
_scoping_rifles = [9, 40, 38, 11]


def target_set(target):
    global _target
    _target = target

def get_best_target(va, local_p):
    global _target_bone
    
    a0 = 9999.9
    for i in range(1, Engine.get_max_clients()):
        entity = Entity.get_client_entity(i)
        if not entity.is_valid():
            continue
        if self.get_team_num() == entity.get_team_num() and local_p.get_team_num() == entity.get_team_num():
            continue
        if aimbotVisibleOnly == 1 and aimbot == 1 and u32.GetAsyncKeyState(aimbotKey):
            if not entity.get_dormant():
                continue
        if aimbot2VisibleOnly == 1 and aimbot2 == 1 and u32.GetAsyncKeyState(aimbot2Key):
            if not entity.get_dormant():
                continue
        if triggerMagnetVisibleOnly == 1 and triggerMagnet == 1 and u32.GetAsyncKeyState(triggerMagnetKey):
            if not entity.get_dormant():
                continue
        if g_aimbot_head == 1:
            fov = Math.get_fov(va, get_target_angle(local_p, entity, 8))
            if fov < a0:
                a0 = fov
                target_set(entity)
                _target_bone = 8
        else:
            for j in range(0, _bones.__len__()):
                fov = Math.get_fov(va, get_target_angle(local_p, entity, _bones[j]))
                if fov < a0:
                    a0 = fov
                    target_set(entity)
                    _target_bone = _bones[j]
    return a0 != 9999

# def esp_sound(va, _target, local_p):
#     if not _target.is_valid():
#         return
#     m = _target.get_origin()
#     c = local_p.get_origin()
#     c.x = m.x - c.x
#     c.y = m.y - c.y
#     c.z = m.z - c.z
#     dist = math.sqrt(Math.vec_length(c))
#     c = Math.vec_angles(Math.vec_normalize(c))
#     c = Math.vec_clamp(c)
#     y = va.x - c.x
#     x = va.y - c.y
#     if y > 89.0:
#         y = 89.0
#     elif y < -89.0:
#         y = -89.0
#     if x > 180.0:
#         x -= 360.0
#     elif x < -180.0:
#         x += 360.0
#     if math.fabs(y) / 89.0 > g_aimbot_fov:
#         return
#     if math.fabs(x) / 180.0 > g_aimbot_fov:
#         return
#     if dist < 1200.0:
#         k32.Beep(400, 80)
#         return
#     elif dist < 2400.0 and math.fabs(x) / 180.0 > g_aimbot_fov / 2.0:
#         k32.Beep(600, 80)
#         return 
#     elif dist >= 2400.0 and math.fabs(x) / 180.0 > g_aimbot_fov / 3.0:
#         k32.Beep(800, 80)
#     return


def aim_at_target(sensitivity, va, angle):
    global g_current_tick
    global g_previous_tick
    y = va.x - angle.x
    x = va.y - angle.y
    if y > 89.0:
        y = 89.0
    elif y < -89.0:
        y = -89.0
    if x > 180.0:
        x -= 360.0
    elif x < -180.0:
        x += 360.0
    if math.fabs(x) / 180.0 >= g_aimbot_fov:
        target_set(Player(0))
        return
    if math.fabs(y) / 89.0 >= g_aimbot_fov:
        target_set(Player(0))
        return
    x = (x / sensitivity) / 0.022
    y = (y / sensitivity) / -0.022
    if g_aimbot_smooth > 1.00:
        sx = 0.00
        sy = 0.00
        if sx < x:
            sx += 1.0 + (x / g_aimbot_smooth)
        elif sx > x:
            sx -= 1.0 - (x / g_aimbot_smooth)
        if sy < y:
            sy += 1.0 + (y / g_aimbot_smooth)
        elif sy > y:
            sy -= 1.0 - (y / g_aimbot_smooth)
    else:
        sx = x
        sy = y
    if g_current_tick - g_previous_tick > 0:
        g_previous_tick = g_current_tick
        u32.mouse_event(0x0001, int(sx), int(sy), 0, 0)
        
def GetWindowText(handle, length=100):
    window_text = ctypes.create_string_buffer(length)
    u32.GetWindowTextA(
        handle,
        ctypes.byref(window_text),
        length
    )

    return window_text.value

from overlay import *

@dataclass
class ScreenSize:
    x = ctypes.windll.user32.GetSystemMetrics(0)
    y = ctypes.windll.user32.GetSystemMetrics(1)

def w2s(pos: Vec3, matrix):
    z = pos.x * matrix[12] + pos.y * matrix[13] + pos.z * matrix[14] + matrix[15]
    if z < 0.1:
        return None

    x = pos.x * matrix[0] + pos.y * matrix[1] + pos.z * matrix[2] + matrix[3]
    y = pos.x * matrix[4] + pos.y * matrix[5] + pos.z * matrix[6] + matrix[7]

    xx = x / z
    yy = y / z

    _x = (ScreenSize.x / 2 * xx) + (xx + ScreenSize.x / 2)
    _y = (ScreenSize.y / 2 * yy) + (yy + ScreenSize.y / 2)

    return [_x, _y]
        
def over2(overlay):
    try:
        for i in range(1, Engine.get_max_clients()):
            entity = Entity.get_client_entity(i)

            if not entity.is_valid() and entity.check_dormant_esp() == 1:
                continue

            view_matrix = Engine.get_matrix()
            entity_position = entity.get_pos()
            w2s_position = w2s(entity_position, view_matrix)
            head_position = entity.get_bone_pos(8)
            w2s_head = w2s(head_position, view_matrix)
            entity_weapon = entity.get_weapon_id()
            if w2s_position is not None and w2s_head is not None:
                # c4data = [34, 129]
                # if entity_weapon in c4data:
                #     c4_pos = entity.get_pos()
                #     w2s_c4_pos = w2s(c4_pos, view_matrix)
                    
                #     if w2s_c4_pos is None or c4_pos.x == 0.0:
                #         continue
                #     overlay.draw_empty_circle(w2s_c4_pos[0], w2s_c4_pos[1], 10.0, 10, (255.0, 255.0, 0.0))
                    

                head = w2s_head[1] - w2s_position[1]
                width = head / 2
                height = width / 4
                center = width / -2
                healthWidth = head / 2
                entity_health = entity.get_health()
                health_color = (0, 255, 0)
                if GetWindowText( u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
                    if entity_health < 90:
                        healthWidth = head / 2.5
                    if entity_health < 80:
                        healthWidth = head / 3
                        health_color = (255, 255, 0)
                    if entity_health < 70:
                        healthWidth = head / 4
                    if entity_health < 60:
                        healthWidth = head / 5
                        health_color = (255, 150, 0)
                    if entity_health < 50:
                        healthWidth = head / 6
                    if entity_health < 40:
                        healthWidth = head / 7
                        health_color = (255, 100, 0)
                    if entity_health < 30:
                        healthWidth = head / 8
                    if entity_health < 20:
                        healthWidth = head / 10
                        health_color = (255, 0, 0)
                    if entity_health < 10:
                        healthWidth = head / 16

                    overlay.box(w2s_position[0] + center, w2s_position[1] - 5, healthWidth, height, 2, health_color)
                    overlay.line(1920 / 2, 0, w2s_position[0], w2s_position[1], 1, (0.53, 0.12, 0.47))

                    if not entity.get_dormant():
                        overlay.draw_empty_circle(w2s_head[0], w2s_head[1], 2, 10, (0.0, 255.0, 0.0))
                        overlay.corner_box(w2s_position[0] + center, w2s_position[1], width, head + 5, 1, (0.53, 0.12, 0.47), (0, 0, 0))
                    else:
                        overlay.draw_empty_circle(w2s_head[0], w2s_head[1], 2, 10, (255.0, 0.0, 0.0))
                        overlay.corner_box(w2s_position[0] + center, w2s_position[1], width, head + 5, 1, (0.1, 0.12, 0.9), (0, 0, 0))
    except Exception as err:
        pass
    k32.Sleep(1)

# def spectator_list(self):
#     spectators = []
#     while True:
#         try:
#             spectators.clear()
#             if entity.is_valid():
#                     if self.get_health() <= 0:
#                         spectators.clear()

#                     for i in range(1, Engine.get_max_clients()):
#                         entity = Entity.get_client_entity(i)
#                         player_name = ent.get_name(entity[0])
#                         if player_name == None or player_name == 'GOTV':
#                             continue

#                         if ent.get_team(entity[1]) == ent.get_team(lp.local_player()):
#                             observed_target_handle = game_handle.read_uint(entity[1] + offsets.m_hObserverTarget) & 0xFFF
#                             spectated = game_handle.read_uint(mem.client_dll + offsets.dwEntityList + (observed_target_handle - 1) * 0x10)
                            
#                             if spectated == lp.local_player():
#                                 spectators.append(ent.get_name(entity[0]))
            
#                 if len(spectators) > 0:
#                     format = '\n'.join(spectators)
#                     dpg.set_value('spectator_list', format)
#             else:
#                 dpg.set_value('spectator_list', '')
#         except Exception as err:
#             print(err)
#         time.sleep(0.2)

# def bomb_events(self):
# # works just fine, but currently unused.
# # TO:DO : cleanup code
#     cur_time = mem.read_float(nv.enginedll + offset.dwGlobalVars + 0x10)
#     print(self.has_defuser())
#             # 
#             # # print(t)
#             # for entity in ent.glow_objects_list:
#             #     bomb_defused = game_handle.read_bool(entity[1] + 0x29c0)
                
#             #     if entity[2] == 129:
#             #         bomb = game_handle.read_float(entity[1] + 0x29a0)
#             #         time_to_explode = bomb - cur_time

#             #         time_to_defuse = bomb - cur_time - (5 if has_defuser == True else 10)
#             #         # print(time_to_explode, time_to_defuse)
#             #         if (time_to_explode) <= 0:
#             #             print('Bomb exploaded!')
#             #             time.sleep(10)
#             #         elif (bomb_defused == True):
#             #             print('Bomb defused!')
#             #             time.sleep(10)
#     k32.Sleep(1)
                            

if __name__ == "__main__":
    try:
        mem = Process('csgo.exe')
        # vt = InterfaceList()
        nv = NetVarList()
    except Exception as e:
        print(e)
        exit(0)

    print('[*]Offsets')
    print('    EntityList:         ' + hex(nv.dwEntityList))
    print('    ClientState:        ' + hex(nv.dwClientState))
    print('    GetLocalPlayer:     ' + hex(nv.dwGetLocalPlayer))
    print('    GetViewAngles:      ' + hex(nv.dwViewAngles))
    print('    GetMaxClients:      ' + hex(nv.dwMaxClients))
    print('    IsInGame:           ' + hex(nv.dwState))
    print(nv.test2)

    global overlay
    overlay = Overlay()

    x1 = (ScreenSize.x / 2) + 1
    y1 = (ScreenSize.y / 2) + 1
    dx = (ScreenSize.x + 1) / 90 # TO DO: Don't hardcode player fov
    dy = (ScreenSize.y + 1) / 90

    while mem.is_running():
        k32.Sleep(1)
        if Engine.is_in_game():
            try:
                if not GetWindowText( u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
                    noWindow = False
                else:
                    noWindow = True
                self = Entity.get_client_entity(Engine.get_local_player())
                view_angle = Engine.get_view_angles()
                weapon_id = self.get_weapon_id()
                
                over2(overlay)

                if weapon_id in _scoping_rifles:
                    if not self.get_scope():
                        overlay.draw_lines(960, 540, 1)

                punch_angle = self.get_vec_punch()
                if punch_angle.x != 0.0 and self.get_shots_fired() > 1:
                    crosshair_x = x1 - dx * punch_angle.y
                    crosshair_y = y1 - dy * punch_angle.x
                    overlay.draw_lines(crosshair_x, crosshair_y, 1)

                overlay.refresh()


                if weapon_id in _aimbot_exclude:
                    continue
                
                if u32.GetAsyncKeyState(6) and noWindow == True:
                    cross_id = self.get_cross_index()
                    if cross_id == 0:
                        continue
                    cross_target = Entity.get_client_entity(cross_id - 1)

                    if triggerBot == 1 and self.get_team_num() != cross_target.get_team_num() and cross_target.get_health() > 0:
                        k32.Sleep(triggerDelayBeforeShot)
                        u32.mouse_event(0x0002, 0, 0, 0, 0)
                        k32.Sleep(50)
                        u32.mouse_event(0x0004, 0, 0, 0, 0)
                        k32.Sleep(triggerDelayAfterShot)

                if triggerMagnet == 1 and u32.GetAsyncKeyState(5) and noWindow == True:
                    g_aimbot_head = triggerMagnetOnlyHS
                    g_aimbot_fov = triggerMagnetFov / 180.0
                    g_aimbot_smooth = triggerMagnetSmooth

                    g_current_tick = self.get_tick_count()
                    
                    if not _target.is_valid() and not get_best_target(view_angle, self):
                        continue
                    aim_at_target(sensitivity, view_angle, get_target_angle(self, _target, _target_bone))

                    cross_id = self.get_cross_index()
                    if cross_id == 0:
                        continue
                    cross_target = Entity.get_client_entity(cross_id - 1)

                    if self.get_team_num() != cross_target.get_team_num() and cross_target.get_health() > 0:
                        k32.Sleep(5)
                        u32.mouse_event(0x0002, 0, 0, 0, 0)
                        k32.Sleep(50)
                        u32.mouse_event(0x0004, 0, 0, 0, 0)
                        k32.Sleep(triggerMagnetDelayAfterShot)
                else:
                    target_set(Player(0))

                if aimbot == 1 and u32.GetAsyncKeyState(1) and noWindow == True:

                    if weapon_id == 4: #Glock-18
                        g_aimbot_head = glockHS
                        g_aimbot_rcs = 0
                        g_aimbot_fov = glockFov / 180.0
                        g_aimbot_smooth = glockSmooth
                    elif weapon_id == 61: #USP-S
                        g_aimbot_head = uspsHS
                        g_aimbot_rcs = 0
                        g_aimbot_fov = uspsFov / 180.0
                        g_aimbot_smooth = uspsSmooth
                    elif weapon_id == 1: #Deagle
                        g_aimbot_head = deagleHS
                        g_aimbot_rcs = 0
                        g_aimbot_fov = deagleFov / 180.0
                        g_aimbot_smooth = deagleSmooth
                    else:
                        g_aimbot_head = aimbotHead
                        g_aimbot_rcs = aimbotRCS
                        g_aimbot_fov = aimbotFov / 180.0
                        g_aimbot_smooth = aimbotSmooth

                    g_current_tick = self.get_tick_count()
                    if not _target.is_valid() and not get_best_target(view_angle, self):
                        continue
                    aim_at_target(sensitivity, view_angle, get_target_angle(self, _target, _target_bone))
                else:
                    target_set(Player(0))

                if aimbot2 == 1 and u32.GetAsyncKeyState(18) and noWindow == True:

                    g_aimbot_head = aimbot2Head
                    g_aimbot_rcs = aimbot2RCS
                    g_aimbot_fov = aimbot2Fov / 180.0
                    g_aimbot_smooth = aimbot2Smooth

                    g_current_tick = self.get_tick_count()
                    if not _target.is_valid() and not get_best_target(view_angle, self):
                        continue
                    aim_at_target(sensitivity, view_angle, get_target_angle(self, _target, _target_bone))
                else:
                    target_set(Player(0))


                # current_punch = self.get_vec_punch()
                # if self.get_shots_fired() > 1:
                #     new_punch = Vector3(current_punch.x - g_old_punch.x,
                #                         current_punch.y - g_old_punch.y, 0)
                #     new_angle = Vector3(view_angle.x - new_punch.x * 1.25, view_angle.y - new_punch.y * 1.0, 0)
                #     u32.mouse_event(0x0001,
                #                     int(((new_angle.y - view_angle.y) / sensitivity) / -0.022),
                #                     int(((new_angle.x - view_angle.x) / sensitivity) / 0.022),
                #                     0, 0)
                # g_old_punch = current_punch
            except ValueError:
                continue
        else:
            g_previous_tick = 0
            target_set(Player(0))
