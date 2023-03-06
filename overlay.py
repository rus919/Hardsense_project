import sys
import pyMeow as pm
from requests import get
import ctypes
from ctypes import *

from utils.offsets import *

from engine.process import *
from engine.gamedata import *

from utils.entity import *

import threading
import time

# from tools.config import *

ntdll = windll.ntdll
k32 = windll.kernel32
u32 = windll.user32

DEBUG_MODE = True

class featureState():
    wallhackNameActive = 0

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

    def getWeapon(self, module): #need to pass client_state in module
        getWeaponAddress = pm.r_int(self.mem, self.addr + Offset.m_hActiveWeapon) & 0xFFF
        getWeaponAddressHandle = pm.r_int(self.mem, module + Offset.dwEntityList + (getWeaponAddress - 1) * 0x10)
        return pm.r_int16(self.mem, getWeaponAddressHandle + Offset.m_iItemDefinitionIndex)
    
    # def getPlayerSteamID(module):
    #     player_info = pm.r_int(self.mem, module + Offset.dwClientState_PlayerInfo)
    #     player_info_items = pm.r_int(self.mem, pm.r_int(self.mem, player_info + 0x40) + 0xC)
    #     return pm.r_int(self.mem, player_info_items + 0x28 + ((i-1) * 0x34))

playersInfoAddr = []
def getPlayerInfo():
    try:
        csgo_proc = pm.open_process(processName="csgo.exe")
        csgo_client = pm.get_module(csgo_proc, "client.dll")["base"]
        csgo_engine = pm.get_module(csgo_proc, "engine.dll")["base"]
        engine_ptr = pm.r_uint(csgo_proc, csgo_engine + Offset.dwClientState)
        # print(engine_ptr)
        get_state = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_State)
    except Exception as err:
        print(err)
        exit(0)
    
    if get_state == 6:
        try:
            playersInfoAddr.clear()
            for i in range(1, 32):
                
                
                entity = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwEntityList + i * 0x10)
                localPlayerAddr = pm.r_int(csgo_proc, csgo_client + Offset.dwLocalPlayer)                
                
                player_resources = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwPlayerResource)
                if entity != 0 and entity != localPlayerAddr:
                    
                    player_info = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_PlayerInfo)
                    aox = pm.r_int(csgo_proc, player_info + 0x40)
                    dxa = pm.r_int(csgo_proc, aox + 0xC)
                    xea = pm.r_int(csgo_proc, dxa + 0x28 + (i * 0x34))
                    playerSteamID = pm.r_string(csgo_proc, xea + 0x94) # Getting steamID32
                    id_split = playerSteamID.split(":") #Convert steamID32 to array
                    steam64id = 76561197960265728 #Base for adding
                    steam64id += int(id_split[2]) * 2 #Take the player ID in [2] and *2 then add to steam64id, if steamID32 [1] contains 1 then add +1 = steamID64
                    if id_split[1] == "1":
                        steam64id += 1
                    
                    ents = Entity(entity, Process.csgo, Process.csgo_client)
                                        
                    entityCompRank = pm.r_int(Process.csgo, player_resources + Offset.m_iCompetitiveRanking + (i+1) * 4)
                    entityCompWins = pm.r_int(Process.csgo, player_resources + Offset.m_iCompetitiveWins + (i+1) * 4)
                    
                    if [i, ents.name, ents.team ,entityCompRank ,entityCompWins, steam64id] not in playersInfoAddr:
                        playersInfoAddr.append([i, ents.name, ents.team, entityCompRank, entityCompWins, steam64id])
        except Exception as err:
            print(err)
            pass
    print(playersInfoAddr)
    # time.sleep(15.00)

bombIndexAddr = []
# def getBombInfo():
#     while pm.overlay_loop():
#         try:
#             GameRulesProxy = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwGameRulesProxy)
#             bombPlanted = pm.r_int(Process.csgo, GameRulesProxy + Offset.m_bBombPlanted)
#             if bombPlanted == 1:
#                 bombIndexAddr.clear()
#                 for i in range(300, 550):
#                     entity = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwEntityList + i * 0x10)
#                     if entity != 0:
                        
#                         client_networkable = pm.r_int(Process.csgo, entity + 0x8)
#                         dwGetClientClassFn = pm.r_int(Process.csgo, client_networkable + 0x8)
#                         entity_client_class = pm.r_int(Process.csgo, dwGetClientClassFn+ 0x1)
#                         class_id = pm.r_int(Process.csgo, entity_client_class + 0x14)
#                         # print(class_id)
#                         if class_id == 129:
#                             if [entity] not in bombIndexAddr:
#                                 bombIndexAddr.append(entity)
#             else:
#                 bombIndexAddr.clear()
#         except Exception as err:
#             print(err)
#             pass
#         # print(bombPlanted)
        
#         time.sleep(1.00)

