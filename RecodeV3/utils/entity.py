from engine.process import Process
from utils.offsets import Offset
import struct
from pyMeow import vec3

try:
    csgo = Process('csgo.exe')
    csgo_client = csgo.get_module("client.dll")
    csgo_engine = csgo.get_module("engine.dll")
except Exception as err:
    print(err)
    exit(0)

class LocalPlayer():    
    def get_local_player():
        return csgo.read_i32(csgo_client + Offset.dwLocalPlayer)
    
    def get_crosshair_id():
        return csgo.read_i32(LocalPlayer.get_local_player() + Offset.m_iCrosshairId)

class Entity():    
    def __init__(self, entityAddr):
        self.entityObj = entityAddr

    def get_health(self):
        return csgo.read_i32(self.entityObj + Offset.m_iHealth)
    
    def get_dormant(self):
        return csgo.read_i8(self.entityObj + Offset.m_bDormant)
    
    def get_team(self):
        return csgo.read_i8(self.entityObj + Offset.m_iTeamNum)
    
    def get_position(self):
        x = csgo.read_float(self.entityObj + Offset.m_vecOrigin)
        y = csgo.read_float(self.entityObj + Offset.m_vecOrigin + 0x4)
        z = csgo.read_float(self.entityObj + Offset.m_vecOrigin + 0x8)
        return vec3(x, y, z)
    
    def get_bone_position(self, index: int):
        aa = 0x30 * index
        ab = csgo.read_i32(self.entityObj + Offset.m_dwBoneMatrix)
        x = csgo.read_float(ab + aa + 0x0c)
        y = csgo.read_float(ab + aa + 0x1c)
        z = csgo.read_float(ab + aa + 0x2c)
        return vec3(x, y, z)
    
    def get_shots_fired(self):
        return csgo.read_i32(self.entityObj + Offset.m_iShotsFired)

    def get_vec_view(self):
        x = csgo.read_float(self.entityObj + Offset.m_vecViewOffset + 0x0c)
        y = csgo.read_float(self.entityObj + Offset.m_vecViewOffset + 0x1c)
        z = csgo.read_float(self.entityObj + Offset.m_vecViewOffset + 0x2c)
        return vec3(x, y, z)
    
    def get_eye_pos(self):
        v = self.get_vec_view()
        o = self.get_position()
        return vec3(v['x'] + o['x'], v['y'] + o['y'], v['z'] + o['z'])
    
    
class Engine():
    def get_entity(index):
        return csgo.read_i32(csgo_client + Offset.dwEntityList + index * 0x10)
    
    def get_view_matrix():
        view = csgo.read_buffer(csgo_client + Offset.dwViewMatrix, 64)
        matrix = struct.unpack("16f", view)
        return matrix
    
    def get_state():
        return csgo.read_i32(csgo_engine + Offset.dwClientState)
    
    def get_client_state():
        return csgo.read_i32(Engine.get_state() + Offset.dwClientState_State)
    
    def get_client_view_angles():
        x = csgo.read_float(Engine.get_state() + Offset.dwClientState_ViewAngles, 0x0c)
        y = csgo.read_float(Engine.get_state() + Offset.dwClientState_ViewAngles, 0x1c)
        z = csgo.read_float(Engine.get_state() + Offset.dwClientState_ViewAngles, 0x2c)
        return vec3(x, y, z)
    
    def get_GameRulesProxy():
        return csgo.read_i32(csgo_client + Offset.dwGameRulesProxy)
    
    def get_bomb_planted():
        return csgo.read_i32(Engine.get_GameRulesProxy() + Offset.m_bBombPlanted)
    
    # def get_freeze_period():
    #     return csgo.read_i8(Engine.get_GameRulesProxy() + Offset.m_bFreezePeriod)
    
    def get_bomb_ticking(bomb_entity):
        return csgo.read_i8(bomb_entity + 0x2990) # m_bBombTicking
    
    def get_bomb_site(bomb_entity):
        return csgo.read_i8(bomb_entity + 0x2994) # m_nBombSite
    
    def get_curr_time():
        return csgo.read_float(csgo_engine + Offset.dwGlobalVars + 0x10)
    
    def get_bomb_time(bomb_entity):
        return csgo.read_float(bomb_entity + 0x29a0) - Engine.get_curr_time() #To start countdown \ m_flC4Blow
    
    def get_defuse_time(bomb_entity):
        return csgo.read_float(bomb_entity + Offset.m_flDefuseCountDown) - Engine.get_curr_time() #To start countdown 
    
    def is_defusing_bomb(bomb_entity):
        return csgo.read_i8(bomb_entity + 0x29c4) #m_hBombDefuser
    