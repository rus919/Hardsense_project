from engine.process import *
from utils.offsets import *

class Entity2():
    def __init__(self, entityAddr):
        self.w2s = None
        self.entityObj = entityAddr
 
    def localPlayer():
        return pm.r_int(Process.csgo, Process.csgo_client + Offset.dwLocalPlayer)
    
    def getCrosshairID():
        return pm.r_int(Process.csgo, Entity.localPlayer() + Offset.m_iCrosshairId)

    # def health(self):
    #     return pm.r_int(Process.csgo, self.entityObj + Offset.m_iHealth)
    
    # def dormant(self):
    #     return pm.r_int(Process.csgo, self.entityObj + Offset.m_bDormant)

    def getTeam(self):
        return pm.r_int(Process.csgo, self.entityObj + Offset.m_iTeamNum)
    
    def getState():
        engine_ptr = pm.r_int(Process.csgo, Process.csgo_engine + Offset.dwClientState)
        return pm.r_int(Process.csgo, engine_ptr + Offset.dwClientState_State)
    
    # def position(self):
    #     return pm.r_vec3(Process.csgo, self.entityObj + Offset.m_vecOrigin)
    
    # def viewMatrix():
    #     return pm.r_floats(Process.csgo, Process.csgo_client + Offset.dwViewMatrix, 16)
    
    # def boneBase(self):
    #     return pm.r_int(Process.csgo, self.entityObj + Offset.m_dwBoneMatrix)
    
    # def playerCrosshairIndex():
    #     return pm.r_uint(Process.csgo, Entity.localPlayer() + Offset.m_iCrosshairId)
    
    # def getCrosshairPlayer():
    #     return pm.r_uint(Process.csgo, Process.csgo_client + Offset.dwEntityList + (Entity.playerCrosshairIndex() - 1) * 0x10)
    
    # def getMaxPlayers():
    #     return pm.r_int(Process.csgo, Process.csgo_client + Offset.dwClientState_MaxPlayer)

    # def bone_pos(self, bone_id):
    #     return pm.vec3(
    #         pm.r_float(Process.csgo, Entity.boneBase(self) + 0x30 * bone_id + 0x0C),
    #         pm.r_float(Process.csgo, Entity.boneBase(self) + 0x30 * bone_id + 0x1C),
    #         pm.r_float(Process.csgo, Entity.boneBase(self) + 0x30 * bone_id + 0x2C),
    #     )