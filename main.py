import math
from requests import get
import threading
import pyMeow as meow
from engine.process import Process, Windll
from engine.gamedata import Colors
from utils.offsets import Offset
from utils.entity import Entity, LocalPlayer, Engine
from tools.trigger import trigger
from tools.esp import esp
from tools.entity_parse import entity_parse, EntityList

from GUI import *
import os, sys

# class Math:
    
#     def sin_cos(radians):
#         return [math.sin(radians), math.cos(radians)]

    
#     def rad2deg(x):
#         return x * 3.141592654

    
#     def deg2rad(x):
#         return x * 0.017453293

    
#     def angle_vec(angles):
#         s = Math.sin_cos(Math.deg2rad(angles.x))
#         y = Math.sin_cos(Math.deg2rad(angles.y))
#         return Vector3(s[1] * y[1], s[1] * y[0], -s[0])

    
#     def vec_normalize(vec):
#         radius = 1.0 / (math.sqrt(vec['x'] * vec['x'] + vec['y'] * vec['y'] + vec['z'] * vec['z']) + 1.192092896e-07)
#         vec['x'] *= radius
#         vec['y'] *= radius
#         vec['z'] *= radius
#         return vec

    
#     def vec_angles(forward):
#         if forward['y'] == 0.00 and forward['x'] == 0.00:
#             yaw = 0
#             pitch = 270.0 if forward['z'] > 0.00 else 90.0
#         else:
#             yaw = math.atan2(forward['y'], forward['x']) * 57.295779513
#             if yaw < 0.00:
#                 yaw += 360.0
#             tmp = math.sqrt(forward['x'] * forward['x'] + forward['y'] * forward['y'])
#             pitch = math.atan2(-forward['z'], tmp) * 57.295779513
#             if pitch < 0.00:
#                 pitch += 360.0
#         return meow.vec3(pitch, yaw, 0.00)

    
#     def vec_clamp(v):
#         if 89.0 < v['x'] <= 180.0:
#             v['x'] = 89.0
#         if v['x'] > 180.0:
#             v['x'] -= 360.0
#         if v['x'] < -89.0:
#             v['x'] = -89.0
#         v['y'] = math.fmod(v['y'] + 180.0, 360.0) - 180.0
#         v['z'] = 0.00
#         return v

    # @staticmethod
    # def vec_dot(v0, v1):
    #     return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

    # @staticmethod
    # def vec_length(v):
    #     return v.x * v.x + v.y * v.y + v.z * v.z

    # @staticmethod
    # def get_fov(va, angle):
    #     a0 = Math.angle_vec(va)
    #     a1 = Math.angle_vec(angle)
    #     return Math.rad2deg(math.acos(Math.vec_dot(a0, a1) / Math.vec_length(a0)))
    
# _target = Entity(0)
# _target_bone = 0
# # 79 = left leg | 72 = right leg | 78 = left knee | 71 = right knee | 6 = upper chest | 41 = left shoulder | 11 = right shoulder | 77 left pelvis | 70 right pelvis | 42 = left elbow | 12 = right elbow
# # _bones = [72, 79, 78, 71, 77, 70, 6, 41, 42, 12, 11, 5, 4, 3, 0, 7, 8]
# _bones = [5, 4, 3, 0, 7, 8]

# g_current_tick = 0
# g_previous_tick = 0


# _target = Entity(0)
# _target_bone = 0
            
# def get_target_angle(local_player, entity, bone_id):
#     bone_pos = entity.get_bone_position(bone_id)
#     eye_pos = local_player.get_eye_pos()
#     eye_pos['x'] = bone_pos['x'] - eye_pos['x']
#     eye_pos['y'] = bone_pos['y'] - eye_pos['y']
#     eye_pos['z'] = bone_pos['z'] - eye_pos['z']
#     eye_pos = Math.vec_angles(Math.vec_normalize(eye_pos))
#     return Math.vec_clamp(eye_pos)


# def target_set(target):
#     global _target
#     _target = target

