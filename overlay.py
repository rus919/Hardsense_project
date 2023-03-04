import sys
import pyMeow as pm
from requests import get
import ctypes
from ctypes import *

from utils.offsets import *
from engine.gamedata import *

import threading
import time
import multiprocessing
from multiprocessing import Process

ntdll = windll.ntdll
k32 = windll.kernel32
u32 = windll.user32

DEBUG_MODE = False

class Colors:
    orange = pm.get_color("orange")
    cyan = pm.get_color("cyan")
    white = pm.get_color("white")
    red = pm.get_color("red")
    purple = pm.get_color("purple")
    black = pm.get_color("black")
    # healthEspOverlay = pm.new_color(55, 55, 55, 255)

class Entity():
    def __init__(self, addr, mem, gmod):
        self.wts = None
        self.addr = addr
        self.mem = mem
        self.gmod = gmod
        self.wts2 = None
        
        self.id = pm.r_int(self.mem, self.addr + 0x64)
        self.health = pm.r_int(self.mem, self.addr + Offset.m_iHealth)
        self.dormant = pm.r_int(self.mem, self.addr + Offset.m_bDormant)
        self.team = pm.r_int(self.mem, self.addr + Offset.m_iTeamNum)
        self.bone_base = pm.r_int(self.mem, self.addr + Offset.m_dwBoneMatrix)
        self.pos = pm.r_vec3(self.mem, self.addr + 0xA0) #m_vecAbsOrigin 0xA0 = 160
        self.get_lifestate = pm.r_int(self.mem, self.addr + Offset.m_lifeState)
        
        self.armour = pm.r_int(self.mem, self.addr + Offset.m_ArmorValue)
        self.is_scoped = pm.r_bool(self.mem, self.addr + Offset.m_bIsScoped)
        self.bombSite = pm.r_int(self.mem, self.addr + Offset.m_nBombSite)
        self.bombtest = pm.r_float(self.mem, self.addr + 0x29a0) #m_flC4Blow
        self.bombTicking = pm.r_int(self.mem, self.addr + 0x2990) #m_bBombTicking
        self.defusingTime = pm.r_float(self.mem, self.addr + 0x29bc) #m_flDefuseCountDown
        self.defusingPlayer = pm.r_byte(self.mem, self.addr + 0x29c4) #m_bIsDefusing
        
        self.get_vec_punch = pm.r_vec3(self.mem, self.addr + Offset.m_aimPunchAngle)
        self.get_shots_fired = pm.r_int(self.mem, self.addr + Offset.m_iShotsFired)
        
        
    @property
    def name(self):
        radar_base = pm.r_int(self.mem, self.gmod + Offset.dwRadarBase)
        hud_radar = pm.r_int(self.mem, radar_base + 0x78)
        return pm.r_string(self.mem, hud_radar + 0x300 + (0x174 * (self.id - 1)))
    
    def bone_pos(self, bone_id):
        return pm.vec3(
            pm.r_float(self.mem, self.bone_base + 0x30 * bone_id + 0x0C),
            pm.r_float(self.mem, self.bone_base + 0x30 * bone_id + 0x1C),
            pm.r_float(self.mem, self.bone_base + 0x30 * bone_id + 0x2C),
        )
    
    def class_id(self):
        client_networkable = pm.r_int(self.mem, self.addr + 0x8)
        dwGetClientClassFn = pm.r_int(self.mem, client_networkable + 0x8)
        entity_client_class = pm.r_int(self.mem, dwGetClientClassFn+ 0x1)
        class_id = pm.r_int(self.mem, entity_client_class + 0x14)
        return class_id

    def getWeapon(self, module): #need to pass game_module in module
        getWeaponAddress = pm.r_int(self.mem, self.addr + Offset.m_hActiveWeapon) & 0xFFF
        getWeaponAddressHandle = pm.r_int(self.mem, module + Offset.dwEntityList + (getWeaponAddress - 1) * 0x10)
        return pm.r_int(self.mem, getWeaponAddressHandle + Offset.m_iItemDefinitionIndex)

bombIndexAddr = []
playersInfoAddr = []
_scoping_rifles = [9, 40, 38, 11]

