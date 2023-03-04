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

from tools.config import *
from tools.triggerbot import *
from tools.bombinfo import *
from tools.playersinfo import *

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
        return pm.r_int16(self.mem, getWeaponAddressHandle + Offset.m_iItemDefinitionIndex)

# bombIndexAddr = []
_scoping_rifles = [9, 40, 38, 11]

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
            #     localPlayerWeapon = localPlayer.getWeapon(csgo_client)
            #     if localPlayerWeapon in _scoping_rifles:
            #         if not localPlayer.is_scoped:
            #             pm.draw_circle(
            #                 centerX = screen_center_x,
            #                 centerY = screen_center_y,
            #                 radius = 3,
            #                 color = Colors.red,
            #             )
            #     else:
            #         pass
            
            spectatorsArr = []
            for ents in entAddr:
                if ents > 0:
                    try:
                        entity = Entity(ents, csgo_proc, csgo_client)
                        
                        # if ents != localPlayerAddr:
                        #     print(entity.getWeapon(csgo_client))
                        
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
        pm.end_drawing()

def main():
    threading.Thread(target=processInfo.checkGameFocus, name='checkGameFocus', daemon=True).start()
    threading.Thread(target=getBombInfo, name='getBombInfo', daemon=True).start()
    threading.Thread(target=getPlayerInfo, name='getPlayerInfo', daemon=True).start()
    threading.Thread(target=triggerbot, name='Trigger.triggerbot', daemon=True).start()
    newOverlay() #start after all processes
    
if __name__ == "__main__":    
    pm.overlay_init(fps=1000, title='test')
    main()