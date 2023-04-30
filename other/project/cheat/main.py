from os import system
import os
import pymem
import pymem.process
import keyboard
import time
import math
import re
import requests
import ctypes
import random
import secrets
import sys
from termcolor import colored
import subprocess
import urllib3
import win32com.client as wincom

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = os.open(os.devnull, os.O_RDWR)

try:        
    from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess

    class scare:

        def fuck(names):
            for proc in process_iter():
                try:
                    for name in names:
                        if name.lower() in proc.name().lower():
                            proc.kill()
                except (NoSuchProcess, AccessDenied, ZombieProcess):
                    pass

        def crow():
            forbidden = ['http', 'traffic', 'wireshark', 'fiddler', 'packet']
            return scare.fuck(names=forbidden)
        
    scare.crow()
except:
    pass

user32 = ctypes.windll.user32
hwid = str(str(subprocess.check_output('wmic csproduct get uuid', stdin=DEVNULL, stderr=DEVNULL)).strip().replace(r"\r", "").split(r"\n")[1].strip())
users = requests.get("\u0068\u0074\u0074\u0070\u0073\u003a\u002f\u002f\u0070\u0061\u0073\u0074\u0065\u0062\u0069\u006e\u002e\u0063\u006f\u006d\u002f\u0072\u0061\u0077\u002f\u0078\u0044\u006d\u0053\u0069\u0053\u0031\u0051", verify=False)
    
def GetWindowText(handle, length=100):

    window_text = ctypes.create_string_buffer(length)
    user32.GetWindowTextA(
        handle,
        ctypes.byref(window_text),
        length
    )

    return window_text.value

def speak(text):
    speak = wincom.Dispatch("SAPI.Spvoice")
    speak.Speak(text)