def getBombInfo():
    try:
        csgo_proc = pm.open_process(processName="csgo.exe")
        csgo_client = pm.get_module(csgo_proc, "client.dll")["base"]
        csgo_engine = pm.get_module(csgo_proc, "engine.dll")["base"]
        
        engine_ptr = pm.r_uint(csgo_proc, csgo_engine + Offset.dwClientState)
        get_state = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_State)
    except Exception as err:
        if DEBUG_MODE:
            print(err)
        exit()
    while pm.overlay_loop():
        try:
            if get_state == 6:
                GameRulesProxy = pm.r_int(csgo_proc, csgo_client + Offset.dwGameRulesProxy)
                bombPlanted = pm.r_int(csgo_proc, GameRulesProxy + Offset.m_bBombPlanted)
                
                if bombPlanted == 1:
                    bombIndexAddr.clear()
                    for i in range(350, 550):
                        entity = pm.r_int(csgo_proc, csgo_client + Offset.dwEntityList + i * 0x10)
                        
                        if entity != 0:
                            client_networkable = pm.r_int(csgo_proc, entity + 0x8)
                            dwGetClientClassFn = pm.r_int(csgo_proc, client_networkable + 0x8)
                            entity_client_class = pm.r_int(csgo_proc, dwGetClientClassFn+ 0x1)
                            class_id = pm.r_int(csgo_proc, entity_client_class + 0x14)
                            if class_id == 129:
                                if [entity] not in bombIndexAddr:
                                    bombIndexAddr.append(entity)
                else:
                    bombIndexAddr.clear()
        except Exception as err:
            print(err)
            pass
        time.sleep(1.00)
        
def getPlayerInfo():
    try:
        csgo_proc = pm.open_process(processName="csgo.exe")
        csgo_client = pm.get_module(csgo_proc, "client.dll")["base"]
        csgo_engine = pm.get_module(csgo_proc, "engine.dll")["base"]
        
        engine_ptr = pm.r_uint(csgo_proc, csgo_engine + Offset.dwClientState)
        get_state = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_State)
    except Exception as err:
        if DEBUG_MODE:
            print(err)
        exit()
    while pm.overlay_loop():
        try:
            if get_state == 6:
                playersInfoAddr.clear()
                for i in range(1, 32):
                    entity = pm.r_int(csgo_proc, csgo_client + Offset.dwEntityList + i * 0x10)
                    player_resources = pm.r_int(csgo_proc, csgo_client + Offset.dwPlayerResource)
                    if entity != 0:                        
                        entityCompRank = pm.r_int(csgo_proc, player_resources + Offset.m_iCompetitiveRanking + (i+1) * 4)
                        entityCompWins = pm.r_int(csgo_proc, player_resources + Offset.m_iCompetitiveWins + (i+1) * 4)
                        if [i, entity ,entityCompRank ,entityCompWins] not in playersInfoAddr:
                            playersInfoAddr.append([i, entity, entityCompRank, entityCompWins])
                else:
                    bombIndexAddr.clear()
        except Exception as err:
            print(err)
            pass
        print(playersInfoAddr)
        time.sleep(15.00)
        
