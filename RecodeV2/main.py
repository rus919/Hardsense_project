import os, struct
from dataclasses import dataclass
import ctypes as ctypes
from pymem import Pymem, process, exception, pattern
import threading
from requests import get

import pyMeow as meow

import mouse
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser

class Offsets:
    pass

class Colors:
    orange = meow.get_color("orange")
    black = meow.get_color("black")
    purple = meow.get_color("purple")
    white = meow.get_color("white")
    cyan = meow.get_color("cyan")
    red = meow.get_color("red")
    green = meow.get_color("green")
    pink = meow.get_color("pink")
    crosshair = meow.new_color(255, 0, 255, 255)
    recoil = meow.new_color(0, 0, 255, 155)
    
class LocalPlayer():
    def __init__(self, address):
        self.address = address
    
    @staticmethod
    def get_local_player():
        return csgo.read_uint(csgo_client + Offsets.dwLocalPlayer)
    
    @staticmethod
    def get_crosshair_id():
        return csgo.read_uint(LocalPlayer.get_local_player() + Offsets.m_iCrosshairId)

class Entity():
    def __init__(self, address):
        self.address = address
    
    def get_id(self):
        return csgo.read_int(self.address + 0x64)
    
    def get_team(self):
        return csgo.read_int(self.address + Offsets.m_iTeamNum)
    
    def get_health(self):
        return csgo.read_int(self.address + Offsets.m_iHealth)
    
    def get_armour(self):
        return csgo.read_int(self.address + Offsets.m_ArmorValue)

    def get_dormant(self):
        return csgo.read_int(self.address + Offsets.m_bDormant)
    
    def get_life_state(self):
        return csgo.read_int(self.address + Offsets.m_lifeState)
    
    def is_scoped(self):
        return csgo.read_bool(self.address + Offsets.m_bIsScoped)
    
    def get_vec_punch(self):
        vec_punch_x = csgo.read_float(self.address + Offsets.m_aimPunchAngle)
        vec_punch_y = csgo.read_float(self.address + Offsets.m_aimPunchAngle + 4)
        vec_punch_z = csgo.read_float(self.address + Offsets.m_aimPunchAngle + 8)
        return meow.vec3(vec_punch_x, vec_punch_y, vec_punch_z)
    
    def get_shots_fired(self):
        return csgo.read_int(self.address + Offsets.m_iShotsFired)

    def get_position(self):
        localpos_x = csgo.read_float(self.address + Offsets.m_vecOrigin)
        localpos_y = csgo.read_float(self.address + Offsets.m_vecOrigin + 4)
        localpos_z = csgo.read_float(self.address + Offsets.m_vecOrigin + 8)
        return meow.vec3(localpos_x, localpos_y, localpos_z)

    def get_bone_position(self, bone_id: int):
        bone_matrix = csgo.read_uint(self.address + Offsets.m_dwBoneMatrix)
        return meow.vec3(csgo.read_float(bone_matrix + 0x30 * bone_id + 0x0c),
                       csgo.read_float(bone_matrix + 0x30 * bone_id + 0x1c),
                       csgo.read_float(bone_matrix + 0x30 * bone_id + 0x2c)
        )
  
    def getWeapon(self):
        getWeaponAddress = csgo.read_uint(self.address + Offsets.m_hActiveWeapon) & 0xFFF
        getWeaponAddressHandle = csgo.read_uint(csgo_client + Offsets.dwEntityList + (getWeaponAddress - 1) * 0x10)
        return csgo.read_short(getWeaponAddressHandle + Offsets.m_iItemDefinitionIndex)
    
    def get_player_steam_id(index):
        player_info = csgo.read_uint(Engine.get_state() + Offsets.dwClientState_PlayerInfo)
        player_items = csgo.read_uint(csgo.read_uint(player_info + 0x40) + 0xC)
        info = csgo.read_uint(player_items + 0x28 + (index * 0x34))
        if info != 0:
            return csgo.read_string(info + 0x94) # 0x94 = steamid32, char 0x10 == name, 
        
    @property
    def get_name(self):
        radar_base = csgo.read_uint(csgo_client + Offsets.dwRadarBase)
        hud_radar = csgo.read_uint(radar_base + 0x78)
        return csgo.read_string(hud_radar + 0x300 + (0x174 * (self.get_id() - 1)), 32)
    
    def get_observed_target_handle(self):
        return csgo.read_int(self.address + Offsets.m_hObserverTarget) & 0xFFF

class Engine():
    @staticmethod
    def get_entity(index):
        return csgo.read_uint(csgo_client + Offsets.dwEntityList + index * 0x10)

    @staticmethod
    def get_view_matrix():
        view = csgo.read_bytes(csgo_client + Offsets.dwViewMatrix, 64)
        matrix = struct.unpack("16f", view)
        return matrix

    @staticmethod
    def get_state():
        return csgo.read_uint(csgo_engine + Offsets.dwClientState)
    
    @staticmethod
    def get_client_state():
        return csgo.read_uint(Engine.get_state() + Offsets.dwClientState_State)
    
    @staticmethod
    def get_client_view_angles():
        view_angle_bytes = csgo.read_bytes(Engine.get_state() + Offsets.dwClientState_ViewAngles, 0xC)
        var = struct.unpack("3f", view_angle_bytes)
        return meow.vec3(*var)
        
    
    @staticmethod
    def get_GameRulesProxy():
        return csgo.read_uint(csgo_client + Offsets.dwGameRulesProxy)
    
    @staticmethod
    def get_bomb_planted():
        return csgo.read_uint(Engine.get_GameRulesProxy() + Offsets.m_bBombPlanted)
    
    @staticmethod
    def get_bomb_ticking(bomb_entity):
        return csgo.read_bool(bomb_entity + Offsets.m_bBombTicking)
    
    @staticmethod
    def get_bomb_site(bomb_entity):
        return csgo.read_short(bomb_entity + Offsets.m_nBombSite)
    
    @staticmethod
    def get_bomb_time(bomb_entity):
        return csgo.read_float(bomb_entity + Offsets.m_flC4Blow) - Engine.get_curr_time() #To start countdown 
    
    @staticmethod
    def get_defuse_time(bomb_entity):
        return csgo.read_float(bomb_entity + Offsets.m_flDefuseCountDown) - Engine.get_curr_time() #To start countdown 
    
    def is_defusing_bomb(bomb_entity):
        return csgo.read_int(bomb_entity + Offsets.m_hBombDefuser)
    
    @staticmethod
    def get_curr_time():
        return csgo.read_float(csgo_engine + Offsets.dwGlobalVars + 0x10)

def GetWindowText(handle, length=100):
        window_text = ctypes.create_string_buffer(length)
        u32.GetWindowTextA(
            handle,
            ctypes.byref(window_text),
            length
        )
        return window_text.value

EntityList = []
bombAddr = []
playersInfo = []
def entity_parse():
    while True:
        if Engine.get_client_state() == 6:
            try:
                EntityList.clear()
                
                for i in range(1, 512):                    
                    entity = csgo.read_uint(csgo_client + Offsets.dwEntityList + i * 0x10)
                    if entity != 0:
                        ents = Entity(entity)
                        client_networkable = csgo.read_uint(entity + 0x8)
                        dwGetClientClassFn = csgo.read_uint(client_networkable + 0x8)
                        entity_client_class = csgo.read_uint(dwGetClientClassFn+ 0x1)
                        class_id = csgo.read_uint(entity_client_class + 0x14)

                        if class_id == 40:
                            if not EntityList.__contains__(entity):
                                EntityList.append(entity)
                                
                        if Engine.get_bomb_planted() == 1:
                            if class_id == 129:
                                if not bombAddr.__contains__(entity):
                                    bombAddr.append(entity) 
                        else:
                            bombAddr.clear()
                                            
            except Exception as err:
                print('entity_parse: ', err)
                pass
        else:
            k32.Sleep(2000)
            continue
        
        k32.Sleep(1000)

