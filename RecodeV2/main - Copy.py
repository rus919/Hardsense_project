import os, struct
from dataclasses import dataclass
import ctypes as ctypes
import threading
from requests import get

from pymem import Pymem, process, exception, pattern

import pyMeow as meow

import mouse
import time

class Offsets:
    pass

class Colors:
    orange = meow.get_color("orange")
    black = meow.get_color("black")
    purple = meow.get_color("purple")
    
class LocalPlayer():
    def __init__(self, address):
        self.address = address
    
    @staticmethod
    def get_local_player():
        return meow.r_uint(csgo, csgo_client + Offsets.dwLocalPlayer)
    
    @staticmethod
    def get_crosshair_id():
        return meow.r_uint(csgo, LocalPlayer.get_local_player() + Offsets.m_iCrosshairId)

class Entity():
    def __init__(self, address):
        self.address = address
    
    def get_id(self):
        return meow.r_int(csgo, self.address + 0x64)
    
    def get_team(self):
        return meow.r_int(csgo, self.address + Offsets.m_iTeamNum)
    
    def get_health(self):
        return meow.r_int(csgo, self.address + Offsets.m_iHealth)
    
    def get_armour(self):
        return meow.r_int(csgo, self.address + Offsets.m_ArmorValue)

    def get_dormant(self):
        return meow.r_int(csgo, self.address + Offsets.m_bDormant)

    def get_position(self):
        localpos_x = meow.r_float(csgo, self.address + Offsets.m_vecOrigin)
        localpos_y = meow.r_float(csgo, self.address + Offsets.m_vecOrigin + 4)
        localpos_z = meow.r_float(csgo, self.address + Offsets.m_vecOrigin + 8)
        return meow.vec3(localpos_x, localpos_y, localpos_z)

    def get_bone_position(self, bone_id: int):
        bone_matrix = meow.r_uint(csgo, self.address + Offsets.m_dwBoneMatrix)
        return meow.vec3(meow.r_float(csgo, bone_matrix + 0x30 * bone_id + 0x0c),
                       meow.r_float(csgo, bone_matrix + 0x30 * bone_id + 0x1c),
                       meow.r_float(csgo, bone_matrix + 0x30 * bone_id + 0x2c)
        )
  
    def getWeapon(self):
        getWeaponAddress = meow.r_uint(csgo, self.address + Offsets.m_hActiveWeapon) & 0xFFF
        getWeaponAddressHandle = meow.r_uint(csgo, csgo_client + Offsets.dwEntityList + (getWeaponAddress - 1) * 0x10)
        return meow.r_int16(csgo, getWeaponAddressHandle + Offsets.m_iItemDefinitionIndex)
    
    # def get_player_name(index):
    #     player_info = csgo.read_uint(Engine.get_state() + Offsets.dwClientState_PlayerInfo)
    #     player_items = csgo.read_uint(csgo.read_uint(player_info + 0x40) + 0xC)
    #     info = csgo.read_uint(player_items + 0x28 + (index * 0x34))
    #     if info != 0:
    #         return csgo.read_bytes(info + 0x10, 32) #0x94
        
    @property
    def get_name(self):
        radar_base = meow.r_uint(csgo, csgo_client + Offsets.dwRadarBase)
        hud_radar = meow.r_uint(csgo, radar_base + 0x78)
        return meow.r_string(csgo, hud_radar + 0x300 + (0x174 * (self.get_id() - 1)), 32)
    
    def get_observed_target_handle(self):
        return meow.r_uint(csgo, self.address + Offsets.m_hObserverTarget) & 0xFFF
        

class Engine():
    @staticmethod
    def get_entity(index):
        # return meow.r_int64(csgo, csgo_client + Offsets.dwEntityList + index * 0x10)
        return csgo2.read_uint(csgo_client2 + Offsets.dwEntityList + index * 0x10)

    @staticmethod
    def get_view_matrix():
        view = meow.r_bytes(csgo, csgo_client + Offsets.dwViewMatrix, 64)
        matrix = struct.unpack("16f", view)
        return matrix

    @staticmethod
    def get_state():
        return meow.r_uint(csgo, csgo_engine + Offsets.dwClientState)
    
    @staticmethod
    def get_client_state():
        return meow.r_uint(csgo, Engine.get_state() + Offsets.dwClientState_State)
    
    @staticmethod
    def test(index):
        raw = csgo2.read_bytes(csgo_client2 + Offsets.dwEntityList + index * 0x10, struct.calcsize('I'))
        # print(struct.calcsize('I'))
        raw2 = struct.unpack('<I', raw)[0]
        return raw2

def GetWindowText(handle, length=100):
        window_text = ctypes.create_string_buffer(length)
        u32.GetWindowTextA(
            handle,
            ctypes.byref(window_text),
            length
        )
        return window_text.value

