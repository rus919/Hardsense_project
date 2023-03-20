import pyMeow as meow
from engine.process import Process, Windll
from engine.gamedata import Colors, GetWindowText
from utils.entity import Entity, LocalPlayer, Engine
from tools.entity_parse import EntityList

def esp():
    while meow.overlay_loop():
        
        meow.begin_drawing()
        
        if GetWindowText( Windll.u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
            if Engine.get_client_state() == 6:
                meow.draw_text(text = "HARDSENSE", posX = 5, posY = 5, fontSize = 10, color = meow.get_color("red"))
                meow.draw_fps(50, 50)
                
                try:
                    local_player = Entity(LocalPlayer.get_local_player())
                    view_matrix = Engine.get_view_matrix()                    
                except Exception as err:
                    print(err)
                    continue
                
                for ents in EntityList:
                    try:
                        entity = Entity(ents)                        
                        if not entity.get_dormant() and entity.get_health() > 0 and local_player.get_team() != entity.get_team() and ents != local_player:
                            entity_w2s = meow.world_to_screen(view_matrix, entity.get_position(), 1)
                            head_pos = meow.world_to_screen(view_matrix, entity.get_bone_position(8), 1)

                            head = entity_w2s["y"] - head_pos["y"]
                            width = head / 2
                            center = width / 2
                            
                            # meow.draw_rectangle_lines(
                            #     posX=head_pos['x'] - center * 1.0,
                            #     posY=head_pos['y'] - center / 2,
                            #     width=width * 1.0,
                            #     height=head + center / 2,
                            #     color=Colors.black,
                            #     lineThick=1.0,
                            # )
                            
                            meow.draw_circle(
                                centerX = head_pos["x"],
                                centerY = head_pos["y"],
                                radius = 3,
                                color = meow.get_color("red"),
                            )
                            
                    except Exception as err:
                        if not "out of" in repr(err):
                            print(err)
                        continue
        
        meow.end_drawing()        