def getPlayerInfo(): # Not returning properly, missing player data when in entity he is there
    if Engine.get_client_state() == 6:
        try:
            playersInfo.clear()
            for i in range(1, 64):     
                entity = Engine.get_entity(i)
                player_resources = csgo.read_int(csgo_client + Offsets.dwPlayerResource)
                if entity != 0:
                    playerSteamID = Entity.get_player_steam_id(i) # Getting steamID32
                    id_split = playerSteamID.split(":") #Convert steamID32 to array
                    steam64id = 76561197960265728 #Base for adding
                    steam64id += int(id_split[2]) * 2 #Take the player ID in [2] and *2 then add to steam64id, if steamID32 [1] contains 1 then add +1 = steamID64
                    if id_split[1] == "1":
                        steam64id += 1
                    
                    ents = Entity(entity)
                                        
                    entityCompRank = csgo.read_int(player_resources + Offsets.m_iCompetitiveRanking + (i+1) * 4)
                    entityCompWins = csgo.read_int(player_resources + Offsets.m_iCompetitiveWins + (i+1) * 4)
                    
                    if [i, ents.get_name, ents.get_team(), entityCompRank, entityCompWins, steam64id] not in playersInfo:
                        playersInfo.append([i, ents.get_name, ents.get_team(), entityCompRank, entityCompWins, steam64id])
            print(playersInfo)
        except Exception as err:
            print('PLAYERS INFO ERROR: ', err)
            pass

