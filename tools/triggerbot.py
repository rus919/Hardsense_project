from engine.process import *
from utils.entity import *
from utils.offsets import *
from tools.config import *

import time

def triggerbot():
    while True:
        if Process.csgo:
            try:
                if triggerbotEnabled == 1:
                    if Process.u32.GetAsyncKeyState(triggerbotKey):
                        crosshairID = Entity.getCrosshairID()

                        entity = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwEntityList + (crosshairID - 1) * 0x10)
                        entity = Entity(entity)
                        
                        localplayer = Entity(Entity.localPlayer())
                        
                        player_team = localplayer.getTeam()
                        entity_team = entity.getTeam()

                        if crosshairID > 0 and crosshairID <= 64 and player_team != entity_team:
                            Process.k32.Sleep(triggerbotDelayBeforeShot)
                            Process.u32.mouse_event(0x0002, 0, 0, 0, 0)
                            Process.k32.Sleep(50)
                            Process.u32.mouse_event(0x0004, 0, 0, 0, 0)
                            Process.k32.Sleep(triggerbotDelayAfterShot)
            except Exception as err:
                if Process.DEBUG_MODE:
                    print(err)
                continue
        time.sleep(0.001)