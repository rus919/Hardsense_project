from engine.process import Process, Windll
from engine.gamedata import GetWindowText
from utils.entity import Entity, LocalPlayer, Engine
from engine.gui_communication import trigger_state

def trigger():
    while True:
        if GetWindowText( Windll.u32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
            if Engine.get_client_state() == 6:
                if trigger_state.enabled == 1:
                    try:
                        local_player = Entity(LocalPlayer.get_local_player())
                    except Exception as err:
                        print(err)
                        continue
                    if Windll.u32.GetAsyncKeyState(trigger_state.trigger_key):
                        try:
                            entity_id = LocalPlayer.get_crosshair_id()
                            if entity_id == 0:
                                continue
                            entity = Entity(Engine.get_entity(entity_id - 1))
                            if local_player.get_team() != entity.get_team() and entity.get_health() > 0:
                                Windll.k32.Sleep(10)
                                Windll.u32.mouse_event(0x0002, 0, 0, 0, 0)
                                Windll.k32.Sleep(25)
                                Windll.u32.mouse_event(0x0004, 0, 0, 0, 0)
                                Windll.k32.Sleep(250)
                        except Exception as err:
                            print(err)
                            continue
        Windll.k32.Sleep(1)