EntityList = []
def entity_parse():
    while True:
        if Engine.get_client_state() == 6:
            try:
                EntityList.clear()
                
                # ent_addrs = meow.r_uints(csgo, csgo_client + Offsets.dwEntityList, 128)[0::4]
                # print(ent_addrs)
                for i in range(1, 64):                    
                    entity = Engine.get_entity(i)
                    print(entity)
                    if entity != 0:
                        # client_networkable = csgo2.read_uint(entity + 0x8)
                        # dwGetClientClassFn = csgo2.read_uint(client_networkable + 0x8)
                        # entity_client_class = csgo2.read_uint(dwGetClientClassFn+ 0x1)
                        # class_id = csgo2.read_uint(entity_client_class + 0x14)
                        # if class_id == 40:					
                        if [entity] not in EntityList:
                            EntityList.append(entity)
                # print(EntityList)
                        # tempEntList = EntityList
            except Exception as err:
                print('entity_parse: ', err)
                pass
        else:
            k32.Sleep(2000)
            continue
        # print(EntityList)
        time.sleep(10.0)

def trigger():
    while True:
        if Engine.get_client_state() == 6 and GetWindowText( u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
            if u32.GetAsyncKeyState(6):
                Local_player = Entity(LocalPlayer.get_local_player())            
                entity_id = LocalPlayer.get_crosshair_id()
                if entity_id != 0 and entity_id < 64:
                    entity = Entity(Engine.get_entity(entity_id - 1))
                    
                    if Local_player.get_team() != entity.get_team() and entity.get_health() > 0:
                        k32.Sleep(1)
                        mouse.click()
                        k32.Sleep(200)

def esp():
    # weapon_id_list = [1, 2, 3, 4, 7, 8, 9, 10, 11, 13, 14, 16, 17, 19, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 
    #            41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 60, 61, 63, 64, 500, 503, 505, 506, 507, 508, 509, 512, 514, 
    #            515, 516, 517, 518, 519, 520, 521, 522, 523, 525]
    knife_weapons = [42, 59, 500, 503, 505, 506, 507, 508, 509, 512, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 525]
    try:
        meow.load_font("assets/fonts/ff.ttf", 0)
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
        
        # for i in range(1, 64):
        #     if Engine.test(i) != 0:
        #         print(Engine.test(i))
            
                
        if GetWindowText( u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
            meow.draw_text(text = "HARDSENSE", posX = 5, posY = 5, fontSize = 10, color = meow.get_color("red"))
            meow.draw_fps(50, 50)
            if Engine.get_client_state() == 6:
                try:
                    Local_player = Entity(LocalPlayer.get_local_player())
                    
                    # currentTime = meow.r_float(csgo_proc, csgo_engine + Offset.dwGlobalVars + 0x0010)
                except Exception as err:
                    print('ESP INIT ERROR:', err)
                            
                spectators = []
                for ents in EntityList:
                        
                    try:
                        view_matrix = Engine.get_view_matrix()
                        entity = Entity(ents)
                                    
                        
                        if Local_player.get_health() <= 0:
                            spectators.clear()
                            
                        spectated = Engine.get_entity(entity.get_observed_target_handle() - 1)
                        if spectated == LocalPlayer.get_local_player():
                            spectators.append(entity.get_name)
                            meow.draw_font(
                                fontId = 0,
                                text= '\n'.join(spectators),
                                posX=500,
                                posY=150,
                                fontSize=25,
                                spacing = 2.0,
                                tint = Colors.purple,
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
        # time.sleep(0.000001)

def main():
    try:
        meow.overlay_init(fps=3000, title='test')
        threading.Thread(target=entity_parse, name='entity_parse', daemon=True).start()
        threading.Thread(target=trigger, name='trigger', daemon=True).start()
        # threading.Thread(target=specator_list, name='specator_list', daemon=True).start()
        esp()
        
    except Exception as err:
        print(f'Threads have been canceled! Exiting...\nReason: {err}\nExiting...')
        exit(0)

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
        csgo = meow.open_process(processName="csgo.exe")
        csgo_client = meow.get_module(csgo, "client.dll")["base"]
        csgo_engine = meow.get_module(csgo, "engine.dll")["base"]
        
        csgo2 = Pymem('csgo.exe')
        csgo_client2 = process.module_from_name(csgo2.process_handle, 'client.dll').lpBaseOfDll
        
        ntdll = ctypes.windll.ntdll
        k32 = ctypes.windll.kernel32
        u32 = ctypes.windll.user32
    except Exception as err:
        print(err)
        print('Could not find CS:GO process!\nMake sure the game is running first!')
        exit(0)
        
    main()

    
    