def newOverlay():
    try:
        csgo_proc = pm.open_process(processName="csgo.exe")
        csgo_client = pm.get_module(csgo_proc, "client.dll")["base"]
        csgo_engine = pm.get_module(csgo_proc, "engine.dll")["base"]
        
        pm.load_font("assets/fonts/ff.ttf", 0)
        p2000 = pm.load_texture("assets/images/p2000.png")        
    except Exception as err:
        if DEBUG_MODE:
            print(err)
        exit()
        
    while pm.overlay_loop():
        try:
            engine_ptr = pm.r_uint(csgo_proc, csgo_engine + Offset.dwClientState)
            get_state = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_State)
            # none = 0, CHALLENGE = 1, CONNECTED = 2, NEW = 3, PRESPAWN = 4, SPAWN = 5, FULL = 6, CHANGELEVEL = 7
        except Exception as err:
            if DEBUG_MODE:
                print(err)
            pass        

        pm.begin_drawing()
        
        bombTextPos_x = pm.get_screen_width() / 100
        bombTextPos_y = pm.get_screen_height() / 1.5
        
        screen_center_x = pm.get_screen_width() // 2
        screen_center_y = pm.get_screen_height() // 2
        
        # if processInfo.gameFocused:
        pm.draw_text(text = "HARDSENSE", posX = 5, posY = 5, fontSize = 10, color = Colors.purple)
        pm.draw_fps(50, 50)
        
        if get_state == 6:         
            try:
                localPlayerAddr = pm.r_int(csgo_proc, csgo_client + Offset.dwLocalPlayer)
                localPlayer = Entity(localPlayerAddr, csgo_proc, csgo_client)
                
                view_matrix = pm.r_floats(csgo_proc, csgo_client + Offset.dwViewMatrix, 16)  
                currentTime = pm.r_float(csgo_proc, csgo_engine + Offset.dwGlobalVars + 0x0010)

                entAddr = pm.r_ints(csgo_proc, csgo_client + Offset.dwEntityList, 128)[0::4]
                
            except Exception as err:
                if DEBUG_MODE:
                    print("2", err)
                pass         
            
            
            spectatorsArr = []
            for ents in entAddr:
                if ents > 0:
                    try:
                        entity = Entity(ents, csgo_proc, csgo_client)
                        # # print(entity.name)
                        
                        if localPlayer.health > 0:
                            
                            # if entity.team == localPlayer.team:
                            observed_target_handle = pm.r_int(csgo_proc, ents + Offset.m_hObserverTarget) & 0xFFF
                            spectated = pm.r_int(csgo_proc, csgo_client + Offset.dwEntityList + (observed_target_handle - 1) * 0x10)
                                                            
                            if spectated == localPlayerAddr:
                                spectatorsArr.append(entity.name)
                                
                                pm.draw_font(
                                fontId = 0,
                                text= 'Spectators: \n' + '\n'.join(spectatorsArr),
                                posX=500,
                                posY=150,
                                fontSize=25,
                                spacing = 2.0,
                                tint = Colors.purple,
                                )
                                
                        else:
                            spectatorsArr.clear()
                            
                        if not entity.dormant and entity.health > 0 and localPlayer.team != entity.team and ents != localPlayerAddr:
                            entity.wts = pm.world_to_screen(view_matrix, entity.pos, 1)
                            head_pos = pm.world_to_screen(view_matrix, entity.bone_pos(8), 1)
                            
                            head = entity.wts["y"] - head_pos["y"]
                            width = head / 2
                            center = width / 2
                            
                            # entity.getWeapon(csgo_client)

                            pm.draw_circle(
                                centerX = head_pos["x"],
                                centerY = head_pos["y"],
                                radius = 3,
                                color = Colors.red,
                            )
                            
                            # pm.draw_rectangle(
                            # posX=head_pos["x"] - center,
                            # posY=head_pos["y"] - center / 2,
                            # width=width,
                            # height=head + center / 2,
                            # color=Colors.red,
                            # )
                            # pm.draw_rectangle_lines(
                            #     posX=head_pos["x"] - center * 1.0,
                            #     posY=head_pos["y"] - center / 2,
                            #     width=width * 1.0,
                            #     height=head + center / 2,
                            #     color=Colors.red,
                            #     lineThick=1.0,
                            # )
                            if entity.getWeapon(csgo_client) == 32: 
                                pm.draw_texture(
                                    texture = p2000, 
                                    posX = head_pos["x"] / 1.005, 
                                    posY = entity.wts["y"] * 1.01, 
                                    rotation = 0, 
                                    scale = 0.3,
                                    tint = Colors.purple
                                )
                            # pm.draw_text(
                            #     text= f"{entity.getWeapon(csgo_client)}",
                            #     posX=head_pos["x"] - center - 10,
                            #     posY=head_pos["y"] - center - 5,
                            #     fontSize=5,
                            #     color=Colors.red,
                            # )
                            
                            # pm.draw_text(
                            #     text= f"H:{entity.health}",
                            #     posX=head_pos["x"] - center - 25,
                            #     posY=head_pos["y"] - center / 2,
                            #     fontSize=1,
                            #     color=Colors.red,
                            # )
                        
                            # pm.draw_text(
                            #     text= f"A:{entity.armour}",
                            #     posX=head_pos["x"] - center - 25,
                            #     posY=(head_pos["y"] - center / 2) + 10,
                            #     fontSize=1,
                            #     color=Colors.purple,
                            # )
                            # pm.draw_text(
                            #     text= entity.name,
                            #     posX=head_pos["x"] - center - 10,
                            #     posY=head_pos["y"] - center - 5,
                            #     fontSize=5,
                            #     color=Colors.red,
                            # )
                    except Exception as err:
                        if DEBUG_MODE:
                            print("3", err)
                        pass
            
            for bombindex in bombIndexAddr:
                try:
                    entity = Entity(bombindex, csgo_proc, csgo_client)
                    try:
                        entity.wts2 = entity.pos
                        head_pos = pm.world_to_screen(view_matrix, entity.wts2, 1)
                        
                        bombtime = entity.bombtest - currentTime
                        defuseTime = entity.defusingTime - currentTime
                                                        
                        pm.draw_text(
                        text= f"bomb",
                        posX=head_pos["x"],
                        posY=head_pos["y"],
                        fontSize=25,
                        color=Colors.purple,
                        )
                        
                        if defuseTime > bombtime:
                            defuseTimeColor = Colors.red
                        else:
                            defuseTimeColor = Colors.cyan
                        
                        if entity.bombTicking and bombtime > 0:
                            if entity.bombSite == 0:
                                pm.draw_text(
                                text= f"BOMB: A",
                                posX=bombTextPos_x,
                                posY=bombTextPos_y,
                                fontSize=25,
                                color=Colors.cyan,
                                )
                            else:
                                pm.draw_text(
                                text= f"BOMB: B",
                                posX=bombTextPos_x,
                                posY=bombTextPos_y,
                                fontSize=25,
                                color=Colors.cyan,
                                )
                            
                            pm.draw_text(
                            text= f"{bombtime:.3}",
                            posX=bombTextPos_x * 1.05,
                            posY=bombTextPos_y * 1.05,
                            fontSize=25,
                            color=Colors.purple,
                            )
                            if entity.defusingPlayer != 255:
                                pm.draw_text(
                                text= f"{defuseTime:.3}",
                                posX=bombTextPos_x * 1.05,
                                posY=bombTextPos_y * 1.1,
                                fontSize=25,
                                color=defuseTimeColor,
                                )

                    except Exception as err:
                        # print(err)
                        pass
                except Exception as err:
                    if DEBUG_MODE:
                        print("2", err)
                    pass
            
            if localPlayer.health > 0:
                if localPlayer.get_vec_punch["x"] != 0.0:
                    if localPlayer.get_shots_fired > 1:
                        player_fov_x = pm.get_screen_width() // 90
                        player_fov_y = pm.get_screen_height() // 90
                        crosshair_x = screen_center_x - player_fov_x * localPlayer.get_vec_punch["y"]
                        crosshair_y = screen_center_y - player_fov_y * -localPlayer.get_vec_punch["x"]
                        pm.draw_circle(
                            centerX = crosshair_x,
                            centerY = crosshair_y,
                            radius = 2,
                            color = Colors.white,
                        )
            
            
            # if localPlayer.health > 0 and localPlayer.get_lifestate == 0:
            #     if localPlayer.getWeapon(csgo_client) in _scoping_rifles:
            #         if not localPlayer.is_scoped:
            #             pm.draw_circle(
            #                 centerX = screen_center_x,
            #                 centerY = screen_center_y,
            #                 radius = 3,
            #                 color = Colors.red,
            #             ) 
        pm.end_drawing()