def trigger():
    while True:
        if Engine.get_client_state() == 6 and GetWindowText( u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
            if u32.GetAsyncKeyState(6):
                Local_player = Entity(LocalPlayer.get_local_player())            
                entity_id = LocalPlayer.get_crosshair_id()
                if entity_id != 0 and entity_id < 64:
                    entity = Entity(Engine.get_entity(entity_id - 1))
                    if Local_player.get_team() != entity.get_team() and entity.get_health() > 0:
                        # k32.Sleep(1)
                        mouse.click()
                        k32.Sleep(200)
        k32.Sleep(1)

def rcs_control():
    g_old_punch = 0
    while True:
        if Engine.get_client_state() == 6:
            try:
                Local_player = Entity(LocalPlayer.get_local_player())
                current_punch = Local_player.get_vec_punch()
                view_angle = Engine.get_client_view_angles()
                if Local_player.get_shots_fired() > 1:
                    new_punch = meow.vec3(current_punch['x'] - g_old_punch['x'], current_punch['y'] - g_old_punch['y'], 0)
                    new_angle = meow.vec3(view_angle['x'] - new_punch['x'] * 2.0, view_angle['y'] - new_punch['y'] * 2.0, 0)
                    u32.mouse_event(0x0001,
                                    int(((new_angle['y'] - view_angle['y']) / 1.0) / -0.022),
                                    int(((new_angle['x'] - view_angle['x']) / 1.0) / 0.022),
                                    0, 0)
                g_old_punch = current_punch
            except Exception as err:
                print(err)
                continue
    
def esp():
    # weapon_id_list = [1, 2, 3, 4, 7, 8, 9, 10, 11, 13, 14, 16, 17, 19, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 
    #            41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 60, 61, 63, 64, 500, 503, 505, 506, 507, 508, 509, 512, 514, 
    #            515, 516, 517, 518, 519, 520, 521, 522, 523, 525]
    knife_weapons = [42, 59, 500, 503, 505, 506, 507, 508, 509, 512, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 525]
    scoped_weapons = [9, 11, 38, 40]
    try:
        meow.load_font("assets/fonts/ff.ttf", 0)
        crosshair = meow.load_texture("assets/images/crosshair.png")
        Desert_Eagle = meow.load_texture("assets/images/desert_eagle.png")
        Dual_Berettas = meow.load_texture("assets/images/elite.png")
        Five_SeveN = meow.load_texture("assets/images/fiveseven.png")
        p2000 = meow.load_texture("assets/images/p2000.png")
        Glock_18 = meow.load_texture("assets/images/glock.png")
        AK_47 = meow.load_texture("assets/images/ak47.png")
        AUG = meow.load_texture("assets/images/aug.png")
        AWP = meow.load_texture("assets/images/awp.png")
        FAMAS = meow.load_texture("assets/images/famas.png")
        G3SG1 = meow.load_texture("assets/images/g3sg1.png")
        Galil_AR = meow.load_texture("assets/images/galil.png")
        M249 = meow.load_texture("assets/images/m249.png")
        M4A4 = meow.load_texture("assets/images/m4a4.png")
        MAC_10 = meow.load_texture("assets/images/mac10.png")
        P90 = meow.load_texture("assets/images/p90.png")
        MP5_SD = meow.load_texture("assets/images/mp5.png")
        UMP_45 = meow.load_texture("assets/images/ump.png")
        XM1014 = meow.load_texture("assets/images/xm1014.png")
        Bizon = meow.load_texture("assets/images/bizon.png")
        MAG_7 = meow.load_texture("assets/images/mag7.png")
        Negev = meow.load_texture("assets/images/negev.png")
        Sawed_Off = meow.load_texture("assets/images/sawedoff.png")
        Tec_9 = meow.load_texture("assets/images/tec9.png")
        Zeus = meow.load_texture("assets/images/zeus_x27.png")
        MP7 = meow.load_texture("assets/images/mp7.png")
        MP9 = meow.load_texture("assets/images/mp9.png")
        Nova = meow.load_texture("assets/images/nova.png")
        P250 = meow.load_texture("assets/images/p250.png")
        SCAR_20 = meow.load_texture("assets/images/scar20.png")
        SG_553 = meow.load_texture("assets/images/sg553.png")
        SSG_08 = meow.load_texture("assets/images/ssg08.png")
        M4A1_S = meow.load_texture("assets/images/m4a1_silencer.png")
        USP_S = meow.load_texture("assets/images/usp_silencer.png")
        CZ75_Auto = meow.load_texture("assets/images/cz75a.png")
        R8_Revolver = meow.load_texture("assets/images/r8_revolver.png")	
        Knife = meow.load_texture("assets/images/knife.png")
        Flashbang = meow.load_texture("assets/images/flash_grenade.png")
        Explosive_Grenade = meow.load_texture("assets/images/explosive_grenade.png")
        Smoke_Grenade = meow.load_texture("assets/images/smoke_grenade.png")
        Molotov = meow.load_texture("assets/images/molotov.png")
        Decoy_Grenade = meow.load_texture("assets/images/decoy_grenade.png")
        Incendiary_Grenade = meow.load_texture("assets/images/incendiary_grenade.png")
        C4 = meow.load_texture("assets/images/c4.png")
    except Exception as err:
        print('Assets loading error:', err)
        pass	
 
 
    while meow.overlay_loop():
        
        meow.begin_drawing()
        
        get_screen_width_x = meow.get_screen_width()
        get_screen_width_y = meow.get_screen_height()
        
        get_screen_center_x =meow.get_screen_width() // 2
        get_screen_center_y = meow.get_screen_height() // 2
        
        if GetWindowText( u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
            meow.draw_text(text = "HARDSENSE", posX = 5, posY = 5, fontSize = 10, color = meow.get_color("red"))
            meow.draw_fps(50, 50)
            if Engine.get_client_state() == 6:
                try:
                    Local_player = Entity(LocalPlayer.get_local_player())
                    view_matrix = Engine.get_view_matrix()
                    server_time = Engine.get_curr_time()
                except Exception as err:
                    print('001 INIT ERROR:', err)
                
                if LocalPlayer.get_local_player() != 0:
                    if Local_player.get_health() > 0:
                        try:
                            local_player_weapon = Local_player.getWeapon()
                            for holding_scoped_weapons in scoped_weapons:
                                if local_player_weapon == holding_scoped_weapons:
                                    if not Local_player.is_scoped():
                                        
                                        meow.draw_line(
                                            startPosX =get_screen_center_x - 5, 
                                            startPosY =get_screen_center_y, 
                                            endPosX =get_screen_center_x + 5, 
                                            endPosY =get_screen_center_y, 
                                            color = Colors.crosshair, 
                                            thick = 1.0
                                        )
                                        meow.draw_line(
                                            startPosX =get_screen_center_x, 
                                            startPosY =get_screen_center_y - 5, 
                                            endPosX =get_screen_center_x, 
                                            endPosY =get_screen_center_y + 5, 
                                            color = Colors.crosshair, 
                                            thick = 1.0
                                        )
                                else:
                                    continue
                        except Exception as err:
                            print('AWP CROSSHAIR ERROR:',err)
                            continue
                
                    if Local_player.get_vec_punch()['x'] != 0.0:
                        player_fov_x = meow.get_screen_width() // 90
                        player_fov_y = meow.get_screen_height() // 90
                        crosshair_x = get_screen_center_x - player_fov_x * Local_player.get_vec_punch()["y"]
                        crosshair_y = get_screen_center_y - player_fov_y * -Local_player.get_vec_punch()["x"]
                        if Local_player.get_shots_fired() > 1:
                            meow.draw_line(
                                startPosX =crosshair_x - 5, 
                                startPosY =crosshair_y, 
                                endPosX =crosshair_x + 5, 
                                endPosY =crosshair_y, 
                                color = Colors.recoil, 
                                thick = 1.0
                            )
                            meow.draw_line(
                                startPosX =crosshair_x, 
                                startPosY =crosshair_y - 5, 
                                endPosX =crosshair_x, 
                                endPosY =crosshair_y + 5, 
                                color = Colors.recoil, 
                                thick = 1.0
                            )

                for bomb_index in bombAddr:
                    try:
                        bomb_entity = Entity(bomb_index)
                        bomb_pos = bomb_entity.get_position()
                        bomb_w2s_pos = meow.world_to_screen(view_matrix, bomb_pos, 1)
                        bomb_time = Engine.get_bomb_time(bomb_index)
                        defuse_time = Engine.get_defuse_time(bomb_index)
                                                
                        bomb_site = ''
                        
                        if Engine.get_bomb_site(bomb_index) == 0: bomb_site = 'BOMB: A'
                        if Engine.get_bomb_site(bomb_index) == 1: bomb_site = 'BOMB: B'
                        if defuse_time > bomb_time:
                            defuse_color = Colors.red
                        else:
                            defuse_color = Colors.green
                        
                        if Engine.get_bomb_ticking(bomb_index) and bomb_time > 0:
                            
                            meow.draw_text(
                                text= str(bomb_site),
                                posX=get_screen_width_x / 100,
                                posY=get_screen_width_y / 1.5 ,
                                fontSize=25,
                                color=Colors.cyan,
                            )
                            
                            meow.draw_text(
                                text= f"{bomb_time:.3}",
                                posX=get_screen_width_x / 100,
                                posY=(get_screen_width_y / 1.5) * 1.05,
                                fontSize=25,
                                color=Colors.orange,
                            )
                            
                            if Engine.is_defusing_bomb(bomb_index) > 0:
                                meow.draw_text(
                                    text= f"{defuse_time:.3}",
                                    posX=get_screen_width_x / 100,
                                    posY=(get_screen_width_y / 1.5) * 1.10,
                                    fontSize=25,
                                    color=defuse_color,
                                )

                        
                        meow.draw_texture(texture = C4, posX = bomb_w2s_pos["x"], posY = bomb_w2s_pos["y"], rotation = 0, scale = 0.6,tint = Colors.white)
                        
                        
                        
                    except Exception as err:
                        # print('BOMB DISPLAY ERROR:', err)
                        continue
                
                # for weapon_index in weaponList:
                #     try:
                #         weapon_entity = Entity(weapon_index)
                #         weapon_pos = weapon_entity.get_position()
                #         weapon_w2s_pos = meow.world_to_screen(view_matrix, weapon_pos, 1)
                        
                #         meow.draw_texture(texture = AK_47, posX = weapon_w2s_pos["x"], posY = weapon_w2s_pos["y"], rotation = 0, scale = 0.6,tint = Colors.white)
                        
                #     except Exception as err:
                #         # print('WEAPON DISPLAY ERROR:', err)
                #         continue
                
                spectators = []
                for ents in EntityList:
                        
                    try:
                        
                        entity = Entity(ents)
                                    
                        if Local_player.get_health() <= 0:
                            spectators.clear()
                            
                        if entity.get_team() == Local_player.get_team():
                            #Entity will be removed from spectator list only when WH can display it, thats why team check should be used until another method is not found
                            spectated = Engine.get_entity(entity.get_observed_target_handle() - 1)
                            if spectated == LocalPlayer.get_local_player():
                                spectators.append(entity.get_name)
                                meow.draw_font(
                                    fontId = 0,
                                    text= '\n'.join(spectators),
                                    posX=get_screen_width_x / 100,
                                    posY=get_screen_width_y / 1.8,
                                    fontSize=25,
                                    spacing = 2.0,
                                    tint = Colors.white,
                                )

            

                        if not entity.get_dormant() and entity.get_health() > 0 and Local_player.get_team() != entity.get_team() and ents != LocalPlayer.get_local_player():

                            entity_w2s = meow.world_to_screen(view_matrix, entity.get_position(), 1)
                            head_pos = meow.world_to_screen(view_matrix, entity.get_bone_position(8), 1)

                            head = entity_w2s["y"] - head_pos["y"]
                            width = head / 2
                            center = width / 2
            
                            meow.draw_circle(
                                centerX = head_pos["x"],
                                centerY = head_pos["y"],
                                radius = 3,
                                color = meow.get_color("red"),
                            )
            
                            meow.draw_rectangle_lines(
                                posX=head_pos['x'] - center * 1.0,
                                posY=head_pos['y'] - center / 2,
                                width=width * 1.0,
                                height=head + center / 2,
                                color=Colors.black,
                                lineThick=1.0,
                            )
                            
                            meow.draw_text(
                                text= f"H:{entity.get_health()}",
                                posX=head_pos["x"] - center - 25,
                                posY=head_pos["y"] - center / 2,
                                fontSize=1,
                                color=Colors.orange,
                            )
                            
                            meow.draw_text(
                                    text= entity.get_name,
                                    posX=head_pos["x"] - center - 10,
                                    posY=head_pos["y"] - center - 5,
                                    fontSize=5,
                                    color=Colors.white,
                                )

                            # meow.draw_text(
                            #     text= f"A:{entity.get_armour()}",
                            #     posX=head_pos["x"] - center - 25,
                            #     posY=(head_pos["y"] - center / 2) + 10,
                            #     fontSize=-1,
                            #     color=Colors.orange,
                            # )
            
                            # meow.gui_progress_bar(
                            #     posX=head_pos["x"] - center,
                            #     posY=entity_w2s["y"],
                            #     width=width,
                            #     height=10,
                            #     textLeft="HP: ",
                            #     textRight=f" {entity.get_health()}",
                            #     value=entity.get_health(),
                            #     minValue=0,
                            #     maxValue=100,
                            # )
    
                            get_entity_weapon = entity.getWeapon()

                            if get_entity_weapon in knife_weapons:
                                meow.draw_texture(texture = Knife, posX = head_pos["x"] - center / 1.1, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.orange)
                            
                            if get_entity_weapon == 1: meow.draw_texture(texture = Desert_Eagle, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 2: meow.draw_texture(texture = Dual_Berettas, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 3: meow.draw_texture(texture = Five_SeveN, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 4: meow.draw_texture(texture = Glock_18, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 7: meow.draw_texture(texture = AK_47, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 8: meow.draw_texture(texture = AUG, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 9: meow.draw_texture(texture = AWP, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 10: meow.draw_texture(texture = FAMAS, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 11: meow.draw_texture(texture = G3SG1, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 13: meow.draw_texture(texture = Galil_AR, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 14: meow.draw_texture(texture = M249, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 16: meow.draw_texture(texture = M4A4, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 17: meow.draw_texture(texture = MAC_10, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 19: meow.draw_texture(texture = P90, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 23: meow.draw_texture(texture = MP5_SD, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 24: meow.draw_texture(texture = UMP_45, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 25: meow.draw_texture(texture = XM1014, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 26: meow.draw_texture(texture = Bizon, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 27: meow.draw_texture(texture = MAG_7, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 28: meow.draw_texture(texture = Negev, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 29: meow.draw_texture(texture = Sawed_Off, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 30: meow.draw_texture(texture = Tec_9, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 31: meow.draw_texture(texture = Zeus, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 32: meow.draw_texture(texture = p2000, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 33: meow.draw_texture(texture = MP7, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 34: meow.draw_texture(texture = MP9, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 35: meow.draw_texture(texture = Nova, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 36: meow.draw_texture(texture = P250, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 38: meow.draw_texture(texture = SCAR_20, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 39: meow.draw_texture(texture = SG_553, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 40: meow.draw_texture(texture = SSG_08, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 60: meow.draw_texture(texture = M4A1_S, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 61: meow.draw_texture(texture = USP_S, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 63: meow.draw_texture(texture = CZ75_Auto, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 64: meow.draw_texture(texture = R8_Revolver, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            
                            if get_entity_weapon == 43: meow.draw_texture(texture = Flashbang, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 44: meow.draw_texture(texture = Explosive_Grenade, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 45: meow.draw_texture(texture = Smoke_Grenade, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 46: meow.draw_texture(texture = Molotov, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 47: meow.draw_texture(texture = Decoy_Grenade, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 48: meow.draw_texture(texture = Incendiary_Grenade, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                            if get_entity_weapon == 49: meow.draw_texture(texture = C4, posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.01, rotation = 0, scale = 0.3,tint = Colors.purple)
                    
                    except Exception as err:
                        # print('002', err)
                        continue

        meow.end_drawing()
        time.sleep(0.000001)

def main():
    try:
        meow.overlay_init(fps=155, title='test')
        threading.Thread(target=entity_parse, name='entity_parse', daemon=True).start()
        threading.Thread(target=trigger, name='trigger', daemon=True).start()
        # threading.Thread(target=rcs_control, name='rcs_control', daemon=True).start()
        esp()
        
    except Exception as err:
        print(f'Threads have been canceled! Exiting...\nReason: {err}\nExiting...')
        exit(0)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 600)
        MainWindow.setMinimumSize(QtCore.QSize(700, 600))
        MainWindow.setMaximumSize(QtCore.QSize(720, 600))
        MainWindow.setStyleSheet(
            "QMainWindow {background: transparent; }\n"
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
            "}"
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background: transparent;\n" "")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftMenuContainer = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.leftMenuContainer.sizePolicy().hasHeightForWidth()
        )
        self.leftMenuContainer.setSizePolicy(sizePolicy)
        self.leftMenuContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.leftMenuContainer.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.leftMenuContainer.setObjectName("leftMenuContainer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.leftMenuContainer)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leftMenuSubContainer = QtWidgets.QWidget(self.leftMenuContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.leftMenuSubContainer.sizePolicy().hasHeightForWidth()
        )
        self.leftMenuSubContainer.setSizePolicy(sizePolicy)
        self.leftMenuSubContainer.setStyleSheet("")
        self.leftMenuSubContainer.setObjectName("leftMenuSubContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.leftMenuSubContainer)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.leftMenuHeaderContainer = QtWidgets.QFrame(self.leftMenuSubContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.leftMenuHeaderContainer.sizePolicy().hasHeightForWidth()
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenuBtn.sizePolicy().hasHeightForWidth())
        self.leftMenuBtn.setSizePolicy(sizePolicy)
        self.leftMenuBtn.setMinimumSize(QtCore.QSize(70, 60))
        self.leftMenuBtn.setStyleSheet(
            "QPushButton:hover {\n"
            "    background-color: rgb(33, 37, 43);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(85, 170, 255);\n"
            "}\n"
            ""
        )
        self.leftMenuBtn.setText("")
        self.leftMenuBtn.setIconSize(QtCore.QSize(34, 34))
        self.leftMenuBtn.setObjectName("leftMenuBtn")
        self.verticalLayout_3.addWidget(self.leftMenuBtn)
        self.verticalLayout_2.addWidget(
            self.leftMenuHeaderContainer, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop
        )
        self.leftMenuMainContainer = QtWidgets.QFrame(self.leftMenuSubContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.leftMenuMainContainer.sizePolicy().hasHeightForWidth()
        )
        self.leftMenuMainContainer.setSizePolicy(sizePolicy)
        self.leftMenuMainContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftMenuMainContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftMenuMainContainer.setObjectName("leftMenuMainContainer")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.leftMenuMainContainer)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.wallhackBtn = QtWidgets.QPushButton(self.leftMenuMainContainer)
        self.wallhackBtn.setMinimumSize(QtCore.QSize(0, 60))
        self.wallhackBtn.setStyleSheet(
            "QPushButton:hover {\n"
            "    background-color: rgb(33, 37, 43);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(85, 170, 255);\n"
            "}\n"
            ""
        )
        self.wallhackBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/UI/icons/eye_icon.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.wallhackBtn.setIcon(icon)
        self.wallhackBtn.setIconSize(QtCore.QSize(36, 36))
        self.wallhackBtn.setObjectName("wallhackBtn")
        self.verticalLayout_4.addWidget(self.wallhackBtn)
        self.playersBtn = QtWidgets.QPushButton(self.leftMenuMainContainer)
        self.playersBtn.setMinimumSize(QtCore.QSize(0, 60))
        self.playersBtn.setStyleSheet(
            "QPushButton:hover {\n"
            "    background-color: rgb(33, 37, 43);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(85, 170, 255);\n"
            "}\n"
            ""
        )
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/UI/icons/players_icon.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.playersBtn.setIcon(icon1)
        self.playersBtn.setIconSize(QtCore.QSize(36, 36))
        self.playersBtn.setObjectName("playersBtn")
        self.verticalLayout_4.addWidget(self.playersBtn)
        self.verticalLayout_2.addWidget(
            self.leftMenuMainContainer, 0, QtCore.Qt.AlignTop
        )
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.leftMenuFooterContainer = QtWidgets.QFrame(self.leftMenuSubContainer)
        self.leftMenuFooterContainer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftMenuFooterContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftMenuFooterContainer.setObjectName("leftMenuFooterContainer")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.leftMenuFooterContainer)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.settingsBtn = QtWidgets.QPushButton(self.leftMenuFooterContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsBtn.sizePolicy().hasHeightForWidth())
        self.settingsBtn.setSizePolicy(sizePolicy)
        self.settingsBtn.setMinimumSize(QtCore.QSize(50, 60))
        self.settingsBtn.setStyleSheet(
            "QPushButton:hover {\n"
            "    background-color: rgb(33, 37, 43);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(85, 170, 255);\n"
            "}\n"
            ""
        )
        self.settingsBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/UI/icons/settings_icon.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.settingsBtn.setIcon(icon2)
        self.settingsBtn.setIconSize(QtCore.QSize(36, 36))
        self.settingsBtn.setObjectName("settingsBtn")
        self.verticalLayout_5.addWidget(self.settingsBtn)
        self.verticalLayout_2.addWidget(
            self.leftMenuFooterContainer, 0, QtCore.Qt.AlignBottom
        )
        self.verticalLayout.addWidget(self.leftMenuSubContainer, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout.addWidget(self.leftMenuContainer, 0, QtCore.Qt.AlignLeft)
        self.mainBodyContainer = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainBodyContainer.sizePolicy().hasHeightForWidth()
        )
        self.mainBodyContainer.setSizePolicy(sizePolicy)
        self.mainBodyContainer.setStyleSheet("background-color: transparent;")
        self.mainBodyContainer.setObjectName("mainBodyContainer")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.mainBodyContainer)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.headerContainer = QtWidgets.QWidget(self.mainBodyContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.headerContainer.sizePolicy().hasHeightForWidth()
        )
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
        self.headerBtnMinimise.setStyleSheet(
            "QPushButton:hover {\n"
            "    background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(85, 170, 255);\n"
            "}"
        )
        self.headerBtnMinimise.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/RecodeV2/UI/icons/minus_icon.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.headerBtnMinimise.setIcon(icon3)
        self.headerBtnMinimise.setIconSize(QtCore.QSize(24, 24))
        self.headerBtnMinimise.setObjectName("headerBtnMinimise")
        self.horizontalLayout_6.addWidget(self.headerBtnMinimise)
        self.headerBtnClose = QtWidgets.QPushButton(self.rightBtnContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.headerBtnClose.sizePolicy().hasHeightForWidth()
        )
        self.headerBtnClose.setSizePolicy(sizePolicy)
        self.headerBtnClose.setMinimumSize(QtCore.QSize(40, 40))
        self.headerBtnClose.setStyleSheet(
            "QPushButton:hover {\n"
            "    background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(85, 170, 255);\n"
            "}"
        )
        self.headerBtnClose.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/RecodeV2/UI/icons/cross_icon.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.headerBtnClose.setIcon(icon4)
        self.headerBtnClose.setIconSize(QtCore.QSize(24, 24))
        self.headerBtnClose.setObjectName("headerBtnClose")
        self.horizontalLayout_6.addWidget(self.headerBtnClose)
        self.horizontalLayout_3.addWidget(
            self.rightBtnContainer, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop
        )
        self.verticalLayout_6.addWidget(self.headerContainer, 0, QtCore.Qt.AlignTop)
        self.mainBodyContent = QtWidgets.QFrame(self.mainBodyContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainBodyContent.sizePolicy().hasHeightForWidth()
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mainBodyWidget.sizePolicy().hasHeightForWidth()
        )
        self.mainBodyWidget.setSizePolicy(sizePolicy)
        self.mainBodyWidget.setStyleSheet("")
        self.mainBodyWidget.setObjectName("mainBodyWidget")
        self.playersPage = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playersPage.sizePolicy().hasHeightForWidth())
        self.playersPage.setSizePolicy(sizePolicy)
        self.playersPage.setStyleSheet("")
        self.playersPage.setObjectName("playersPage")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.playersPage)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.playersTopBar = QtWidgets.QWidget(self.playersPage)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersTopBar.sizePolicy().hasHeightForWidth()
        )
        self.playersTopBar.setSizePolicy(sizePolicy)
        self.playersTopBar.setStyleSheet("background-color: rgb(29, 32, 40);")
        self.playersTopBar.setObjectName("playersTopBar")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.playersTopBar)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.playersRefreshMsgContainer = QtWidgets.QWidget(self.playersTopBar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersRefreshMsgContainer.sizePolicy().hasHeightForWidth()
        )
        self.playersRefreshMsgContainer.setSizePolicy(sizePolicy)
        self.playersRefreshMsgContainer.setObjectName("playersRefreshMsgContainer")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.playersRefreshMsgContainer)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.playersRefreshMsg = QtWidgets.QLabel(self.playersRefreshMsgContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersRefreshMsg.sizePolicy().hasHeightForWidth()
        )
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
        self.horizontalLayout_5.addWidget(
            self.playersRefreshMsgContainer, 0, QtCore.Qt.AlignLeft
        )
        self.playersRefreshBtnContainer = QtWidgets.QWidget(self.playersTopBar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersRefreshBtnContainer.sizePolicy().hasHeightForWidth()
        )
        self.playersRefreshBtnContainer.setSizePolicy(sizePolicy)
        self.playersRefreshBtnContainer.setMinimumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtnContainer.setMaximumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtnContainer.setStyleSheet(
            "QWidget{\n"
            "    background-color: rgb(27, 29, 55);\n"
            "}\n"
            "QWidget:hover {\n"
            "    background-color: rgb(33, 37, 60);\n"
            "}\n"
            "QWidget:pressed {\n"
            "    background-color: rgb(33, 37, 255);\n"
            "}\n"
            ""
        )
        self.playersRefreshBtnContainer.setObjectName("playersRefreshBtnContainer")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.playersRefreshBtnContainer)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.playersRefreshBtn = QtWidgets.QPushButton(self.playersRefreshBtnContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersRefreshBtn.sizePolicy().hasHeightForWidth()
        )
        self.playersRefreshBtn.setSizePolicy(sizePolicy)
        self.playersRefreshBtn.setMinimumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtn.setMaximumSize(QtCore.QSize(50, 40))
        self.playersRefreshBtn.setStyleSheet("")
        self.playersRefreshBtn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/UI/icons/refresh_icon.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.playersRefreshBtn.setIcon(icon5)
        self.playersRefreshBtn.setIconSize(QtCore.QSize(24, 24))
        self.playersRefreshBtn.setObjectName("playersRefreshBtn")
        self.verticalLayout_16.addWidget(self.playersRefreshBtn)
        self.horizontalLayout_5.addWidget(
            self.playersRefreshBtnContainer, 0, QtCore.Qt.AlignRight
        )
        self.verticalLayout_8.addWidget(self.playersTopBar)
        self.playersContainer = QtWidgets.QWidget(self.playersPage)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersContainer.sizePolicy().hasHeightForWidth()
        )
        self.playersContainer.setSizePolicy(sizePolicy)
        self.playersContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.playersContainer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.playersContainer.setFont(font)
        self.playersContainer.setStyleSheet("background-color: rgb(43, 51, 66);\n" "")
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
        self.PlayersNameHeader.setMinimumSize(QtCore.QSize(0, 0))
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
        self.playersName8.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName8.setObjectName("playersName8")
        self.verticalLayout_11.addWidget(self.playersName8)
        self.playersName9 = QtWidgets.QLabel(self.playersNameContainer)
        self.playersName9.setMinimumSize(QtCore.QSize(0, 45))
        self.playersName9.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersName9.setFont(font)
        self.playersName9.setAlignment(QtCore.Qt.AlignCenter)
        self.playersName9.setObjectName("playersName9")
        self.verticalLayout_11.addWidget(self.playersName9)
        self.horizontalLayout_4.addWidget(self.playersNameContainer)
        self.playersRankContainer = QtWidgets.QWidget(self.playersContainer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.playersRankContainer.sizePolicy().hasHeightForWidth()
        )
        self.playersRankContainer.setSizePolicy(sizePolicy)
        self.playersRankContainer.setMinimumSize(QtCore.QSize(100, 0))
        self.playersRankContainer.setMaximumSize(QtCore.QSize(0, 16777215))
        self.playersRankContainer.setStyleSheet("QLabel{\n" "    padding: 10px;\n" "}")
        self.playersRankContainer.setObjectName("playersRankContainer")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.playersRankContainer)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.playersRankHeader = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRankHeader.setMinimumSize(QtCore.QSize(0, 0))
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
        self.playersRank0.setStyleSheet("")
        self.playersRank0.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.playersRank0.setText("")
        self.playersRank0.setTextFormat(QtCore.Qt.AutoText)
        self.playersRank0.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/global.png"))
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
        self.playersRank1.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/gn1.png"))
        self.playersRank1.setScaledContents(True)
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
        self.playersRank2.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/gn1.png"))
        self.playersRank2.setScaledContents(True)
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
        self.playersRank3.setStyleSheet("")
        self.playersRank3.setText("")
        self.playersRank3.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/gn1.png"))
        self.playersRank3.setScaledContents(True)
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
        self.playersRank4.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/gn1.png"))
        self.playersRank4.setScaledContents(True)
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
        self.playersRank5.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/gn1.png"))
        self.playersRank5.setScaledContents(True)
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
        self.playersRank6.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/global.png"))
        self.playersRank6.setScaledContents(True)
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
        self.playersRank7.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/gn1.png"))
        self.playersRank7.setScaledContents(True)
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
        self.playersRank8.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/global.png"))
        self.playersRank8.setScaledContents(True)
        self.playersRank8.setAlignment(QtCore.Qt.AlignCenter)
        self.playersRank8.setObjectName("playersRank8")
        self.verticalLayout_9.addWidget(self.playersRank8)
        self.playersRank9 = QtWidgets.QLabel(self.playersRankContainer)
        self.playersRank9.setMaximumSize(QtCore.QSize(16777215, 45))
        self.playersRank9.setText("")
        self.playersRank9.setPixmap(QtGui.QPixmap(":/ranks/UI/Ranks/gn3.png"))
        self.playersRank9.setScaledContents(True)
        self.playersRank9.setObjectName("playersRank9")
        self.verticalLayout_9.addWidget(self.playersRank9)
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
        self.playersWinsHeader.setMinimumSize(QtCore.QSize(0, 38))
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
        self.playersWins4.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins4.setObjectName("playersWins4")
        self.verticalLayout_12.addWidget(self.playersWins4)
        self.playersWins5 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins5.setMinimumSize(QtCore.QSize(0, 0))
        self.playersWins5.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins5.setFont(font)
        self.playersWins5.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins5.setObjectName("playersWins5")
        self.verticalLayout_12.addWidget(self.playersWins5)
        self.playersWins6 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins6.setMinimumSize(QtCore.QSize(0, 0))
        self.playersWins6.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins6.setFont(font)
        self.playersWins6.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins6.setObjectName("playersWins6")
        self.verticalLayout_12.addWidget(self.playersWins6)
        self.playersWins7 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins7.setMinimumSize(QtCore.QSize(0, 0))
        self.playersWins7.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins7.setFont(font)
        self.playersWins7.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins7.setObjectName("playersWins7")
        self.verticalLayout_12.addWidget(self.playersWins7)
        self.playersWins8 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins8.setMinimumSize(QtCore.QSize(0, 0))
        self.playersWins8.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins8.setFont(font)
        self.playersWins8.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins8.setObjectName("playersWins8")
        self.verticalLayout_12.addWidget(self.playersWins8)
        self.playersWins9 = QtWidgets.QLabel(self.playersWinsContainer)
        self.playersWins9.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.playersWins9.setFont(font)
        self.playersWins9.setAlignment(QtCore.Qt.AlignCenter)
        self.playersWins9.setObjectName("playersWins9")
        self.verticalLayout_12.addWidget(self.playersWins9)
        self.horizontalLayout_4.addWidget(self.playersWinsContainer)
        self.playersFaceitContainer = QtWidgets.QWidget(self.playersContainer)
        self.playersFaceitContainer.setMinimumSize(QtCore.QSize(100, 0))
        self.playersFaceitContainer.setMaximumSize(QtCore.QSize(100, 16777215))
        self.playersFaceitContainer.setStyleSheet(
            "QPushButton:hover {\n" "    background-color: rgb(60, 65, 75);\n" "}"
        )
        self.playersFaceitContainer.setObjectName("playersFaceitContainer")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.playersFaceitContainer)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.playersFaceitHeader = QtWidgets.QLabel(self.playersFaceitContainer)
        self.playersFaceitHeader.setMinimumSize(QtCore.QSize(0, 0))
        self.playersFaceitHeader.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceitHeader.setFont(font)
        self.playersFaceitHeader.setStyleSheet(
            "background-color: hsl(223, 28, 43, 50%)"
        )
        self.playersFaceitHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.playersFaceitHeader.setObjectName("playersFaceitHeader")
        self.verticalLayout_14.addWidget(self.playersFaceitHeader)
        self.playersFaceit0 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit0.setMinimumSize(QtCore.QSize(0, 45))
        self.playersFaceit0.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.playersFaceit0.setFont(font)
        self.playersFaceit0.setStyleSheet("")
        self.playersFaceit0.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/UI/icons/faceit_icon.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.playersFaceit0.setIcon(icon6)
        self.playersFaceit0.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit0.setCheckable(False)
        self.playersFaceit0.setObjectName("playersFaceit0")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.playersFaceit0)
        self.verticalLayout_14.addWidget(self.playersFaceit0)
        self.playersFaceit1 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit1.setMinimumSize(QtCore.QSize(0, 45))
        self.playersFaceit1.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit2.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit3.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit4.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit5.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit6.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit7.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit8.setMaximumSize(QtCore.QSize(16777215, 45))
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
        self.playersFaceit9 = QtWidgets.QPushButton(self.playersFaceitContainer)
        self.playersFaceit9.setMinimumSize(QtCore.QSize(0, 45))
        self.playersFaceit9.setMaximumSize(QtCore.QSize(16777215, 45))
        self.playersFaceit9.setText("")
        self.playersFaceit9.setIcon(icon6)
        self.playersFaceit9.setIconSize(QtCore.QSize(50, 1000))
        self.playersFaceit9.setObjectName("playersFaceit9")
        self.verticalLayout_14.addWidget(self.playersFaceit9)
        self.horizontalLayout_4.addWidget(self.playersFaceitContainer)
        self.playersCSGOStatsContainer = QtWidgets.QWidget(self.playersContainer)
        self.playersCSGOStatsContainer.setMinimumSize(QtCore.QSize(100, 45))
        self.playersCSGOStatsContainer.setMaximumSize(QtCore.QSize(100, 16777215))
        self.playersCSGOStatsContainer.setStyleSheet(
            "QPushButton:hover {\n" "    background-color: rgb(60, 65, 75);\n" "}"
        )
        self.playersCSGOStatsContainer.setObjectName("playersCSGOStatsContainer")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.playersCSGOStatsContainer)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.CSGOStatsHeader = QtWidgets.QLabel(self.playersCSGOStatsContainer)
        self.CSGOStatsHeader.setMinimumSize(QtCore.QSize(0, 0))
        self.CSGOStatsHeader.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.CSGOStatsHeader.setFont(font)
        self.CSGOStatsHeader.setStyleSheet(
            "QLabel{\n" "    background-color: hsl(223, 28, 43, 50%);\n" "}"
        )
        self.CSGOStatsHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.CSGOStatsHeader.setObjectName("CSGOStatsHeader")
        self.verticalLayout_15.addWidget(self.CSGOStatsHeader)
        self.CSGOStatsBtn0 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn0.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn0.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn0.setFont(font)
        self.CSGOStatsBtn0.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/UI/icons/csgoPlayer_icon.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.CSGOStatsBtn0.setIcon(icon7)
        self.CSGOStatsBtn0.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn0.setCheckable(False)
        self.CSGOStatsBtn0.setObjectName("CSGOStatsBtn0")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.CSGOStatsBtn0)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn0)
        self.CSGOStatsBtn1 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn1.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn1.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn1.setFont(font)
        self.CSGOStatsBtn1.setText("")
        self.CSGOStatsBtn1.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn1.setObjectName("CSGOStatsBtn1")
        self.buttonGroup.addButton(self.CSGOStatsBtn1)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn1)
        self.CSGOStatsBtn2 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn2.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn2.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn2.setFont(font)
        self.CSGOStatsBtn2.setText("")
        self.CSGOStatsBtn2.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn2.setObjectName("CSGOStatsBtn2")
        self.buttonGroup.addButton(self.CSGOStatsBtn2)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn2)
        self.CSGOStatsBtn3 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn3.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn3.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn3.setFont(font)
        self.CSGOStatsBtn3.setText("")
        self.CSGOStatsBtn3.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn3.setObjectName("CSGOStatsBtn3")
        self.buttonGroup.addButton(self.CSGOStatsBtn3)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn3)
        self.CSGOStatsBtn4 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn4.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn4.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn4.setFont(font)
        self.CSGOStatsBtn4.setText("")
        self.CSGOStatsBtn4.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn4.setObjectName("CSGOStatsBtn4")
        self.buttonGroup.addButton(self.CSGOStatsBtn4)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn4)
        self.CSGOStatsBtn5 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn5.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn5.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn5.setFont(font)
        self.CSGOStatsBtn5.setText("")
        self.CSGOStatsBtn5.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn5.setObjectName("CSGOStatsBtn5")
        self.buttonGroup.addButton(self.CSGOStatsBtn5)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn5)
        self.CSGOStatsBtn6 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn6.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn6.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn6.setFont(font)
        self.CSGOStatsBtn6.setText("")
        self.CSGOStatsBtn6.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn6.setObjectName("CSGOStatsBtn6")
        self.buttonGroup.addButton(self.CSGOStatsBtn6)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn6)
        self.CSGOStatsBtn7 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn7.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn7.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn7.setFont(font)
        self.CSGOStatsBtn7.setText("")
        self.CSGOStatsBtn7.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn7.setObjectName("CSGOStatsBtn7")
        self.buttonGroup.addButton(self.CSGOStatsBtn7)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn7)
        self.CSGOStatsBtn8 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn8.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn8.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CSGOStatsBtn8.setFont(font)
        self.CSGOStatsBtn8.setText("")
        self.CSGOStatsBtn8.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn8.setObjectName("CSGOStatsBtn8")
        self.buttonGroup.addButton(self.CSGOStatsBtn8)
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn8)
        self.CSGOStatsBtn9 = QtWidgets.QPushButton(self.playersCSGOStatsContainer)
        self.CSGOStatsBtn9.setMinimumSize(QtCore.QSize(0, 45))
        self.CSGOStatsBtn9.setMaximumSize(QtCore.QSize(16777215, 45))
        self.CSGOStatsBtn9.setText("")
        self.CSGOStatsBtn9.setIcon(icon7)
        self.CSGOStatsBtn9.setIconSize(QtCore.QSize(25, 1000))
        self.CSGOStatsBtn9.setObjectName("CSGOStatsBtn9")
        self.verticalLayout_15.addWidget(self.CSGOStatsBtn9)
        self.horizontalLayout_4.addWidget(self.playersCSGOStatsContainer)
        self.verticalLayout_8.addWidget(self.playersContainer, 0, QtCore.Qt.AlignLeft)
        self.mainBodyWidget.addWidget(self.playersPage)
        self.settingsPage = QtWidgets.QWidget()
        self.settingsPage.setStyleSheet("background-color: rgb(29, 32, 40);\n" "")
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
        self.widget_3.setStyleSheet(
            "border-bottom: 2px solid #212D4B;\n" "padding: 0 0 5px 0;"
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.horizontalSlider.sizePolicy().hasHeightForWidth()
        )
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
        icon7.addPixmap(QtGui.QPixmap(":/icons/UI/icons/faceit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/UI/icons/csgoPlayer_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        Rank_Global = QtGui.QPixmap(":/ranks/UI/Ranks/global.png")
        Rank_Supreme = QtGui.QPixmap(":/ranks/UI/Ranks/supreme.png")
        Rank_Lem = QtGui.QPixmap(":/ranks/UI/Ranks/lem.png")
        Rank_Le = QtGui.QPixmap(":/ranks/UI/Ranks/le.png")
        Rank_Dmg = QtGui.QPixmap(":/ranks/UI/Ranks/dmg.png")
        Rank_Mg3 = QtGui.QPixmap(":/ranks/UI/Ranks/mg2.png")
        Rank_Mg2 = QtGui.QPixmap(":/ranks/UI/Ranks/mg1.png")
        Rank_Mg1 = QtGui.QPixmap(":/ranks/UI/Ranks/mg.png")
        Rank_Gn4 = QtGui.QPixmap(":/ranks/UI/Ranks/gn4.png")
        Rank_Gn3 = QtGui.QPixmap(":/ranks/UI/Ranks/gn3.png")
        Rank_Gn2 = QtGui.QPixmap(":/ranks/UI/Ranks/gn2.png")
        Rank_Gn1 = QtGui.QPixmap(":/ranks/UI/Ranks/gn1.png")
        Rank_Se = QtGui.QPixmap(":/ranks/UI/Ranks/silver_elite.png")
        Rank_S5 = QtGui.QPixmap(":/ranks/UI/Ranks/silver5.png")
        Rank_S4 = QtGui.QPixmap(":/ranks/UI/Ranks/silver4.png")
        Rank_S3 = QtGui.QPixmap(":/ranks/UI/Ranks/silver3.png")
        Rank_S2 = QtGui.QPixmap(":/ranks/UI/Ranks/silver2.png")
        Rank_S1 = QtGui.QPixmap(":/ranks/UI/Ranks/silver1.png")
        
        #Add unranked image -- Future update
        
        steamidsFounds = 0
        for steamids in playersInfo: #Check that the button is not clicked when nothing is there otherwise - crash
            if steamids[5] > 1:
                steamidsFounds = 1 
            else:
                print('error')      
        
        if steamidsFounds == 1:
        
            if len(playersInfo) <= 10:
            
                for i in range(0, len(playersInfo)): #Display players by team -- future update
                    playerNames = 'self.playersName' + str(i) + '.setText(_translate("MainWindow", str(playersInfo[' + str(i) + '][1])))'
                    playerWins = 'self.playersWins' + str(i) + '.setText(_translate("MainWindow", str(playersInfo[' + str(i) + '][4])))'
                    playersFaceit = 'self.playersFaceit' + str(i) + '.setIcon(icon7)'
                    playersCSGOStats = 'self.CSGOStatsBtn' + str(i) + '.setIcon(icon8)'
                    
                    
                    exec(playerNames), exec(playerWins), exec(playersFaceit), exec(playersCSGOStats)
                    
                    for ranks in playersInfo[i][3]:
                        print(ranks)
                    
                    if playersInfo[i][3] == 18: #Global
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Global)'
                    elif playersInfo[i][3] == 17:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Supreme)'
                    elif playersInfo[i][3] == 16:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Lem)'
                    elif playersInfo[i][3] == 15:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Le)'
                    elif playersInfo[i][3] == 14:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Dmg)'
                    elif playersInfo[i][3] == 13:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Mg3)'
                    elif playersInfo[i][3] == 12:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Mg2)'
                    elif playersInfo[i][3] == 11:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Mg1)'
                    elif playersInfo[i][3] == 10:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Gn4)'
                    elif playersInfo[i][3] == 9:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Gn3)'
                    elif playersInfo[i][3] == 8:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Gn2)'
                    elif playersInfo[i][3] == 7:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Gn1)'
                    elif playersInfo[i][3] == 6:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Se)'
                    elif playersInfo[i][3] == 5:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_S5)'
                    elif playersInfo[i][3] == 4:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_S4)'
                    elif playersInfo[i][3] == 3:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_S3)'
                    elif playersInfo[i][3] == 2:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_S2)'
                    elif playersInfo[i][3] == 1:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_S1)'
                    elif playersInfo[i][3] == 0:
                        playersRank = 'self.playersRank' + str(i) + '.setPixmap(Rank_Supreme)'
                        print('Rank 0')
                    else:
                        playersRank = 'print("No rank")'
                
                    exec(playersRank)
            else:
                print("222")

    def openFaceit(self, btn):
        steamidsFounds = 0
        for steamids in playersInfo: #Check that the button is not clicked when nothing is there otherwise - crash
            if steamids[5] > 1:
                steamidsFounds = 1
        
        if steamidsFounds == 1:
            if btn == -2: # btn0
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[0][5]))
            if btn == -3:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[1][5]))
            if btn == -4:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[2][5]))
            if btn == -5:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[3][5]))
            if btn == -6:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[4][5]))
            if btn == -7:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[5][5]))
            if btn == -8:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[6][5]))
            if btn == -9:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[7][5]))
            if btn == -10:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[8][5]))
            if btn == -11:
                webbrowser.open('https://faceitfinder.com/stats/' + str(playersInfo[9][5]))

    def openCSGOStats(self, btn):
        steamidsFounds = 0
        for steamids in playersInfo: #Check that the button is not clicked when nothing is there otherwise - crash
            if steamids[5] > 1:
                steamidsFounds = 1
        
        if steamidsFounds == 1:
            if btn == -2: # btn0
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[0][5]))
            if btn == -3:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[1][5]))
            if btn == -4:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[2][5]))
            if btn == -5:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[3][5]))
            if btn == -6:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[4][5]))
            if btn == -7:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[5][5]))
            if btn == -8:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[6][5]))
            if btn == -9:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[7][5]))
            if btn == -10:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[8][5]))
            if btn == -11:
                webbrowser.open('https://csgostats.gg/player/' + str(playersInfo[9][5]))

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
        self.playersRefreshMsg.setText(_translate("MainWindow", "STATUS:"))
        self.PlayersNameHeader.setText(_translate("MainWindow", "NAME"))
        self.playersName0.setText(_translate("MainWindow", "PLAYER"))
        self.playersName1.setText(_translate("MainWindow", "1"))
        self.playersName2.setText(_translate("MainWindow", "2"))
        self.playersName3.setText(_translate("MainWindow", "3"))
        self.playersName4.setText(_translate("MainWindow", "4"))
        self.playersName5.setText(_translate("MainWindow", "5"))
        self.playersName6.setText(_translate("MainWindow", "6"))
        self.playersName7.setText(_translate("MainWindow", "7"))
        self.playersName8.setText(_translate("MainWindow", "asdasdasdasd"))
        self.playersName9.setText(_translate("MainWindow", "asdadasdasd"))
        self.playersRankHeader.setText(_translate("MainWindow", "RANK"))
        self.playersWinsHeader.setText(_translate("MainWindow", "WINS"))
        self.playersWins0.setText(_translate("MainWindow", "999"))
        self.playersWins1.setText(_translate("MainWindow", "1"))
        self.playersWins2.setText(_translate("MainWindow", "1"))
        self.playersWins3.setText(_translate("MainWindow", "1"))
        self.playersWins4.setText(_translate("MainWindow", "1"))
        self.playersWins5.setText(_translate("MainWindow", "1"))
        self.playersWins6.setText(_translate("MainWindow", "1"))
        self.playersWins7.setText(_translate("MainWindow", "1"))
        self.playersWins8.setText(_translate("MainWindow", "2322"))
        self.playersWins9.setText(_translate("MainWindow", "123"))
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

if __name__ == '__main__':  
    try:
        haze = get(
            "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
        ).json()

        [setattr(Offsets, k, v) for k, v in haze["signatures"].items()]
        [setattr(Offsets, k, v) for k, v in haze["netvars"].items()]
    except:
        print("Unable to fetch Offsets")
        exit(0)
 
    try:
        csgo = Pymem('csgo.exe')
        csgo_client = process.module_from_name(csgo.process_handle, 'client.dll').lpBaseOfDll
        csgo_engine = process.module_from_name(csgo.process_handle, 'engine.dll').lpBaseOfDll
        
        ntdll = ctypes.windll.ntdll
        k32 = ctypes.windll.kernel32
        u32 = ctypes.windll.user32
    except Exception as err:
        print(err)
        print('Could not find CS:GO process!\nMake sure the game is running first!')
        exit(0)
        
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    main()
    
    sys.exit(app.exec_())
