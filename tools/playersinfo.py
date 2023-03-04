from engine.process import *
from utils.entity import *
from utils.offsets import *
from tools.config import *


playersInfoAddr = []
def getPlayerInfo():
    while pm.overlay_loop():
        try:
            # if Entity.getState == 6:
            playersInfoAddr.clear()
            for i in range(1, 32):
                entity = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwEntityList + i * 0x10)
                player_resources = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwPlayerResource)
                if entity != 0:
                                     
                    entityCompRank = pm.r_int(Process.csgo, player_resources + Offset.m_iCompetitiveRanking + (i+1) * 4)
                    entityCompWins = pm.r_int(Process.csgo, player_resources + Offset.m_iCompetitiveWins + (i+1) * 4)
                    
                    if [i, entity ,entityCompRank ,entityCompWins] not in playersInfoAddr:
                        playersInfoAddr.append([i, entity, entityCompRank, entityCompWins])
        except Exception as err:
            print(err)
            pass
        print(playersInfoAddr)
        time.sleep(15.00)