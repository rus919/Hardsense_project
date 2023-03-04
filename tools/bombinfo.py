from engine.process import *
from utils.entity import *
from utils.offsets import *
from tools.config import *

bombIndexAddr = []

def getBombInfo():
    while pm.overlay_loop():
        try:
            GameRulesProxy = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwGameRulesProxy)
            bombPlanted = pm.r_int(Process.csgo, GameRulesProxy + Offset.m_bBombPlanted)
            if bombPlanted == 1:
                bombIndexAddr.clear()
                for i in range(300, 550):
                    entity = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwEntityList + i * 0x10)
                    if entity != 0:
                        
                        client_networkable = pm.r_int(Process.csgo, entity + 0x8)
                        dwGetClientClassFn = pm.r_int(Process.csgo, client_networkable + 0x8)
                        entity_client_class = pm.r_int(Process.csgo, dwGetClientClassFn+ 0x1)
                        class_id = pm.r_int(Process.csgo, entity_client_class + 0x14)
                        if class_id == 129:
                            if [entity] not in bombIndexAddr:
                                bombIndexAddr.append(entity)
            else:
                bombIndexAddr.clear()
        except Exception as err:
            print(err)
            pass
        # print(bombPlanted)
        
        time.sleep(1.00)