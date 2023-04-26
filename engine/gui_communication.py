from dataclasses import dataclass

class app_state:
    menu_key = 'f1'
    overlay_fps = 155
    
class trigger_state:
    enabled = 0
    trigger_key = 0
    advanced = 0

class state:
    master_switch = 0
    watermark = 0
    show_fps = 0
    players_box_enabled = 0
    players_box_type = ''
    players_head_enabled = 0
    players_head_type = ''
    players_health_enabled = 0
    players_health_type = ''
    players_names_enabled = 0
    players_weapon = 0
    players_weapon_type = ''
    sniper_crosshair_enabled = 0
    sniper_crosshair_type = ''
    recoil_crosshair_enabled = 0
    recoil_crosshair_type = ''
    spectator_enabled = 0
    bomb_info_enabled = 0
    
class item_clr:
    watermark = [255,255,255,255]
    box_esp = [255,255,255,255]
    head_esp = [255,255,255,255]
    health_esp = [255,255,255,255]
    name_esp = [255,255,255,255]
    weapon_esp = [255,255,255,255]
    sniper_crosshair = [255,255,255,255]
    recoil_crosshair = [255,255,255,255]
    spectator_list = [255,255,255,255]
    
class menu_clr:
    None

@dataclass
class Weapon:
    trigger_delay_before_shot: int = 5
    trigger_delay_between_shot: int = 25
    trigger_delay_after_shot: int = 150

class glock(Weapon):
    pass
class usp_s(Weapon):
    pass
class p2000(Weapon):
    pass
class dual_berettas(Weapon):
    pass
class p250(Weapon):
    pass
class five_seven(Weapon):
    pass
class tec_9(Weapon):
    pass
class cz75(Weapon):
    pass
class deagle(Weapon):
    pass
class nova(Weapon):
    pass
class xm1014(Weapon):
    pass
class mag_7(Weapon):
    pass
class sawed_off(Weapon):
    pass
class mp9(Weapon):
    pass
class mac_10(Weapon):
    pass
class mp5(Weapon):
    pass
class mp7(Weapon):
    pass
class ump(Weapon):
    pass
class p90(Weapon):
    pass
class bizon(Weapon):
    pass
class m249(Weapon):
    pass
class negev(Weapon):
    pass
class famas(Weapon):
    pass
class galil(Weapon):
    pass
class m4a4(Weapon):
    pass
class m4a1_s(Weapon):
    pass
class ak_47(Weapon):
    pass
class ssg(Weapon):
    pass
class sg553(Weapon):
    pass
class aug(Weapon):
    pass
class awp(Weapon):
    pass
class scar(Weapon):
    pass
class g3sg1(Weapon):
    pass