import pyMeow as meow
from engine.process import Process, Windll
from engine.gamedata import Colors, GetWindowText
from utils.entity import Entity, LocalPlayer, Engine
from tools.entity_parse import EntityList, bombAddr, playersInfo
from engine.gui_communication import app_state, state, item_clr

from GUI import *
import keyboard
import time

import os, sys

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def clr(item_clr):
    return meow.new_color(item_clr[0],item_clr[1],item_clr[2],255)

meow.overlay_init(fps=155, title='test')
def esp():
    scoped_weapons = [9, 11, 38, 40]
    knife_weapons = [42, 59, 500, 503, 505, 506, 507, 508, 509, 512, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 525]
    
    try:
        meow.load_font("assets/fonts/ff.ttf", 0)
        meow.load_font("assets/fonts/ff2.ttf", 1)
        C4 = meow.load_texture("assets/images/c4.png")
    except Exception as err:
        print(err)
        exit(0)

    app = App()
    app.iconbitmap(resource_path("assets/icon.ico"))
    active = 0
    
    while meow.overlay_loop():
    
        app.update() # Update menu, but brakes the menu when moving mouse
        app.update_idletasks() # Update menu, but brakes the menu when moving mouse
        
        menu_key = app_state.menu_key
        
        if keyboard.is_pressed(menu_key) and active == 0:
            active = 1
            app.update_idletasks()
            app.state('withdrawn')
            time.sleep(0.5)
        
        if keyboard.is_pressed(menu_key) and active == 1:
            active = 0
            app.update_idletasks()
            app.state('normal')
            app.focus()
            time.sleep(0.5)

        meow.begin_drawing()
        
        get_screen_width_x = meow.get_screen_width()
        get_screen_width_y = meow.get_screen_height()
        
        get_screen_center_x =meow.get_screen_width() // 2
        get_screen_center_y = meow.get_screen_height() // 2
                
        if state.master_switch == 1:                        
            if GetWindowText( Windll.u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
                if Engine.get_client_state() == 6:
                    if state.watermark == 1:
                        meow.draw_text(text = "HARDSENSE", posX = 5, posY = 5, fontSize = 10, color = clr(item_clr.watermark))
                        
                    meow.draw_fps(15, 15)
                    try:
                        local_player = Entity(LocalPlayer.get_local_player())
                        view_matrix = Engine.get_view_matrix()                    
                    except Exception as err:
                        print(err)
                        continue
                    
                    if state.sniper_crosshair_enabled == 1:
                        if local_player != 0:
                            try:
                                local_player_weapon = local_player.getWeapon()
                                for active_scoped_weapons in scoped_weapons:
                                    if local_player_weapon == active_scoped_weapons:
                                        if not local_player.is_scoped():
                                            
                                            meow.draw_line(
                                                startPosX =get_screen_center_x - 5, 
                                                startPosY =get_screen_center_y, 
                                                endPosX =get_screen_center_x + 5, 
                                                endPosY =get_screen_center_y, 
                                                color = clr(item_clr.sniper_crosshair), 
                                                thick = 1.0
                                            )
                                            meow.draw_line(
                                                startPosX =get_screen_center_x, 
                                                startPosY =get_screen_center_y - 5, 
                                                endPosX =get_screen_center_x, 
                                                endPosY =get_screen_center_y + 5, 
                                                color = clr(item_clr.sniper_crosshair), 
                                                thick = 1.0
                                            )
                            except Exception as err:
                                print('AWP CROSSHAIR ERROR:',err)
                                continue
                            
                    if state.recoil_crosshair_enabled == 1:
                        if local_player.get_vec_punch()['x'] != 0.0:
                            player_fov_x = meow.get_screen_width() // 90
                            player_fov_y = meow.get_screen_height() // 90
                            crosshair_x = get_screen_center_x - player_fov_x * local_player.get_vec_punch()["y"]
                            crosshair_y = get_screen_center_y - player_fov_y * -local_player.get_vec_punch()["x"]
                            if local_player.get_shots_fired() > 1:
                                meow.draw_line(
                                    startPosX =crosshair_x - 5, 
                                    startPosY =crosshair_y, 
                                    endPosX =crosshair_x + 5, 
                                    endPosY =crosshair_y, 
                                    color = clr(item_clr.recoil_crosshair), 
                                    thick = 1.0
                                )
                                meow.draw_line(
                                    startPosX =crosshair_x, 
                                    startPosY =crosshair_y - 5, 
                                    endPosX =crosshair_x, 
                                    endPosY =crosshair_y + 5, 
                                    color = clr(item_clr.recoil_crosshair), 
                                    thick = 1.0
                                )
                    
                    spectators = []
                    for ents in EntityList:
                        try:
                            entity = Entity(ents)
                            
                            if state.spectator_enabled == 1:
                                if local_player.get_health() <= 0:
                                    spectators.clear()
                                if entity.get_team() == local_player.get_team():
                                    #Entity will be removed from spectator list only when WH can display it, thats why team check should be used until another method is not found
                                    spectated = Engine.get_entity(entity.get_observed_target_handle() - 1)
                                    if spectated == LocalPlayer.get_local_player():
                                        spectator_name = entity.get_name.decode("utf-8") 
                                        spectators.append(spectator_name)
                                        meow.draw_font(
                                            fontId = 0,
                                            text= '\n'.join(spectators),
                                            posX=get_screen_width_x / 100,
                                            posY=get_screen_width_y / 1.8,
                                            fontSize=25,
                                            spacing = 2.0,
                                            tint = clr(item_clr.spectator_list),
                                        )         
                                    
                            if not entity.get_dormant() and entity.get_health() > 0 and local_player.get_team() != entity.get_team() and ents != local_player:
                                entity_w2s = meow.world_to_screen(view_matrix, entity.get_position(), 1)
                                head_pos = meow.world_to_screen(view_matrix, entity.get_bone_position(8), 1)

                                head = entity_w2s['y'] - head_pos['y'] 
                                width = head / 2
                                center = width / 2
                                
                                if state.players_box_enabled == 1:
                                    if state.players_box_type == 'normal':
                                        meow.draw_rectangle_lines(
                                            posX=head_pos['x'] - center,
                                            posY=head_pos['y'] - center / 2,
                                            width=width * 1.0,
                                            height=head + center / 2,
                                            color=clr(item_clr.box_esp),
                                            lineThick=1.1,
                                        )
                                    elif state.players_box_type == 'filled':
                                        meow.draw_rectangle(
                                            posX=head_pos["x"] - center,
                                            posY=head_pos["y"] - center / 2,
                                            width=width,
                                            height=head + center / 2,
                                            color=clr(item_clr.box_esp),
                                        )
                                        
                                if state.players_head_enabled == 1:
                                    if state.players_head_type == 'circle':
                                        meow.draw_circle(
                                            centerX = head_pos['x'],
                                            centerY = head_pos['y'],
                                            radius = 3,
                                            color = clr(item_clr.head_esp),
                                        )
                                
                                if state.players_health_enabled == 1:
                                    meow.gui_progress_bar(
                                        posX=head_pos["x"] - center,
                                        posY=entity_w2s["y"],
                                        width=width,
                                        height=10,
                                        textLeft="HP: ",
                                        textRight=f" {entity.get_health()}",
                                        value=entity.get_health(),
                                        minValue=0,
                                        maxValue=100,
                                    )
                                    
                                if state.players_names_enabled == 1:
                                    meow.draw_text(
                                        text= entity.get_name,
                                        posX=head_pos["x"] - center - 10,
                                        posY=head_pos["y"] - center - 5,
                                        fontSize=5,
                                        color=clr(item_clr.name_esp),
                                    )
                                
                                if state.players_weapon == 1:
                                    get_entity_weapon = entity.getWeapon()

                                    if get_entity_weapon in knife_weapons:
                                        meow.draw_texture(texture = meow.load_texture(resource_path("assets/images/knife.png")), posX = head_pos["x"] - center / 1.1, posY = entity_w2s["y"] * 1.02, rotation = 0, scale = 0.3,tint = clr(item_clr.weapon_esp))
                                    
                                    for i in range(1,64):
                                        if get_entity_weapon == i:
                                            meow.draw_texture(texture = meow.load_texture(resource_path(f"assets/images/{i}.png")), posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.02, rotation = 0, scale = 0.3,tint = clr(item_clr.weapon_esp))
                                            # meow.draw_texture(texture = meow.load_texture(f"assets/images/{i}.png"), posX = head_pos["x"] / 1.005, posY = entity_w2s["y"] * 1.02, rotation = 0, scale = 0.3, tint = clr(item_clr.weapon_esp))
                                        
                        except Exception as err:
                            if not "out of" in repr(err):
                                print(err)
                            continue
                    if state.bomb_info_enabled == 1:
                        for bomb_index in bombAddr:
                            try:
                                bomb_entity = Entity(bomb_index)
                                bomb_time = Engine.get_bomb_time(bomb_index)
                                defuse_time = Engine.get_defuse_time(bomb_index)
                                                        
                                bomb_site = ''
                                
                                if Engine.get_bomb_site(bomb_index) == 0: bomb_site = 'A:'
                                if Engine.get_bomb_site(bomb_index) == 1: bomb_site = 'B:'
                                if defuse_time > bomb_time:
                                    defuse_color = Colors.red
                                else:
                                    defuse_color = Colors.green
                                
                                if bomb_time > 10: bomb_time_text = f"{bomb_time:.3}"
                                elif bomb_time < 10: bomb_time_text = f"{bomb_time:.2}"
                                                        
                                if Engine.get_bomb_ticking(bomb_index) and bomb_time > 0.1:
                                    
                                    meow.draw_text(
                                        text=str(bomb_site),
                                        posX=get_screen_width_x / 100,
                                        posY=get_screen_width_y / 1.5 ,
                                        fontSize=25,
                                        color=Colors.white,
                                    )
                                    
                                    meow.draw_text(
                                        text=bomb_time_text,
                                        posX=get_screen_width_x / 100 + 25,
                                        posY=get_screen_width_y / 1.5,
                                        fontSize=25,
                                        color=Colors.orange,
                                    )
                                    
                                    if Engine.is_defusing_bomb(bomb_index) > 0 and Engine.is_defusing_bomb(bomb_index) < 64:
                                        meow.draw_text(
                                            text= f"{defuse_time:.2}",
                                            posX=get_screen_width_x / 100,
                                            posY=(get_screen_width_y / 1.5) * 1.05,
                                            fontSize=25,
                                            color=defuse_color,
                                        )
                                        
                                    bomb_w2s_pos = meow.world_to_screen(view_matrix, bomb_entity.get_position(), 1)
                                    meow.draw_texture(texture = C4, posX = bomb_w2s_pos["x"], posY = bomb_w2s_pos["y"], rotation = 0, scale = 0.6,tint = Colors.white)
                                    
                            except Exception as err:
                                if not "out of" in repr(err):
                                    print(err)
                                continue
        meow.end_drawing()  
        # app.mainloop()        