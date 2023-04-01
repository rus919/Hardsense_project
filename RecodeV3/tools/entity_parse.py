import pyMeow as meow
from engine.process import Process, Windll
from utils.entity import Entity, LocalPlayer, Engine

try:
    csgo = Process('csgo.exe')
    csgo_client = csgo.get_module("client.dll")
    csgo_engine = csgo.get_module("engine.dll")
except Exception as err:
    print(err)
    exit(0)

EntityList = []
bombAddr = []
def entity_parse():
    while True:
        if Engine.get_client_state() == 6:
            try:
                EntityList.clear()
                
                for i in range(1, 512):
                    entity = Engine.get_entity(i)
                    if entity != 0:
                        ents = Entity(entity)
                        client_networkable = csgo.read_i32(entity + 0x8)
                        dwGetClientClassFn = csgo.read_i32(client_networkable + 0x8)
                        entity_client_class = csgo.read_i32(dwGetClientClassFn+ 0x1)
                        class_id = csgo.read_i32(entity_client_class + 0x14)

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
        # print(bombAddr)
        Windll.k32.Sleep(2000)       