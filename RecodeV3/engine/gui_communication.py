import pyMeow as meow

class state:
    master_switch = 0
    watermark = 0
    players_box_enabled = 0
    players_box_type = ''
    players_head_enabled = 0
    players_head_type = ''
    players_health_enabled = 0
    players_health_type = ''
    players_names_enabled = 0
    players_weapon = 0
    players_weapon_type = ''
    spectator_enabled = 0
    bomb_info_enabled = 0
    sniper_crosshair_enabled = 0
    recoil_crosshair_enabled = 0
    
class item_clr:
    watermark = [255,255,255,255]
    box_esp = [255,255,255,255]
    head_esp = [255,255,255,255]
    health_esp = [255,255,255,255]
    name_esp = [255,255,255,255]
    weapon_esp = [255,255,255,255]
    
class menu_clr:
    None