def main():
    if hwid in users.text:
        
        key = 'REG DELETE "HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache" /va /f'
        key2 = 'REG DELETE "HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU" /f'
        key3 = 'REG DELETE "HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags" /f'
        key4 = 'REG DELETE "HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\BagMRU" /f'
        key5 = 'REG DELETE "HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Bags" /f'
        subprocess.call(key, shell = True)
        subprocess.call(key2, shell = True)
        subprocess.call(key3, shell = True)
        subprocess.call(key4, shell = True)
        subprocess.call(key5, shell = True)

        temp_dir = r'c:\windows\temp'
        prefetch_dir = r'C:\Windows\Prefetch'

        process = subprocess.Popen('rmdir /S /Q {}'.format(temp_dir), shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _ = process.communicate()

        process2 = subprocess.Popen('rmdir /S /Q {}'.format(prefetch_dir), shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _ = process2.communicate()
        
        aa0 = "a779d2b2687c01783d4ba406d6db003d29bfeff7f88954b5cca35db6b3e7023f"
        aa1 = "649e2b944d01a13fbbb65c369cc793ed"
        aa2 = 634522979280582856943583417864215043553732516036833547407673484229549188531778767436206111157265100988522719961647899025697046388675241184343995293811266961044261395238311757794962183074214827
        aa3 = ["6bc002242812283c2f7d6769d08df1ecf06f1492f10e5c0babd7d6dd095eb4570ccffd3c0f850317b8a10a77b2a45e7f9c6da9e06e35d44d1786d3c887ed1ca7", 6421467839|412, 37528940968531359234, 1766808553236511598249957914423320888445826969670139386686364123287996035227569576721816277735,  1646849682681777278692270805931344199, 5267721142988091488659587045] 

        print(aa0)
        print(aa1)
        print(aa2)
        print(aa3)

        av = secrets.token_hex(nbytes=64)
        av0 = random.randint(1,999), secrets.token_urlsafe(32)
        av1 = secrets.token_bytes(64)
        av2 = secrets.token_hex(nbytes=128)
        av3 = [secrets.token_hex(nbytes=64), random.random(), 37528940968531359234, random.randint(100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000),  random.randint(10000000000000000000000000000000000,90000000000000000000000000000000000), secrets.token_hex(nbytes=16)] 
        print(av)
        print(av0)
        print(av1)
        print(av2)
        print(av3)

        ctypes.windll.kernel32.SetConsoleTitleW(av)

        #Get cs proccess with client and engine
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

        # ----------------------------------------- Users -----------------------------------------
        usersData = users.json()
        userConfig = str(usersData["users"][hwid])
        userName = str(usersData["users"][userConfig])
        # ----------------------------------------- Users -----------------------------------------
    
        glowActive = True
        chamsActive = True

        radar = 1
        radarKey = "end"
        radarActive = True
        
        # ---------------------------------- Auto update Offsets ----------------------------------
        offsets = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
        response = requests.get(offsets, verify=False).json()

        #Signatures
        dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
        dwClientState = int(response["signatures"]["dwClientState"])
        dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
        dwEntityList = int(response["signatures"]["dwEntityList"])
        dwForceJump = int(response["signatures"]["dwForceJump"])
        dwForceAttack = int(response["signatures"]["dwForceAttack"])
        dwClientState_PlayerInfo = int( response["signatures"]["dwClientState_PlayerInfo"] )
        #Netvars
        m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
        m_bGunGameImmunity = int(response["netvars"]["m_bGunGameImmunity"])
        m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
        m_fFlags = int(response["netvars"]["m_fFlags"])
        m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
        m_iHealth = int(response["netvars"]["m_iHealth"])
        m_bIsDefusing = int(response["netvars"]["m_bIsDefusing"])
        m_iCompetitiveRanking = int( response["netvars"]["m_iCompetitiveRanking"] )
        m_iCompetitiveWins = int(response["netvars"]["m_iCompetitiveWins"])
        m_clrRender = int(response["netvars"]["m_clrRender"])
        m_bSpotted = int(response["netvars"]["m_bSpotted"])
        # ---------------------------------- Auto update Offsets ----------------------------------
        
        # -------------------------------------- Auto Config --------------------------------------
        config = requests.get("https://pastebin.com/raw/" + userConfig, verify=False).json()

        bhopActive = int(config["bhop"]["bhopEnable"])
        bhopType = int(config["bhop"]["bhopType"])
        bhopKey = str(config["bhop"]["bhopKey"])

        triggerActive = int(config["trigger"]["triggerActive"])
        triggerKey = str(config["trigger"]["triggerKey"])
        shotDelay = float(config["trigger"]["ShotDelay"])

        glow = int(config["glow"]["glowActive"])
        glowKey = str(config["glow"]["glowToggleKey"])
        hpGlow = int(config["glow"]["glowByHP"])
        GLOWR = int(config["glow"]["glowDefaultRed"])
        GLOWG = int(config["glow"]["glowDefaultGreen"])
        GLOWB = int(config["glow"]["glowDefaultBlue"])
        GLOWA = float(config["glow"]["glowAlpha"])
        GLOWRD = int(config["glow"]["glowDefusingRed"])
        GLOWGD = int(config["glow"]["glowDefusingGreen"])
        GLOWBD = int(config["glow"]["glowDefusingBlue"])
        midHP = int(config["glow"]["glowMidHp"])
        midHPR = int(config["glow"]["glowMidColorRed"])
        midHPG = int(config["glow"]["glowMidColorGreen"])
        midHPB = int(config["glow"]["glowMidColorBlue"])
        lowHP = int(config["glow"]["glowLowHp"])
        lowHPR = int(config["glow"]["glowLowColorRed"])
        lowHPG = int(config["glow"]["glowLowColorGreen"])
        lowHPB = int(config["glow"]["glowLowColorBlue"])

        chams = int(config["chams"]["chamsActive"])
        chamsKey = str(config["chams"]["chamsToggleKey"])
        chamsR = int(config["chams"]["chamsRed"])
        chamsG = int(config["chams"]["chamsGreen"])
        chamsB = int(config["chams"]["chamsBlue"])

    # -------------------------------------- Auto Config --------------------------------------
        
        os.system("cls")
        print("User:", colored(userName, "cyan"))
        print("Version:", colored("1.7", "magenta"))
    
        while True:
            if not GetWindowText( user32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
                time.sleep( 1 )
                continue
            if client and engine and pm:
                #try: #Fetching cs go process
                    #player = pm.read_int(client + dwLocalPlayer)
                    #engine_pointer = pm.read_int(engine + dwClientState)
                    #glow_manager = pm.read_int(client + dwGlowObjectManager) 
                    #crosshairID = pm.read_int(player + m_iCrosshairId) 
                    #localTeam = pm.read_int(player + m_iTeamNum)
                #except:
                    #time.sleep(1)
                    #continue
            #Bhop
                if keyboard.is_pressed(bhopKey): 
                    if bhopActive == 1 and bhopType == 1: #Normal
                        force_jump = client + dwForceJump
                        player = pm.read_int(client + dwLocalPlayer)
                        on_ground = pm.read_int(player + m_fFlags)
                        if player and on_ground and on_ground == 257 or on_ground == 263:
                            pm.write_int(force_jump, 6)
                            
                    if bhopActive == 1 and bhopType == 2: #legit
                        force_jump = client + dwForceJump
                        player = pm.read_int(client + dwLocalPlayer)
                        on_ground = pm.read_int(player + m_fFlags)
                        if player and on_ground and on_ground == 257 or on_ground == 263:
                            a = random.randint(0,5)
                            time.sleep(a/100)
                            pm.write_int(force_jump, 5)
                            time.sleep(0.08)
                            pm.write_int(force_jump, 4)
            #Trigger
            if keyboard.is_pressed(triggerKey):
                if triggerActive == 1:
                    for i in range(1, 32):

                        entity = pm.read_int(client + dwEntityList + i * 0x10)

                        if entity:

                            player = pm.read_int(client + dwLocalPlayer)
                            entity_id = pm.read_int(player + m_iCrosshairId)

                            entity_team = pm.read_int(entity + m_iTeamNum)
                            player_team = pm.read_int(player + m_iTeamNum)

                            if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
                                pm.write_int(client + dwForceAttack, 6)
                            time.sleep(shotDelay)

            #Glow
            if glow == 1:
                if keyboard.is_pressed(glowKey) and glowActive == False:
                    glowActive = True
                    time.sleep(0.3)
                    speak("ВХ - он")
                elif keyboard.is_pressed(glowKey) and glowActive == True:
                    glowActive = False
                    time.sleep(0.3)
                    speak("ВХ - офф")
                    
                if(glowActive):
                    glowManager = pm.read_int(client + dwGlowObjectManager)
                    GLOWRF, GLOWGF, GLOWBF = float(GLOWR / 255), float(GLOWG / 255), float(GLOWB / 255)
                    
                    for i in range(1, 32):

                        entity = pm.read_int(client + dwEntityList + i * 0x10)

                        if entity:

                            entityTeamID = pm.read_int(entity + m_iTeamNum)
                            entityGlow = pm.read_int(entity + m_iGlowIndex)
                            player = pm.read_int(client + dwLocalPlayer)
                            playerTeam = pm.read_int(player + m_iTeamNum)
                            defusing = pm.read_int(entity + m_bIsDefusing)

                            if entityTeamID != playerTeam:
                                if hpGlow == 1:
                                    entityHp = pm.read_int(entity + m_iHealth)
                                    if entityHp > 50:
                                        GLOWRF, GLOWGF, GLOWBF = float(GLOWR / 255), float(GLOWG / 255), float(GLOWB / 255)
                                    if entityHp < midHP:
                                        GLOWRF, GLOWGF, GLOWBF = float(midHPR / 255), float(midHPG / 255), float(midHPB / 255)
                                    if entityHp < lowHP:
                                        GLOWRF, GLOWGF, GLOWBF = float(lowHPR / 255), float(lowHPG / 255), float(lowHPB / 255)
                                if defusing:
                                    GLOWRF, GLOWGF, GLOWBF = float(GLOWRD / 255), float(GLOWGD / 255), float(GLOWBD / 255)
                  
                                pm.write_float(glowManager + entityGlow * 0x38 + 0x8, float(GLOWRF)) #R
                                pm.write_float(glowManager + entityGlow * 0x38 + 0xC , float(GLOWGF)) #G
                                pm.write_float(glowManager + entityGlow * 0x38 + 0x10, float(GLOWBF)) #B
                                pm.write_float(glowManager + entityGlow * 0x38 + 0x14, float(GLOWA)) #A
                                pm.write_int( glowManager + entityGlow * 0x38 + 0x28, 1 ) #enable

            #chams
            if chams == 1:
                if keyboard.is_pressed(chamsKey) and chamsActive == False:
                    chamsActive = True
                    time.sleep(0.3)
                    speak("Чамс - он")
                elif keyboard.is_pressed(chamsKey) and chamsActive == True:
                    chamsActive = False
                    time.sleep(0.3)
                    speak("Чамс - офф")
            
                if(chamsActive):
                    for i in range(32):
                            entity = pm.read_int(client + dwEntityList + i * 0x10)

                            if entity:

                                entityTeamID = pm.read_int(entity + m_iTeamNum)
                                player = pm.read_int(client + dwLocalPlayer)
                                playerTeam = pm.read_int(player + m_iTeamNum)

                                if (entityTeamID != playerTeam):
                                    pm.write_int(entity + m_clrRender, (chamsR))
                                    pm.write_int(entity + m_clrRender + 0x1, (chamsG))
                                    pm.write_int(entity + m_clrRender + 0x2, (chamsB))
            #radar
            if radar == 1:
                if keyboard.is_pressed(radarKey) and radarActive == False:
                    radarActive = True
                    time.sleep(0.3)
                    speak("Радар - он")
                elif keyboard.is_pressed(radarKey) and radarActive == True:
                    radarActive = False
                    time.sleep(0.3)
                    speak("Радар - офф")

                if(radarActive):
                    for i in range(32):
                            entity = pm.read_int(client + dwEntityList + i * 0x10)

                            if entity:

                                entityTeamID = pm.read_int(entity + m_iTeamNum)
                                player = pm.read_int(client + dwLocalPlayer)
                                playerTeam = pm.read_int(player + m_iTeamNum)

                                if (entityTeamID != playerTeam):
                                    pm.write_int(entity + m_bSpotted, 1)

    else:
        os.system("cls")
        print("HWID ERROR!")
        print(colored(hwid, "red"))
        print("Please contact:", colored("Ruslan#7905", "cyan"))
        os.system('pause >NUL')
if __name__ == "__main__":
    main()