# def get_best_target(va):
#     global _target_bone
#     local_player = Entity(LocalPlayer.get_local_player())
#     a0 = 9999.9
#     for i in range(1, 64):
#         entity = Engine.get_entity(i)
#         if entity != 0:
#             if local_player.get_team() == entity.get_team() and local_p.get_team_num() == entity.get_team_num():
#                 continue
#             if g_aimbot_head == 1:
#                 fov = Math.get_fov(va, get_target_angle(local_p, entity, 8))
#                 if fov < a0:
#                     a0 = fov
#                     target_set(entity)
#                     _target_bone = 8
#             else:
#                 for j in range(0, _bones.__len__()):
#                     fov = Math.get_fov(va, get_target_angle(local_p, entity, _bones[j]))
#                     if fov < a0:
#                         a0 = fov
#                         target_set(entity)
#                         _target_bone = _bones[j]
#     return a0 != 9999

# def aim_at_target(sensitivity, view_angle, angle):
#     y = view_angle['x'] - angle['x']
#     x = view_angle['y'] - angle['y']
#     if y > 89.0:
#         y = 89.0
#     elif y < -89.0:
#         y = -89.0
#     if x > 180.0:
#         x -= 360.0
#     elif x < -180.0:
#         x += 360.0
#     if math.fabs(x) / 180.0 >= g_aimbot_fov:
#         target_set(Entity(0))
#         return
#     if math.fabs(y) / 89.0 >= g_aimbot_fov:
#         target_set(Entity(0))
#         return
#     x = (x / sensitivity) / 0.022
#     y = (y / sensitivity) / -0.022
#     # if g_aimbot_smooth > 1.00:
#     #     sx = 0.00
#     #     sy = 0.00
#     #     if sx < x:
#     #         sx += 1.0 + (x / g_aimbot_smooth)
#     #     elif sx > x:
#     #         sx -= 1.0 - (x / g_aimbot_smooth)
#     #     if sy < y:
#     #         sy += 1.0 + (y / g_aimbot_smooth)
#     #     elif sy > y:
#     #         sy -= 1.0 - (y / g_aimbot_smooth)
#     # else:
#     sx = x
#     sy = y
#     if g_current_tick - g_previous_tick > 0:
#         g_previous_tick = g_current_tick
#         Windll.u32.mouse_event(0x0001, int(sx), int(sy), 0, 0)

# def aimbot():
#     g_aimbot_fov = 1.1
    
#     while True:
#         try:
#             local_player = Entity(LocalPlayer.get_local_player())
#             view_angle = Engine.get_client_view_angles()
#         except Exception as err:
#             print(err)
#             continue
         
#         for ents in EntityList:
#             try:
#                 entity = Entity(ents)
#                 angle = get_target_angle(local_player, entity, 8)
                
#                 # print(view_angle)
#                 if Windll.u32.GetAsyncKeyState(5):
#                     y = view_angle['x'] - angle['x']
#                     x = view_angle['y'] - angle['y']
#                     if y > 89.0:
#                         y = 89.0
#                     elif y < -89.0:
#                         y = -89.0
#                     if x > 180.0:
#                         x -= 360.0
#                     elif x < -180.0:
#                         x += 360.0
#                     if math.fabs(x) / 180.0 >= g_aimbot_fov:
#                         target_set(Entity(0))
#                         continue
#                     if math.fabs(y) / 89.0 >= g_aimbot_fov:
#                         target_set(Entity(0))
#                         continue
#                     x = (x / sensitivity) / 0.022
#                     y = (y / sensitivity) / -0.022
#                     sx = x
#                     sy = y
#                     # if g_current_tick - g_previous_tick > 0:
#                     #     g_previous_tick = g_current_tick
#                     Windll.u32.mouse_event(0x0001, int(sx), int(sy), 0, 0)
                
#             except Exception as err:
#                 print(err)
# #                 continue 

if __name__ == "__main__":
    try:
        csgo = Process('csgo.exe')
        csgo_client = csgo.get_module("client.dll")
        csgo_engine = csgo.get_module("engine.dll")
    except Exception as err:
        print(err)
        exit(0)
                            
    meow.overlay_init(fps=144, title='test')
    
    try:
        threading.Thread(target=entity_parse, name='entity_parse', daemon=True).start()
        threading.Thread(target=trigger, name='trigger', daemon=True).start()
    except Exception as err:
        print(err)
        exit(0)

    esp()
    
    
#Make a debug file where all values will be displayed and enable only if its imported so in release the file will be excluded, and also make DEBUG_MODE easier
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