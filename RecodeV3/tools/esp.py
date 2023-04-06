import pyMeow as meow
from engine.process import Process, Windll
from engine.gamedata import Colors, GetWindowText
from utils.entity import Entity, LocalPlayer, Engine
from tools.entity_parse import EntityList, bombAddr

from engine.state import state

def esp():
    scoped_weapons = [9, 11, 38, 40]
    try:
        meow.load_font("assets/fonts/ff.ttf", 0)
        meow.load_font("assets/fonts/ff2.ttf", 1)
        C4 = meow.load_texture("assets/images/c4.png")
    except Exception as err:
        print(err)
        exit(0)
    
    while meow.overlay_loop():
        
        meow.begin_drawing()
        
        get_screen_width_x = meow.get_screen_width()
        get_screen_width_y = meow.get_screen_height()
        
        get_screen_center_x =meow.get_screen_width() // 2
        get_screen_center_y = meow.get_screen_height() // 2
                                
        if GetWindowText( Windll.u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
            if Engine.get_client_state() == 6 and state.master_switch == 1:
                # meow.draw_text(text = "HARDSENSE", posX = 5, posY = 5, fontSize = 10, color = meow.get_color("red"))
                meow.draw_fps(5, 5)
                
                try:
                    local_player = Entity(LocalPlayer.get_local_player())
                    view_matrix = Engine.get_view_matrix()                    
                except Exception as err:
                    print(err)
                    continue
                
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
                    except Exception as err:
                        print('AWP CROSSHAIR ERROR:',err)
                        continue
                    
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
                
                spectators = []
                for ents in EntityList:
                    try:
                        entity = Entity(ents)
                        
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
                                    tint = Colors.white,
                                )         
                                
                        if not entity.get_dormant() and entity.get_health() > 0 and local_player.get_team() != entity.get_team() and ents != local_player:
                            entity_w2s = meow.world_to_screen(view_matrix, entity.get_position(), 1)
                            head_pos = meow.world_to_screen(view_matrix, entity.get_bone_position(8), 1)

                            head = entity_w2s['y'] - head_pos['y'] 
                            width = head / 2
                            center = width / 2
                            
                            if state.players_box == 1:
                                meow.draw_rectangle_lines(
                                    posX=head_pos['x'] - center,
                                    posY=head_pos['y'] - center / 2,
                                    width=width * 1.0,
                                    height=head + center / 2,
                                    color=Colors.black,
                                    lineThick=1.0,
                                )
                            
                            if state.head_esp == 1:
                                meow.draw_circle(
                                    centerX = head_pos['x'],
                                    centerY = head_pos['y'],
                                    radius = 3,
                                    color = meow.get_color("red"),
                                )
                            
                            meow.draw_text(
                                text= entity.get_name.decode('utf-8'),
                                posX=head_pos["x"] - center - 10,
                                posY=head_pos["y"] - center - 5,
                                fontSize=5,
                                color=Colors.white,
                            )
                            
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
                            
                    except Exception as err:
                        if not "out of" in repr(err):
                            print(err)
                        continue
        
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