def newOverlay():
    try:
        csgo_proc = pm.open_process(processName="csgo.exe")
        csgo_client = pm.get_module(csgo_proc, "client.dll")["base"]
        csgo_engine = pm.get_module(csgo_proc, "engine.dll")["base"]
        
        Desert_Eagle= pm.load_texture("assets/images/desert_eagle.png")
        Dual_Berettas = pm.load_texture("assets/images/elite.png")
        Five_SeveN= pm.load_texture("assets/images/fiveseven.png")
        p2000 = pm.load_texture("assets/images/p2000.png")
        Glock_18= pm.load_texture("assets/images/glock.png")
        AK_47 = pm.load_texture("assets/images/ak47.png")
        AUG = pm.load_texture("assets/images/aug.png")
        AWP = pm.load_texture("assets/images/awp.png")
        FAMAS = pm.load_texture("assets/images/famas.png")
        G3SG1 = pm.load_texture("assets/images/g3sg1.png")
        Galil_AR= pm.load_texture("assets/images/galil.png")
        M249= pm.load_texture("assets/images/m249.png")
        M4A4= pm.load_texture("assets/images/m4a4.png")
        MAC_10= pm.load_texture("assets/images/mac10.png")
        P90 = pm.load_texture("assets/images/p90.png")
        MP5_SD= pm.load_texture("assets/images/mp5.png")
        UMP_45= pm.load_texture("assets/images/ump.png")
        XM1014= pm.load_texture("assets/images/xm104.png")
        Bizon = pm.load_texture("assets/images/bizon.png")
        MAG_7 = pm.load_texture("assets/images/mag7.png")
        Negev = pm.load_texture("assets/images/negev.png")
        Sawed_Off = pm.load_texture("assets/images/sawedoff.png")
        Tec_9 = pm.load_texture("assets/images/tec9.png")
        Zeus= pm.load_texture("assets/images/zeus_x27.png")
        MP7 = pm.load_texture("assets/images/mp7.png")
        MP9 = pm.load_texture("assets/images/mp9.png")
        Nova= pm.load_texture("assets/images/nova.png")
        P250= pm.load_texture("assets/images/p250.png")
        SCAR_20 = pm.load_texture("assets/images/scar20.png")
        SG_553= pm.load_texture("assets/images/sg553.png")
        SSG_08= pm.load_texture("assets/images/ssg08.png")
        M4A1_S= pm.load_texture("assets/images/m4a1_silencer.png")
        USP_S = pm.load_texture("assets/images/usp_silencer.png")
        CZ75_Auto = pm.load_texture("assets/images/cz75a.png")
        R8_Revolver = pm.load_texture("assets/images/r8_revolver.png")
        
        Knife = pm.load_texture("assets/images/knife.png")
        
        Flashbang = pm.load_texture("assets/images/flash_grenade.png")
        Explosive_Grenade = pm.load_texture("assets/images/explosive_grenade.png")
        Smoke_Grenade = pm.load_texture("assets/images/smoke_grenade.png")
        Molotov = pm.load_texture("assets/images/molotov.png")
        Decoy_Grenade = pm.load_texture("assets/images/decoy_grenade.png")
        Incendiary_Grenade = pm.load_texture("assets/images/incendiary_grenade.png")
        C4 = pm.load_texture("assets/images/c4.png")
        
        pm.load_font("assets/fonts/ff.ttf", 0)

    except Exception as err:
        if DEBUG_MODE:
            print("001", err)
        exit()
        
    while pm.overlay_loop():
        try:
            engine_ptr = pm.r_uint(csgo_proc, csgo_engine + Offset.dwClientState)
            get_state = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_State)
            # none = 0, CHALLENGE = 1, CONNECTED = 2, NEW = 3, PRESPAWN = 4, SPAWN = 5, FULL = 6, CHANGELEVEL = 7
        except Exception as err:
            if DEBUG_MODE:
                print("002", err)
            quit(0)        

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
                # print(localPlayerAddr)
                
                view_matrix = pm.r_floats(csgo_proc, csgo_client + Offset.dwViewMatrix, 16)  
                currentTime = pm.r_float(csgo_proc, csgo_engine + Offset.dwGlobalVars + 0x0010)

                entAddr = pm.r_ints(csgo_proc, csgo_client + Offset.dwEntityList, 128)[0::4]

                # print(entAddr)
                # print(entAddr)
            except Exception as err:
                if DEBUG_MODE:
                    print("003", err)
                pass         
                        
            for bombindex in bombIndexAddr:
                try:
                    entity = Entity(bombindex, csgo_proc, csgo_client)
                    try:
                        entity.wts2 = entity.pos
                        head_pos = pm.world_to_screen(view_matrix, entity.wts2, 1)
                        
                        bombtime = entity.bombtest - currentTime
                        defuseTime = entity.defusingTime - currentTime
                        
                        pm.draw_texture(texture = C4, posX = head_pos["x"], posY = head_pos["y"], rotation = 0, scale = 0.6,tint = Colors.white)         
                        
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
                        print("004", err)
                    pass
            
            
            if localPlayerAddr != 0:
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
            
            # print(localPlayer.get_lifestate)
            # if localPlayer.health > 0 and localPlayer.get_lifestate == 0:
            #     try:
            #         localPlayerWeapon = localPlayer.getWeapon(csgo_client)
            #         if localPlayerWeapon == 9 or localPlayerWeapon == 11 or localPlayerWeapon == 38 or localPlayerWeapon == 40:
            #             if not localPlayer.is_scoped:
            #                 pm.draw_circle(
            #                     centerX = screen_center_x,
            #                     centerY = screen_center_y,
            #                     radius = 3,
            #                     color = Colors.red,
            #                 )
            #     except Exception as err:
            #         print(err)
            #         pass
            
            # if localPlayerAddr != 0:
            #     for i in range(1, 32):
            #         try:
            #             entity = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwEntityList + i * 0x10)
                        
            #             if entity > 0:
            #                 player_info = pm.r_int(csgo_proc, engine_ptr + Offset.dwClientState_PlayerInfo)
            #                 aox = pm.r_int(csgo_proc, player_info + 0x40)
            #                 dxa = pm.r_int(csgo_proc, aox + 0xC)
            #                 xea = pm.r_int(csgo_proc, dxa + 0x28 + (i * 0x34))
            #                 xeaa = pm.r_string(csgo_proc, xea + 0x94)
            #                 print(xeaa)
            #         except Exception as err:
            #             print(err)
            #             continue
            
            spectatorsArr = []
            for ents in entAddr:                    
                if ents > 0:
                    try:
                        entity = Entity(ents, csgo_proc, csgo_client)
                        if localPlayer.health > 0:
                            
                            if entity.team == localPlayer.team:
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
                                
                        else:
                            spectatorsArr.clear()
                            
                        if not entity.dormant and entity.health > 0 and localPlayer.team != entity.team and ents != localPlayerAddr:
                            entity.wts = pm.world_to_screen(view_matrix, entity.pos, 1)
                            head_pos = pm.world_to_screen(view_matrix, entity.bone_pos(8), 1)
                            
                            head = entity.wts["y"] - head_pos["y"]
                            width = head / 2
                            center = width / 2
                            
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
                            getEntWeapon = entity.getWeapon(csgo_client)

                            if getEntWeapon == 42 or getEntWeapon == 59 or getEntWeapon == 42 or getEntWeapon == 500 or getEntWeapon == 503 or getEntWeapon == 505 or getEntWeapon == 506 or getEntWeapon == 507 or getEntWeapon == 508 or getEntWeapon == 509 or getEntWeapon == 510 or getEntWeapon == 511 or getEntWeapon == 512 or getEntWeapon == 513 or getEntWeapon == 514 or getEntWeapon == 515 or getEntWeapon == 516 or getEntWeapon == 517 or getEntWeapon == 518 or getEntWeapon == 519 or getEntWeapon == 520 or getEntWeapon == 521 or getEntWeapon == 522 or getEntWeapon == 523 or getEntWeapon == 524 or getEntWeapon == 525: 
                                pm.draw_texture(texture = Knife, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                                
                            if getEntWeapon == 1: pm.draw_texture(texture = Desert_Eagle, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 2: pm.draw_texture(texture = Dual_Berettas, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 3: pm.draw_texture(texture = Five_SeveN, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 4: pm.draw_texture(texture = Glock_18, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 7: pm.draw_texture(texture = AK_47, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 8: pm.draw_texture(texture = AUG, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 9: pm.draw_texture(texture = AWP, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 10: pm.draw_texture(texture = FAMAS, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 11: pm.draw_texture(texture = G3SG1, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 13: pm.draw_texture(texture = Galil_AR, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 14: pm.draw_texture(texture = M249, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 16: pm.draw_texture(texture = M4A4, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 17: pm.draw_texture(texture = MAC_10, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 19: pm.draw_texture(texture = P90, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 23: pm.draw_texture(texture = MP5_SD, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 24: pm.draw_texture(texture = UMP_45, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 25: pm.draw_texture(texture = XM1014, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 26: pm.draw_texture(texture = Bizon, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 27: pm.draw_texture(texture = MAG_7, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 28: pm.draw_texture(texture = Negev, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 29: pm.draw_texture(texture = Sawed_Off, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 30: pm.draw_texture(texture = Tec_9, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 31: pm.draw_texture(texture = Zeus, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 32: pm.draw_texture(texture = p2000, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 33: pm.draw_texture(texture = MP7, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 34: pm.draw_texture(texture = MP9, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 35: pm.draw_texture(texture = Nova, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 36: pm.draw_texture(texture = P250, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 38: pm.draw_texture(texture = SCAR_20, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 39: pm.draw_texture(texture = SG_553, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 40: pm.draw_texture(texture = SSG_08, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 60: pm.draw_texture(texture = M4A1_S, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 61: pm.draw_texture(texture = USP_S, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 63: pm.draw_texture(texture = CZ75_Auto, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 64: pm.draw_texture(texture = R8_Revolver, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            
                            if getEntWeapon == 43: pm.draw_texture(texture = Flashbang, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 44: pm.draw_texture(texture = Explosive_Grenade, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 45: pm.draw_texture(texture = Smoke_Grenade, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 46: pm.draw_texture(texture = Molotov, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 47: pm.draw_texture(texture = Decoy_Grenade, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 48: pm.draw_texture(texture = Incendiary_Grenade, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if getEntWeapon == 49: pm.draw_texture(texture = C4, posX = head_pos["x"] / 1.005, posY = entity.wts["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            
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
                            if featureState.wallhackNameActive:
                                pm.draw_text(
                                    text= entity.name,
                                    posX=head_pos["x"] - center - 10,
                                    posY=head_pos["y"] - center - 5,
                                    fontSize=5,
                                    color=Colors.red,
                                )
                    except Exception as err:
                        # if DEBUG_MODE:
                            # print("005", err)
                        pass
        pm.end_drawing()

def triggerbot(): # Check if game is running, memory leak when game is closed #
    while True:
        if Process.csgo:
            engine_ptr = pm.r_uint(Process.csgo, Process.csgo_engine + Offset.dwClientState)
            get_state = pm.r_int(Process.csgo, engine_ptr + Offset.dwClientState_State)
            if get_state == 6:
                try:
                        if Process.u32.GetAsyncKeyState(6):
                            localPlayerAddr = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwLocalPlayer)
                            crosshairID = pm.r_int(Process.csgo, localPlayerAddr + Offset.m_iCrosshairId)

                            entity = pm.r_int(Process.csgo, Process.csgo_client + Offset.dwEntityList + (crosshairID - 1) * 0x10)
                            entity = Entity(entity, Process.csgo, Process.csgo_client)
                            
                            localplayer = Entity(localPlayerAddr, Process.csgo, Process.csgo_client)
                            
                            player_team = localplayer.team
                            entity_team = entity.team

                            if crosshairID > 0 and crosshairID <= 64 and player_team != entity_team:
                                Process.k32.Sleep(0)
                                Process.u32.mouse_event(0x0002, 0, 0, 0, 0)
                                Process.k32.Sleep(50)
                                Process.u32.mouse_event(0x0004, 0, 0, 0, 0)
                                Process.k32.Sleep(150)
                except Exception as err:
                    if Process.DEBUG_MODE:
                        print("006", err)
                    continue
        time.sleep(0.01)

import webbrowser


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 550)
        MainWindow.setMinimumSize(QtCore.QSize(700, 550))
        MainWindow.setMaximumSize(QtCore.QSize(700, 550))
        MainWindow.setStyleSheet("QMainWindow {background: transparent; }\n"
"\n"
"*{\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    background: none;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"    color: #fff;\n"
"}\n"
"\n"
"#centralwidget{\n"
"    background-color: #1f232a;\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background: transparent;\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftMenuContainer = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuContainer.sizePolicy().hasHeightForWidth())
        self.leftMenuContainer.setSizePolicy(sizePolicy)
        self.leftMenuContainer.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.leftMenuContainer.setObjectName("leftMenuContainer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.leftMenuContainer)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leftMenuSubContainer = QtWidgets.QWidget(self.leftMenuContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuSubContainer.sizePolicy().hasHeightForWidth())
        self.leftMenuSubContainer.setSizePolicy(sizePolicy)
        self.leftMenuSubContainer.setObjectName("leftMenuSubContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.leftMenuSubContainer)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.leftMenuHeaderContainer = QtWidgets.QFrame(self.leftMenuSubContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuHeaderContainer.sizePolicy().hasHeightForWidth())
        self.leftMenuHeaderContainer.setSizePolicy(sizePolicy)
        self.leftMenuHeaderContainer.setStyleSheet("")
        self.leftMenuHeaderContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftMenuHeaderContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftMenuHeaderContainer.setObjectName("leftMenuHeaderContainer")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.leftMenuHeaderContainer)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.leftMenuBtn = QtWidgets.QPushButton(self.leftMenuHeaderContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuBtn.sizePolicy().hasHeightForWidth())
        self.leftMenuBtn.setSizePolicy(sizePolicy)
        self.leftMenuBtn.setMinimumSize(QtCore.QSize(50, 40))
        self.leftMenuBtn.setStyleSheet("QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"")
        self.leftMenuBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/assets/UI/menu_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftMenuBtn.setIcon(icon)
        self.leftMenuBtn.setIconSize(QtCore.QSize(34, 34))
        self.leftMenuBtn.setObjectName("leftMenuBtn")
        self.verticalLayout_3.addWidget(self.leftMenuBtn)
        self.verticalLayout_2.addWidget(self.leftMenuHeaderContainer, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.leftMenuMainContainer = QtWidgets.QFrame(self.leftMenuSubContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuMainContainer.sizePolicy().hasHeightForWidth())
        self.leftMenuMainContainer.setSizePolicy(sizePolicy)
        self.leftMenuMainContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftMenuMainContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftMenuMainContainer.setObjectName("leftMenuMainContainer")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.leftMenuMainContainer)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.wallhackBtn = QtWidgets.QPushButton(self.leftMenuMainContainer)
        self.wallhackBtn.setMinimumSize(QtCore.QSize(50, 60))
        self.wallhackBtn.setStyleSheet("QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"")
        self.wallhackBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/assets/UI/eye_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.wallhackBtn.setIcon(icon1)
        self.wallhackBtn.setIconSize(QtCore.QSize(36, 36))
        self.wallhackBtn.setObjectName("wallhackBtn")
        self.verticalLayout_4.addWidget(self.wallhackBtn)
        self.playersBtn = QtWidgets.QPushButton(self.leftMenuMainContainer)
        self.playersBtn.setMinimumSize(QtCore.QSize(50, 60))
        self.playersBtn.setStyleSheet("QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"")
        self.playersBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/assets/UI/players_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playersBtn.setIcon(icon2)
        self.playersBtn.setIconSize(QtCore.QSize(36, 36))
        self.playersBtn.setObjectName("playersBtn")
        self.verticalLayout_4.addWidget(self.playersBtn)
        self.verticalLayout_2.addWidget(self.leftMenuMainContainer, 0, QtCore.Qt.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.leftMenuFooterContainer = QtWidgets.QFrame(self.leftMenuSubContainer)
        self.leftMenuFooterContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftMenuFooterContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftMenuFooterContainer.setObjectName("leftMenuFooterContainer")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.leftMenuFooterContainer)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.userBtnContainer = QtWidgets.QWidget(self.leftMenuFooterContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userBtnContainer.sizePolicy().hasHeightForWidth())
        self.userBtnContainer.setSizePolicy(sizePolicy)
        self.userBtnContainer.setStyleSheet("")
        self.userBtnContainer.setObjectName("userBtnContainer")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.userBtnContainer)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_5.addWidget(self.userBtnContainer, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.settingsBtn = QtWidgets.QPushButton(self.leftMenuFooterContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsBtn.sizePolicy().hasHeightForWidth())
        self.settingsBtn.setSizePolicy(sizePolicy)
        self.settingsBtn.setMinimumSize(QtCore.QSize(50, 60))
        self.settingsBtn.setStyleSheet("QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"")
        self.settingsBtn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/settings_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settingsBtn.setIcon(icon3)
        self.settingsBtn.setIconSize(QtCore.QSize(36, 36))
        self.settingsBtn.setObjectName("settingsBtn")
        self.verticalLayout_5.addWidget(self.settingsBtn)
        self.verticalLayout_2.addWidget(self.leftMenuFooterContainer, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout.addWidget(self.leftMenuSubContainer, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout.addWidget(self.leftMenuContainer, 0, QtCore.Qt.AlignLeft)
        self.mainBodyContainer = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBodyContainer.sizePolicy().hasHeightForWidth())
        self.mainBodyContainer.setSizePolicy(sizePolicy)
        self.mainBodyContainer.setStyleSheet("background-color: transparent;")
        self.mainBodyContainer.setObjectName("mainBodyContainer")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.mainBodyContainer)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.headerContainer = QtWidgets.QWidget(self.mainBodyContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerContainer.sizePolicy().hasHeightForWidth())
        self.headerContainer.setSizePolicy(sizePolicy)
        self.headerContainer.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.headerContainer.setObjectName("headerContainer")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.headerContainer)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rightBtnContainer = QtWidgets.QWidget(self.headerContainer)
        self.rightBtnContainer.setStyleSheet("background-color: transparent;")
        self.rightBtnContainer.setObjectName("rightBtnContainer")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.rightBtnContainer)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.headerBtnMinimise = QtWidgets.QPushButton(self.rightBtnContainer)
        self.headerBtnMinimise.setMinimumSize(QtCore.QSize(40, 40))
        self.headerBtnMinimise.setStyleSheet("QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.headerBtnMinimise.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/assets/UI/minus_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.headerBtnMinimise.setIcon(icon4)
        self.headerBtnMinimise.setIconSize(QtCore.QSize(24, 24))
        self.headerBtnMinimise.setObjectName("headerBtnMinimise")
        self.horizontalLayout_6.addWidget(self.headerBtnMinimise)
        self.headerBtnClose = QtWidgets.QPushButton(self.rightBtnContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerBtnClose.sizePolicy().hasHeightForWidth())
        self.headerBtnClose.setSizePolicy(sizePolicy)
        self.headerBtnClose.setMinimumSize(QtCore.QSize(40, 40))
        self.headerBtnClose.setStyleSheet("QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.headerBtnClose.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/assets/UI/cross_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.headerBtnClose.setIcon(icon5)
        self.headerBtnClose.setIconSize(QtCore.QSize(24, 24))
        self.headerBtnClose.setObjectName("headerBtnClose")
        self.horizontalLayout_6.addWidget(self.headerBtnClose)
        self.horizontalLayout_3.addWidget(self.rightBtnContainer, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.verticalLayout_6.addWidget(self.headerContainer, 0, QtCore.Qt.AlignTop)
        self.mainBodyContent = QtWidgets.QFrame(self.mainBodyContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBodyContent.sizePolicy().hasHeightForWidth())
        self.mainBodyContent.setSizePolicy(sizePolicy)
        self.mainBodyContent.setStyleSheet("")
        self.mainBodyContent.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainBodyContent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainBodyContent.setObjectName("mainBodyContent")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.mainBodyContent)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.mainBodyWidget = QtWidgets.QStackedWidget(self.mainBodyContent)
        self.mainBodyWidget.setStyleSheet("")
        self.mainBodyWidget.setObjectName("mainBodyWidget")
        self.playersPage = QtWidgets.QWidget()
        self.playersPage.setStyleSheet("")
        self.playersPage.setObjectName("playersPage")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.playersPage)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.playersTopBar = QtWidgets.QWidget(self.playersPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersTopBar.sizePolicy().hasHeightForWidth())
        self.playersTopBar.setSizePolicy(sizePolicy)
        self.playersTopBar.setStyleSheet("background-color: rgb(29, 32, 40);")
        self.playersTopBar.setObjectName("playersTopBar")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.playersTopBar)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.playersRefreshMsgContainer = QtWidgets.QWidget(self.playersTopBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersRefreshMsgContainer.sizePolicy().hasHeightForWidth())
        self.playersRefreshMsgContainer.setSizePolicy(sizePolicy)
        self.playersRefreshMsgContainer.setObjectName("playersRefreshMsgContainer")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.playersRefreshMsgContainer)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.playersRefreshMsg = QtWidgets.QLabel(self.playersRefreshMsgContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersRefreshMsg.sizePolicy().hasHeightForWidth())
        self.playersRefreshMsg.setSizePolicy(sizePolicy)
        self.playersRefreshMsg.setMinimumSize(QtCore.QSize(0, 20))
        self.playersRefreshMsg.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRefreshMsg.setFont(font)
        self.playersRefreshMsg.setStyleSheet("")
        self.playersRefreshMsg.setObjectName("playersRefreshMsg")
        self.horizontalLayout_7.addWidget(self.playersRefreshMsg)
        self.horizontalLayout_5.addWidget(self.playersRefreshMsgContainer, 0, QtCore.Qt.AlignLeft)
        self.playersRefreshBtnContainer = QtWidgets.QWidget(self.playersTopBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersRefreshBtnContainer.sizePolicy().hasHeightForWidth())
        self.playersRefreshBtnContainer.setSizePolicy(sizePolicy)
        self.playersRefreshBtnContainer.setMinimumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtnContainer.setMaximumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtnContainer.setStyleSheet("QWidget{\n"
"    background-color: rgb(27, 29, 55);\n"
"}\n"
"QWidget:hover {\n"
"    background-color: rgb(33, 37, 60);\n"
"}\n"
"QWidget:pressed {\n"
"    background-color: rgb(33, 37, 255);\n"
"}\n"
"")
        self.playersRefreshBtnContainer.setObjectName("playersRefreshBtnContainer")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.playersRefreshBtnContainer)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.playersRefreshBtn = QtWidgets.QPushButton(self.playersRefreshBtnContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersRefreshBtn.sizePolicy().hasHeightForWidth())
        self.playersRefreshBtn.setSizePolicy(sizePolicy)
        self.playersRefreshBtn.setMinimumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtn.setMaximumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtn.setStyleSheet("")
        self.playersRefreshBtn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/assets/UI/refresh_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playersRefreshBtn.setIcon(icon6)
        self.playersRefreshBtn.setIconSize(QtCore.QSize(24, 24))
        self.playersRefreshBtn.setObjectName("playersRefreshBtn")
        self.verticalLayout_16.addWidget(self.playersRefreshBtn)
        self.horizontalLayout_5.addWidget(self.playersRefreshBtnContainer, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_8.addWidget(self.playersTopBar)
        self.playersContainer = QtWidgets.QWidget(self.playersPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersContainer.sizePolicy().hasHeightForWidth())
        self.playersContainer.setSizePolicy(sizePolicy)
        self.playersContainer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.playersContainer.setFont(font)
        self.playersContainer.setStyleSheet("background-color: hsl(223, 14, 54, 50%);\n"
"")
        self.playersContainer.setObjectName("playersContainer")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.playersContainer)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.playersNameContainer = QtWidgets.QWidget(self.playersContainer)
        self.playersNameContainer.setMinimumSize(QtCore.QSize(230, 45))
        self.playersNameContainer.setMaximumSize(QtCore.QSize(0, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setKerning(True)
        self.playersNameContainer.setFont(font)
        self.playersNameContainer.setStyleSheet("")
        self.playersNameContainer.setObjectName("playersNameContainer")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.playersNameContainer)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.PlayersNameHeader = QtWidgets.QLabel(self.playersNameContainer)
        self.PlayersNameHeader.setMinimumSize(QtCore.QSize(0, 45))
        self.PlayersNameHeader.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.PlayersNameHeader.setFont(font)
        self.PlayersNameHeader.setStyleSheet("background-color: hsl(223, 28, 43, 50%);")
        self.PlayersNameHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.PlayersNameHeader.setObjectName("PlayersNameHeader")
        self.verticalLayout_11.addWidget(self.PlayersNameHeader)
        self.playersName0 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName0.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName0.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName0.setFont(font)
        self.playersName0.setTextFormat(QtCore.Qt.AutoText)
        self.playersName0.setScaledContents(False)
        self.playersName0.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName0.setObjectName("playersName0")
        self.verticalLayout_11.addWidget(self.playersName0)
        self.playersName1 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName1.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName1.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName1.setFont(font)
        self.playersName1.setText("")
        self.playersName1.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName1.setObjectName("playersName1")
        self.verticalLayout_11.addWidget(self.playersName1)
        self.playersName2 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName2.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName2.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName2.setFont(font)
        self.playersName2.setText("")
        self.playersName2.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName2.setObjectName("playersName2")
        self.verticalLayout_11.addWidget(self.playersName2)
        self.playersName3 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName3.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName3.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName3.setFont(font)
        self.playersName3.setText("")
        self.playersName3.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName3.setObjectName("playersName3")
        self.verticalLayout_11.addWidget(self.playersName3)
        self.playersName4 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName4.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName4.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName4.setFont(font)
        self.playersName4.setText("")
        self.playersName4.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName4.setObjectName("playersName4")
        self.verticalLayout_11.addWidget(self.playersName4)
        self.playersName5 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName5.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName5.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName5.setFont(font)
        self.playersName5.setText("")
        self.playersName5.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName5.setObjectName("playersName5")
        self.verticalLayout_11.addWidget(self.playersName5)
        self.playersName6 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName6.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName6.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName6.setFont(font)
        self.playersName6.setText("")
        self.playersName6.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName6.setObjectName("playersName6")
        self.verticalLayout_11.addWidget(self.playersName6)
        self.playersName7 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName7.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName7.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName7.setFont(font)
        self.playersName7.setText("")
        self.playersName7.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName7.setObjectName("playersName7")
        self.verticalLayout_11.addWidget(self.playersName7)
        self.playersName8 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName8.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName8.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName8.setFont(font)
        self.playersName8.setText("")
        self.playersName8.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName8.setObjectName("playersName8")
        self.verticalLayout_11.addWidget(self.playersName8)
        self.horizontalLayout_4.addWidget(self.playersNameContainer)
        self.playersRankContainer = QtWidgets.QWidget(self.playersContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersRankContainer.sizePolicy().hasHeightForWidth())
        self.playersRankContainer.setSizePolicy(sizePolicy)
        self.playersRankContainer.setMinimumSize(QtCore.QSize(100, 0))
        self.playersRankContainer.setMaximumSize(QtCore.QSize(0, 16777215))
        self.playersRankContainer.setObjectName("playersRankContainer")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.playersRankContainer)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.playersRankHeader = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRankHeader.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRankHeader.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.playersRankHeader.setFont(font)
        self.playersRankHeader.setStyleSheet("background-color: hsl(223, 28, 43, 50%)")
        self.playersRankHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRankHeader.setObjectName("playersRankHeader")
        self.verticalLayout_9.addWidget(self.playersRankHeader)
        self.playersRank0 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank0.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank0.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank0.setFont(font)
        self.playersRank0.setStyleSheet("padding: 10px;")
        self.playersRank0.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.playersRank0.setText("")
        self.playersRank0.setTextFormat(QtCore.Qt.AutoText)
        self.playersRank0.setPixmap(QtGui.QPixmap(":/ranks/assets/Ranks/global.png"))
        self.playersRank0.setScaledContents(True)
        self.playersRank0.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank0.setWordWrap(False)
        self.playersRank0.setIndent(-1)
        self.playersRank0.setOpenExternalLinks(False)
        self.playersRank0.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.playersRank0.setObjectName("playersRank0")
        self.verticalLayout_9.addWidget(self.playersRank0)
        self.playersRank1 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank1.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank1.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank1.setFont(font)
        self.playersRank1.setText("")
        self.playersRank1.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank1.setObjectName("playersRank1")
        self.verticalLayout_9.addWidget(self.playersRank1)
        self.playersRank2 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank2.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank2.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank2.setFont(font)
        self.playersRank2.setText("")
        self.playersRank2.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank2.setObjectName("playersRank2")
        self.verticalLayout_9.addWidget(self.playersRank2)
        self.playersRank3 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank3.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank3.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank3.setFont(font)
        self.playersRank3.setText("")
        self.playersRank3.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank3.setObjectName("playersRank3")
        self.verticalLayout_9.addWidget(self.playersRank3)
        self.playersRank4 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank4.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank4.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank4.setFont(font)
        self.playersRank4.setText("")
        self.playersRank4.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank4.setObjectName("playersRank4")
        self.verticalLayout_9.addWidget(self.playersRank4)
        self.playersRank5 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank5.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank5.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank5.setFont(font)
        self.playersRank5.setText("")
        self.playersRank5.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank5.setObjectName("playersRank5")
        self.verticalLayout_9.addWidget(self.playersRank5)
        self.playersRank6 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank6.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank6.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank6.setFont(font)
        self.playersRank6.setText("")
        self.playersRank6.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank6.setObjectName("playersRank6")
        self.verticalLayout_9.addWidget(self.playersRank6)
        self.playersRank7 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank7.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank7.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank7.setFont(font)
        self.playersRank7.setText("")
        self.playersRank7.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank7.setObjectName("playersRank7")
        self.verticalLayout_9.addWidget(self.playersRank7)
        self.playersRank8 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank8.setMinimumSize(QtCore.QSize(0, 45))
        self.playersRank8.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersRank8.setFont(font)
        self.playersRank8.setText("")
        self.playersRank8.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank8.setObjectName("playersRank8")
        self.verticalLayout_9.addWidget(self.playersRank8)
        self.horizontalLayout_4.addWidget(self.playersRankContainer)
        self.playersWinsContainer = QtWidgets.QWidget(self.playersContainer)
        self.playersWinsContainer.setMinimumSize(QtCore.QSize(100, 0))
        self.playersWinsContainer.setMaximumSize(QtCore.QSize(100, 16777215))
        self.playersWinsContainer.setObjectName("playersWinsContainer")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.playersWinsContainer)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.playersWinsHeader = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWinsHeader.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWinsHeader.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.playersWinsHeader.setFont(font)
        self.playersWinsHeader.setStyleSheet("background-color: hsl(223, 28, 43, 50%)")
        self.playersWinsHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWinsHeader.setObjectName("playersWinsHeader")
        self.verticalLayout_12.addWidget(self.playersWinsHeader)
        self.playersWins0 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins0.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins0.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins0.setFont(font)
        self.playersWins0.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins0.setObjectName("playersWins0")
        self.verticalLayout_12.addWidget(self.playersWins0)
        self.playersWins1 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins1.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins1.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins1.setFont(font)
        self.playersWins1.setText("")
        self.playersWins1.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins1.setObjectName("playersWins1")
        self.verticalLayout_12.addWidget(self.playersWins1)
        self.playersWins2 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins2.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins2.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins2.setFont(font)
        self.playersWins2.setText("")
        self.playersWins2.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins2.setObjectName("playersWins2")
        self.verticalLayout_12.addWidget(self.playersWins2)
        self.playersWins3 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins3.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins3.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins3.setFont(font)
        self.playersWins3.setText("")
        self.playersWins3.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins3.setObjectName("playersWins3")
        self.verticalLayout_12.addWidget(self.playersWins3)
        self.playersWins4 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins4.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins4.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins4.setFont(font)
        self.playersWins4.setText("")
        self.playersWins4.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins4.setObjectName("playersWins4")
        self.verticalLayout_12.addWidget(self.playersWins4)
        self.playersWins5 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins5.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins5.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins5.setFont(font)
        self.playersWins5.setText("")
        self.playersWins5.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins5.setObjectName("playersWins5")
        self.verticalLayout_12.addWidget(self.playersWins5)
        self.playersWins6 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins6.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins6.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins6.setFont(font)
        self.playersWins6.setText("")
        self.playersWins6.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins6.setObjectName("playersWins6")
        self.verticalLayout_12.addWidget(self.playersWins6)
        self.playersWins7 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins7.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins7.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins7.setFont(font)
        self.playersWins7.setText("")
        self.playersWins7.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins7.setObjectName("playersWins7")
        self.verticalLayout_12.addWidget(self.playersWins7)
        self.playersWins8 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins8.setMinimumSize(QtCore.QSize(0, 45))
        self.playersWins8.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins8.setFont(font)
        self.playersWins8.setText("")
        self.playersWins8.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins8.setObjectName("playersWins8")
        self.verticalLayout_12.addWidget(self.playersWins8)
        self.horizontalLayout_4.addWidget(self.playersWinsContainer)
        self.playersFaceitContainer = QtWidgets.QWidget(self.playersContainer)
        self.playersFaceitContainer.setMinimumSize(QtCore.QSize(100, 0))
        self.playersFaceitContainer.setMaximumSize(QtCore.QSize(100, 16777215))
        self.playersFaceitContainer.setStyleSheet("QPushButton:hover {\n"
"    background-color: hsl(223, 11, 38, 50%);\n"
"}")
        self.playersFaceitContainer.setObjectName("playersFaceitContainer")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.playersFaceitContainer)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.playersFaceitHeader = QtWidgets.QLabel(self.playersFaceitContainer)
        self.playersFaceitHeader.setMinimumSize(QtCore.QSize(0, 45))
        self.playersFaceitHeader.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceitHeader.setFont(font)
        self.playersFaceitHeader.setStyleSheet("background-color: hsl(223, 28, 43, 50%)")
        self.playersFaceitHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.playersFaceitHeader.setObjectName("playersFaceitHeader")
        self.verticalLayout_14.addWidget(self.playersFaceitHeader)
        self.playersFaceit0 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit0.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit0.setFont(font)
        self.playersFaceit0.setStyleSheet("")
        self.playersFaceit0.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/assets/UI/faceit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playersFaceit0.setIcon(icon7)
        self.playersFaceit0.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit0.setCheckable(False)
        self.playersFaceit0.setObjectName("playersFaceit0")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.playersFaceit0)
        self.verticalLayout_14.addWidget(self.playersFaceit0)
        self.playersFaceit1 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit1.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit1.setFont(font)
        self.playersFaceit1.setText("")
        self.playersFaceit1.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit1.setObjectName("playersFaceit1")
        self.buttonGroup_2.addButton(self.playersFaceit1)
        self.verticalLayout_14.addWidget(self.playersFaceit1)
        self.playersFaceit2 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit2.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit2.setFont(font)
        self.playersFaceit2.setText("")
        self.playersFaceit2.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit2.setObjectName("playersFaceit2")
        self.buttonGroup_2.addButton(self.playersFaceit2)
        self.verticalLayout_14.addWidget(self.playersFaceit2)
        self.playersFaceit3 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit3.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit3.setFont(font)
        self.playersFaceit3.setText("")
        self.playersFaceit3.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit3.setObjectName("playersFaceit3")
        self.buttonGroup_2.addButton(self.playersFaceit3)
        self.verticalLayout_14.addWidget(self.playersFaceit3)
        self.playersFaceit4 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit4.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit4.setFont(font)
        self.playersFaceit4.setText("")
        self.playersFaceit4.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit4.setObjectName("playersFaceit4")
        self.buttonGroup_2.addButton(self.playersFaceit4)
        self.verticalLayout_14.addWidget(self.playersFaceit4)
        self.playersFaceit5 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit5.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit5.setFont(font)
        self.playersFaceit5.setText("")
        self.playersFaceit5.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit5.setObjectName("playersFaceit5")
        self.buttonGroup_2.addButton(self.playersFaceit5)
        self.verticalLayout_14.addWidget(self.playersFaceit5)
        self.playersFaceit6 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit6.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit6.setFont(font)
        self.playersFaceit6.setText("")
        self.playersFaceit6.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit6.setObjectName("playersFaceit6")
        self.buttonGroup_2.addButton(self.playersFaceit6)
        self.verticalLayout_14.addWidget(self.playersFaceit6)
        self.playersFaceit7 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit7.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit7.setFont(font)
        self.playersFaceit7.setText("")
        self.playersFaceit7.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit7.setObjectName("playersFaceit7")
        self.buttonGroup_2.addButton(self.playersFaceit7)
        self.verticalLayout_14.addWidget(self.playersFaceit7)
        self.playersFaceit8 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit8.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit8.setFont(font)
        self.playersFaceit8.setText("")
        self.playersFaceit8.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit8.setObjectName("playersFaceit8")
        self.buttonGroup_2.addButton(self.playersFaceit8)
        self.verticalLayout_14.addWidget(self.playersFaceit8)
        self.horizontalLayout_4.addWidget(self.playersFaceitContainer)
        self.playersCSGOStatsContainer = QtWidgets.QWidget(self.playersContainer)
        self.playersCSGOStatsContainer.setMinimumSize(QtCore.QSize(100, 45))
        self.playersCSGOStatsContainer.setMaximumSize(QtCore.QSize(100, 16777215))
        self.playersCSGOStatsContainer.setStyleSheet("QPushButton:hover {\n"
"    background-color: hsl(223, 11, 38, 50%);\n"
"}")
        self.playersCSGOStatsContainer.setObjectName("playersCSGOStatsContainer")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.playersCSGOStatsContainer)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.CSGOStatsHeader = QtWidgets.QLabel(self.playersCSGOStatsContainer)
        self.CSGOStatsHeader.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsHeader.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.CSGOStatsHeader.setFont(font)
        self.CSGOStatsHeader.setStyleSheet("QLabel{\n"
"    background-color: hsl(223, 28, 43, 50%);\n"
"}")
        self.CSGOStatsHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.CSGOStatsHeader.setObjectName("CSGOStatsHeader")
        self.verticalLayout_15.addWidget(self.CSGOStatsHeader)
        self.CSGOStatsBtn = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn.setFont(font)
        self.CSGOStatsBtn.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/assets/UI/csgoPlayer_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CSGOStatsBtn.setIcon(icon8)
        self.CSGOStatsBtn.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn.setCheckable(False)
        self.CSGOStatsBtn.setObjectName("CSGOStatsBtn")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.CSGOStatsBtn)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn)
        self.CSGOStatsBtn_2 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_2.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_2.setFont(font)
        self.CSGOStatsBtn_2.setText("")
        self.CSGOStatsBtn_2.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_2.setObjectName("CSGOStatsBtn_2")
        self.buttonGroup.addButton(self.CSGOStatsBtn_2)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_2)
        self.CSGOStatsBtn_3 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_3.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_3.setFont(font)
        self.CSGOStatsBtn_3.setText("")
        self.CSGOStatsBtn_3.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_3.setObjectName("CSGOStatsBtn_3")
        self.buttonGroup.addButton(self.CSGOStatsBtn_3)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_3)
        self.CSGOStatsBtn_4 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_4.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_4.setFont(font)
        self.CSGOStatsBtn_4.setText("")
        self.CSGOStatsBtn_4.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_4.setObjectName("CSGOStatsBtn_4")
        self.buttonGroup.addButton(self.CSGOStatsBtn_4)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_4)
        self.CSGOStatsBtn_5 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_5.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_5.setFont(font)
        self.CSGOStatsBtn_5.setText("")
        self.CSGOStatsBtn_5.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_5.setObjectName("CSGOStatsBtn_5")
        self.buttonGroup.addButton(self.CSGOStatsBtn_5)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_5)
        self.CSGOStatsBtn_6 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_6.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_6.setFont(font)
        self.CSGOStatsBtn_6.setText("")
        self.CSGOStatsBtn_6.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_6.setObjectName("CSGOStatsBtn_6")
        self.buttonGroup.addButton(self.CSGOStatsBtn_6)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_6)
        self.CSGOStatsBtn_7 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_7.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_7.setFont(font)
        self.CSGOStatsBtn_7.setText("")
        self.CSGOStatsBtn_7.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_7.setObjectName("CSGOStatsBtn_7")
        self.buttonGroup.addButton(self.CSGOStatsBtn_7)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_7)
        self.CSGOStatsBtn_8 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_8.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_8.setFont(font)
        self.CSGOStatsBtn_8.setText("")
        self.CSGOStatsBtn_8.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_8.setObjectName("CSGOStatsBtn_8")
        self.buttonGroup.addButton(self.CSGOStatsBtn_8)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_8)
        self.CSGOStatsBtn_9 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn_9.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn_9.setFont(font)
        self.CSGOStatsBtn_9.setText("")
        self.CSGOStatsBtn_9.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn_9.setObjectName("CSGOStatsBtn_9")
        self.buttonGroup.addButton(self.CSGOStatsBtn_9)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn_9)
        self.horizontalLayout_4.addWidget(self.playersCSGOStatsContainer)
        self.verticalLayout_8.addWidget(self.playersContainer, 0, QtCore.Qt.AlignHCenter)
        self.mainBodyWidget.addWidget(self.playersPage)
        self.settingsPage = QtWidgets.QWidget()
        self.settingsPage.setStyleSheet("background-color: rgb(29, 32, 40);\n"
"")
        self.settingsPage.setObjectName("settingsPage")
        self.gridLayout = QtWidgets.QGridLayout(self.settingsPage)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.settingsPage)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.widget_4 = QtWidgets.QWidget(self.settingsPage)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout.addWidget(self.widget_4, 1, 0, 1, 1)
        self.widget_6 = QtWidgets.QWidget(self.settingsPage)
        self.widget_6.setStyleSheet("")
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.widget_3 = QtWidgets.QWidget(self.widget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.widget_3.setFont(font)
        self.widget_3.setStyleSheet("border-bottom: 2px solid #212D4B;\n"
"padding: 0 0 5px 0;")
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.label = QtWidgets.QLabel(self.widget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout_18.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_17.addWidget(self.widget_3)
        self.widget_7 = QtWidgets.QWidget(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setMinimumSize(QtCore.QSize(0, 200))
        self.widget_7.setStyleSheet("")
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_8.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.widget_8left = QtWidgets.QWidget(self.widget_7)
        self.widget_8left.setObjectName("widget_8left")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.widget_8left)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_2 = QtWidgets.QLabel(self.widget_8left)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_19.addWidget(self.label_2)
        self.horizontalLayout_8.addWidget(self.widget_8left)
        self.widget_8right = QtWidgets.QWidget(self.widget_7)
        self.widget_8right.setObjectName("widget_8right")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.widget_8right)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.horizontalSlider = QtWidgets.QSlider(self.widget_8right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_20.addWidget(self.horizontalSlider)
        self.horizontalLayout_8.addWidget(self.widget_8right)
        self.verticalLayout_17.addWidget(self.widget_7, 0, QtCore.Qt.AlignTop)
        self.gridLayout.addWidget(self.widget_6, 0, 1, 1, 1)
        self.widget_5 = QtWidgets.QWidget(self.settingsPage)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout.addWidget(self.widget_5, 1, 1, 1, 1)
        self.mainBodyWidget.addWidget(self.settingsPage)
        self.wallhackPage = QtWidgets.QWidget()
        self.wallhackPage.setStyleSheet("background-color: rgb(75,75, 75);")
        self.wallhackPage.setObjectName("wallhackPage")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.wallhackPage)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.wallhackPage)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.checkBox = QtWidgets.QCheckBox(self.widget_2)
        self.checkBox.setChecked(False)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_13.addWidget(self.checkBox)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.mainBodyWidget.addWidget(self.wallhackPage)
        self.verticalLayout_7.addWidget(self.mainBodyWidget)
        self.verticalLayout_6.addWidget(self.mainBodyContent)
        self.horizontalLayout.addWidget(self.mainBodyContainer)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.mainBodyWidget.setCurrentIndex(0)
         
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def display_players(self): #Update players button -- make a check if the rank is not 0 then display players        
        getPlayerInfo()
        _translate = QtCore.QCoreApplication.translate
        
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/assets/UI/faceit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/assets/UI/csgoPlayer_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                
        steamidsFounds = 0
        for steamids in playersInfoAddr: #Check that the button is not clicked when nothing is there otherwise - crash
            if steamids[5] > 1:
                steamidsFounds = 1
        
        
        if steamidsFounds == 1:
        
        # if len(playersInfoAddr) == 9:
            
        # for eee in playersInfoAddr: #Display players by team -- future update
        #     if eee[2] == 2:
        
            self.playersName0.setText(_translate("MainWindow", str(playersInfoAddr[0][1])))
            self.playersName1.setText(_translate("MainWindow", str(playersInfoAddr[1][1])))
            self.playersName2.setText(_translate("MainWindow", str(playersInfoAddr[2][1])))
            self.playersName3.setText(_translate("MainWindow", str(playersInfoAddr[3][1])))
            self.playersName4.setText(_translate("MainWindow", str(playersInfoAddr[4][1])))
            self.playersName5.setText(_translate("MainWindow", str(playersInfoAddr[5][1])))
            self.playersName6.setText(_translate("MainWindow", str(playersInfoAddr[6][1])))
            self.playersName7.setText(_translate("MainWindow", str(playersInfoAddr[7][1])))
            self.playersName8.setText(_translate("MainWindow", str(playersInfoAddr[8][1])))
            
            self.playersRank0.setText(_translate("MainWindow", str(playersInfoAddr[0][3])))
            self.playersRank1.setText(_translate("MainWindow", str(playersInfoAddr[1][3])))
            self.playersRank2.setText(_translate("MainWindow", str(playersInfoAddr[2][3])))
            self.playersRank3.setText(_translate("MainWindow", str(playersInfoAddr[3][3])))
            self.playersRank4.setText(_translate("MainWindow", str(playersInfoAddr[4][3])))
            self.playersRank5.setText(_translate("MainWindow", str(playersInfoAddr[5][3])))
            self.playersRank6.setText(_translate("MainWindow", str(playersInfoAddr[6][3])))
            self.playersRank7.setText(_translate("MainWindow", str(playersInfoAddr[7][3])))
            self.playersRank8.setText(_translate("MainWindow", str(playersInfoAddr[8][3])))
            
            self.playersWins0.setText(_translate("MainWindow", str(playersInfoAddr[0][4])))
            self.playersWins1.setText(_translate("MainWindow", str(playersInfoAddr[1][4])))
            self.playersWins2.setText(_translate("MainWindow", str(playersInfoAddr[2][4])))
            self.playersWins3.setText(_translate("MainWindow", str(playersInfoAddr[3][4])))
            self.playersWins4.setText(_translate("MainWindow", str(playersInfoAddr[4][4])))
            self.playersWins5.setText(_translate("MainWindow", str(playersInfoAddr[5][4])))
            self.playersWins6.setText(_translate("MainWindow", str(playersInfoAddr[6][4])))
            self.playersWins7.setText(_translate("MainWindow", str(playersInfoAddr[7][4])))
            self.playersWins8.setText(_translate("MainWindow", str(playersInfoAddr[8][4])))
            
            self.playersFaceit0.setIcon(icon7)
            self.playersFaceit1.setIcon(icon7)
            self.playersFaceit2.setIcon(icon7)
            self.playersFaceit3.setIcon(icon7)
            self.playersFaceit4.setIcon(icon7)
            self.playersFaceit5.setIcon(icon7)
            self.playersFaceit6.setIcon(icon7)
            self.playersFaceit7.setIcon(icon7)
            self.playersFaceit8.setIcon(icon7)        
            
            self.CSGOStatsBtn.setIcon(icon8)
            self.CSGOStatsBtn_2.setIcon(icon8)
            self.CSGOStatsBtn_3.setIcon(icon8)
            self.CSGOStatsBtn_4.setIcon(icon8)
            self.CSGOStatsBtn_5.setIcon(icon8)
            self.CSGOStatsBtn_6.setIcon(icon8)
            self.CSGOStatsBtn_7.setIcon(icon8)
            self.CSGOStatsBtn_8.setIcon(icon8)
            self.CSGOStatsBtn_9.setIcon(icon8)
        
        # elif len(playersInfoAddr) == 3:
        #     self.playersName0.setText(_translate("MainWindow", str(playersInfoAddr[0][1])))
        #     self.playersName1.setText(_translate("MainWindow", str(playersInfoAddr[1][1])))
        #     self.playersName2.setText(_translate("MainWindow", str(playersInfoAddr[2][1])))
            
        #     self.playersRank0.setText(_translate("MainWindow", str(playersInfoAddr[0][3])))
        #     self.playersRank1.setText(_translate("MainWindow", str(playersInfoAddr[1][3])))
        #     self.playersRank2.setText(_translate("MainWindow", str(playersInfoAddr[2][3])))
            
        #     self.playersWins0.setText(_translate("MainWindow", str(playersInfoAddr[0][4])))
        #     self.playersWins1.setText(_translate("MainWindow", str(playersInfoAddr[1][4])))
        #     self.playersWins2.setText(_translate("MainWindow", str(playersInfoAddr[2][4])))
            
        #     self.playersFaceit0.setIcon(icon7)
        #     self.playersFaceit1.setIcon(icon7)
        #     self.playersFaceit2.setIcon(icon7)    
            
        #     self.CSGOStatsBtn.setIcon(icon8)
        #     self.CSGOStatsBtn_2.setIcon(icon8)
        #     self.CSGOStatsBtn_3.setIcon(icon8)
            
        # else:
        #     self.playersRefreshMsg.setText('ERROR: Players not found')
    
    def openFaceit(self, btn):
        steamidsFounds = 0
        for steamids in playersInfoAddr: #Check that the button is not clicked when nothing is there otherwise - crash
            if steamids[5] > 1:
                steamidsFounds = 1
        
        if steamidsFounds == 1:
            if btn == -2: # btn0
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[0][5]))
            if btn == -3:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[1][5]))
            if btn == -4:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[2][5]))
            if btn == -5:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[3][5]))
            if btn == -6:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[4][5]))
            if btn == -7:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[5][5]))
            if btn == -8:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[6][5]))
            if btn == -9:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[7][5]))
            if btn == -10:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfoAddr[8][5]))
            
    def openCSGOStats(self, btn):
        steamidsFounds = 0
        for steamids in playersInfoAddr: #Check that the button is not clicked when nothing is there otherwise - crash
            if steamids[5] > 1:
                steamidsFounds = 1
        
        if steamidsFounds == 1:
            if btn == -2: # btn0
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[0][5]))
            if btn == -3:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[1][5]))
            if btn == -4:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[2][5]))
            if btn == -5:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[3][5]))
            if btn == -6:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[4][5]))
            if btn == -7:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[5][5]))
            if btn == -8:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[6][5]))
            if btn == -9:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[7][5]))
            if btn == -10:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfoAddr[8][5]))
            
    
    def btnState(self):
        _translate = QtCore.QCoreApplication.translate
        if self.checkBox.isChecked():
            print('hello')
            featureState.wallhackNameActive = 1
        else:
            featureState.wallhackNameActive = 0

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.wallhackBtn.setToolTip(_translate("MainWindow", "Analysis"))
        self.playersBtn.setToolTip(_translate("MainWindow", "Reports"))
        self.settingsBtn.setToolTip(_translate("MainWindow", "Settings"))
        self.playersRefreshMsg.setText(_translate("MainWindow", "asd"))
        self.PlayersNameHeader.setText(_translate("MainWindow", "NAME"))
        self.playersName0.setText(_translate("MainWindow", "asdasdasd"))
        self.playersRankHeader.setText(_translate("MainWindow", "RANK"))
        self.playersWinsHeader.setText(_translate("MainWindow", "WINS"))
        self.playersWins0.setText(_translate("MainWindow", "32"))
        self.playersFaceitHeader.setText(_translate("MainWindow", "FACEIT"))
        self.CSGOStatsHeader.setText(_translate("MainWindow", "CSGOSTATS"))
        self.label.setText(_translate("MainWindow", "Overlay"))
        self.label_2.setText(_translate("MainWindow", "Performance"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        
        self.wallhackBtn.clicked.connect(lambda: self.mainBodyWidget.setCurrentIndex(2))
        self.playersBtn.clicked.connect(lambda: self.mainBodyWidget.setCurrentIndex(0))
        self.settingsBtn.clicked.connect(lambda: self.mainBodyWidget.setCurrentIndex(1))
        
        self.buttonGroup_2.buttonClicked[int].connect(self.openFaceit) # adding [int] to get the button ID from a group
        self.buttonGroup.buttonClicked[int].connect(self.openCSGOStats)
        
        self.playersRefreshBtn.clicked.connect(self.display_players)
        
        self.checkBox.clicked.connect(self.btnState)
import res   


def main():
    threading.Thread(target=processInfo.checkGameFocus, name='checkGameFocus', daemon=True).start()
    # threading.Thread(target=getBombInfo, name='getBombInfo', daemon=True).start()
    threading.Thread(target=triggerbot, name='Trigger.triggerbot', daemon=True).start()
    newOverlay() #start after all processes
    
if __name__ == "__main__":    
    pm.overlay_init(fps=145, title='test')
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    main()
    
    sys.exit(app.exec_())
    