def trigger():
        try:
            csgo_proc = pm.open_process(processName="csgo.exe")
            csgo_client = pm.get_module(csgo_proc, "client.dll")["base"]
            csgo_engine = pm.get_module(csgo_proc, "engine.dll")["base"]
            
            engine_ptr = pm.r_uint(csgo_proc, csgo_engine + Offset.dwClientState)
            get_state = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_State)
        except Exception as err:
            if DEBUG_MODE:
                print(err)
            exit()
            
        while True:
            try:
                if u32.GetAsyncKeyState(0x05):
                    localPlayerAddr = pm.r_int(csgo_proc, csgo_client + Offset.dwLocalPlayer)
                    # localPlayer = Entity(localPlayerAddr, csgo_proc, csgo_client)
                    
                    # player = pm.r_int(csgo_proc, csgo_client + Offset.dwLocalPlayer)
                    entity_id = pm.r_int(csgo_proc, localPlayerAddr + Offset.m_iCrosshairId)
                    entity = pm.r_int(csgo_proc, csgo_client + Offset.dwEntityList + (entity_id - 1) * 0x10)

                    entity_team = pm.r_int(csgo_proc, entity + Offset.m_iTeamNum)
                    player_team = pm.r_int(csgo_proc, localPlayerAddr + Offset.m_iTeamNum)

                    if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
                        # k32.Sleep(5)
                        u32.mouse_event(0x0002, 0, 0, 0, 0)
                        k32.Sleep(50)
                        u32.mouse_event(0x0004, 0, 0, 0, 0)
                        k32.Sleep(150)
            except Exception as err:
                if DEBUG_MODE:
                    print(err)
                continue
            time.sleep(0.0001)

def main():
    threading.Thread(target=processInfo.checkGameFocus, name='checkGameFocus', daemon=True).start()
    threading.Thread(target=getBombInfo, name='getBombInfo', daemon=True).start()
    threading.Thread(target=getPlayerInfo, name='getPlayerInfo', daemon=True).start()
    threading.Thread(target=trigger, name='trigger', daemon=True).start()
    # proc = Process(target=test2)
    # proc.start()
    # threading.Thread(target=test2, name='test2', daemon=True).start()
    newOverlay() #start after all processes
    # proc.join()
if __name__ == "__main__":
    pm.overlay_init(fps=1000, title='test')
    main()