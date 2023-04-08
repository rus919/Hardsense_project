import pyMeow as meow
from engine.process import Process, Windll
from utils.entity import Entity, LocalPlayer, Engine
from utils.offsets import Offset

try:
    csgo = Process('csgo.exe')
    csgo_client = csgo.get_module("client.dll")
    csgo_engine = csgo.get_module("engine.dll")
except Exception as err:
    print(err)
    exit(0)

EntityList = []
bombAddr = []
playersInfo = []
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
        
def getPlayerInfo(): # Not returning properly, missing player data when in entity he is there
    if Engine.get_client_state() == 6:
        try:
            playersInfo.clear()
            for i in range(1, 64):     
                entity = Engine.get_entity(i)
                if entity != 0:
                    playerSteamID = Entity.get_player_steam_id(i).decode('utf-8') # Getting steamID32
                    if playerSteamID != 'BOT':
                        id_split = playerSteamID.split(":") #Convert steamID32 to array
                        steam64id = 76561197960265728 #Base for adding
                        steam64id += int(id_split[2]) * 2 #Take the player ID in [2] and *2 then add to steam64id, if steamID32 [1] contains 1 then add +1 = steamID64
                        if id_split[1] == "1":
                            steam64id += 1
                    else:
                        steam64id = 'BOT'
                                        
                    ents = Entity(entity)
                    
                    ent_name = ents.get_name.decode('utf-8', errors="ignore")
                                        
                    entityCompRank = csgo.read_i32(Engine.get_player_resources() + Offset.m_iCompetitiveRanking + (i+1) * 4)
                    entityCompWins = csgo.read_i32(Engine.get_player_resources() + Offset.m_iCompetitiveWins + (i+1) * 4)
                    

                    if [i, ent_name, ents.get_team(), entityCompRank, entityCompWins, steam64id] not in playersInfo:
                        playersInfo.append([i, ent_name , ents.get_team(), entityCompRank, entityCompWins, steam64id])
                    # print(steam64id)
        except Exception as err:
            print('PLAYERS INFO ERROR: ', err)
            pass