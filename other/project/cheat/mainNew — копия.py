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
from ctypes import *
import random
import secrets
import sys
from termcolor import colored
import subprocess
import urllib3
from win32api import GetAsyncKeyState
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess

#import win32com
#import win32com.client as wincom
#import pyttsx3
#from pyttsx3.drivers import sapi5

#engine1 = pyttsx3.init()

#engine1.say("привет - мир")

#engine1.runAndWait()

urllib3.disable_warnings()

u32 = windll.user32

try:
	from subprocess import DEVNULL
except ImportError:
	DEVNULL = os.open(os.devnull, os.O_RDWR)

try:        
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
k32 = windll.kernel32
ntdll = windll.ntdll
hwid = str(str(subprocess.check_output('wmic csproduct get uuid', stdin=DEVNULL, stderr=DEVNULL)).strip().replace(r"\r", "").split(r"\n")[1].strip())
users = requests.get("\u0068\u0074\u0074\u0070\u0073\u003a\u002f\u002f\u0070\u0061\u0073\u0074\u0065\u0062\u0069\u006e\u002e\u0063\u006f\u006d\u002f\u0072\u0061\u0077\u002f\u0078\u0044\u006d\u0053\u0069\u0053\u0031\u0051", verify=False)

try:
	pm = pymem.Pymem("csgo.exe")
	client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
	engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
except:
	print("Для начала вам нужно запустить CS:GO!")
	time.sleep(10)
	exit()

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
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
dwClientState_GetLocalPlayer = int( response["signatures"]["dwClientState_GetLocalPlayer"] )
dwClientState_MaxPlayer = int( response["signatures"]["dwClientState_MaxPlayer"] )
dwClientState_State = int( response["signatures"]["dwClientState_State"] )
m_bDormant = int(response["signatures"]["m_bDormant"])
#dwClientState_PlayerInfo = int(response["signatures"]["dwClientState_PlayerInfo"])
#dwPlayerResource = int(response["signatures"]["dwPlayerResource"])

#Netvars
m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_fFlags = int(response["netvars"]["m_fFlags"])
m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
m_iHealth = int(response["netvars"]["m_iHealth"])
m_bIsDefusing = int(response["netvars"]["m_bIsDefusing"])
m_clrRender = int(response["netvars"]["m_clrRender"])
m_bSpotted = int(response["netvars"]["m_bSpotted"])
m_iShotsFired = int(response["netvars"]["m_iShotsFired"])
m_aimPunchAngle = int(response["netvars"]["m_aimPunchAngle"])
#m_iCompetitiveRanking = int(response["netvars"]["m_iCompetitiveRanking"])
#m_iCompetitiveWins = int(response["netvars"]["m_iCompetitiveWins"])
m_nTickBase = int(response["netvars"]["m_nTickBase"])
m_lifeState = int(response["netvars"]["m_lifeState"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
m_Local = int(response["netvars"]["m_Local"])
m_nForceBone = int(response["netvars"]["m_Local"])
# ---------------------------------- Auto update Offsets ----------------------------------

def GetWindowText(handle, length=100):

	window_text = ctypes.create_string_buffer(length)
	user32.GetWindowTextA(
		handle,
		ctypes.byref(window_text),
		length
	)

	return window_text.value

#def speak(text):
	#speak = wincom.Dispatch("SAPI.Spvoice")
	#speak.Speak(text)



class Vector3(Structure):
	_fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]

def getUsers():
	global userConfig, userName
	usersData = users.json()
	userConfig = str(usersData["users"][hwid])
	userName = str(usersData["users"][userConfig])

def av():
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

def autoConfig():
	global bhopActive, bhopType, bhopKey
	global triggerActive, triggerKey, shotDelay
	global glow, glowKey, hpGlow, GLOWR, GLOWG, GLOWB, GLOWA, GLOWRD, GLOWGD, GLOWBD, midHP, midHPR, midHPG, midHPB, lowHP, lowHPR, lowHPG, lowHPB
	global chams, chamsKey, chamsR, chamsG, chamsB
	global radar, radarKey
	global rcs, rcsKey
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

	radar = int(config["radar"]["radarActive"])
	radarKey = str(config["radar"]["radarToggleKey"])
	
	rcs = int(config["rcs"]["rcsActive"])
	rcsKey = str(config["rcs"]["rcsToggleKey"])

def console():
	os.system("cls")
	print("User:", colored(userName, "cyan"))
	print("Version:", colored("1.8 BETA", "magenta"))
	#print("Expiry date:", colored("06.01.22", "green"))

def main():
	if hwid in users.text:
		av()
		getUsers()
		autoConfig()
		console()

		glowActive = True
		chamsActive = True
		radarActive = True
		g_oldpunchx = 0.0
		g_oldpunchy = 0.0
		rcsActive = True
		
		global g_aimbot_fov, g_aimbot_head, g_aimbot_smooth, g_current_tick, g_previous_tick, g_aimbot_rcs

		g_current_tick = 0.0
		g_previous_tick = 0.0

		g_aimbot_fov = 10.5 / 180.0
		g_aimbot_head = True
		g_aimbot_smooth = 5.5
		g_aimbot_rcs = True
			
		while True:
				if not GetWindowText( user32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
					time.sleep( 1 )
					continue
				if client and engine and pm:
					try:
						player = pm.read_int(client + dwLocalPlayer)
						on_ground = pm.read_int(player + m_fFlags)
						crosshairID = pm.read_int(player + m_iCrosshairId)
						getcrosshairTarget = pm.read_uint( client + dwEntityList + (crosshairID - 1) * 0x10 )
						crosshairTeam = pm.read_uint( getcrosshairTarget + m_iTeamNum )
						playerTeam = pm.read_int(player + m_iTeamNum)
						glowManager = pm.read_int(client + dwGlowObjectManager)
						engine_pointer = pm.read_uint( engine + dwClientState )
						maxClients = pm.read_uint(engine_pointer + dwClientState_MaxPlayer)
						#fl_sensitivity = _sensitivity.get_float()
						#view_angle = Engine.get_view_angles()
						view_anglex = pm.read_float(engine_pointer + dwClientState_ViewAngles)
						#self = Entity.get_client_entity(Engine.get_local_player())

					except:
						#print( "[TEST] Ошибка - Раунд не начался" )
						time.sleep( 5 )
						continue

				for i in range(1, maxClients):
					entity = pm.read_uint( client + dwEntityList + i * 0x10 )

					if entity:
						try:
							entityGlow = pm.read_int(entity + m_iGlowIndex)
							entityTeamID = pm.read_int(entity + m_iTeamNum)
							defusing = pm.read_int(entity + m_bIsDefusing)
							entityHp = pm.read_int(entity + m_iHealth)
							dormant = pm.read_uint(entity + m_bDormant)
						except:
							time.sleep( 2 )
							continue

						#Glow
						if glow == 1:
							if keyboard.is_pressed(glowKey) and glowActive == False:
								glowActive = True
								time.sleep(0.3)
								#speak("ВХ - он")
							elif keyboard.is_pressed(glowKey) and glowActive == True:
								glowActive = False
								time.sleep(0.3)
								#speak("ВХ - офф")

							if(glowActive):
							
								GLOWRF, GLOWGF, GLOWBF = float(GLOWR / 255), float(GLOWG / 255), float(GLOWB / 255)
								if entityTeamID != playerTeam and not dormant:
									if hpGlow == 1:
										
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
								#speak("Чамс - он")
							elif keyboard.is_pressed(chamsKey) and chamsActive == True:
								chamsActive = False
								time.sleep(0.3)
								#speak("Чамс - офф")
						
							if(chamsActive):
								if entityTeamID != playerTeam:
									pm.write_int(entity + m_clrRender, (chamsR))
									pm.write_int(entity + m_clrRender + 0x1, (chamsG))
									pm.write_int(entity + m_clrRender + 0x2, (chamsB))

						#radar
						if radar == 1:
							if keyboard.is_pressed(radarKey) and radarActive == False:
								radarActive = True
								time.sleep(0.3)
								#speak("Радар - он")
							elif keyboard.is_pressed(radarKey) and radarActive == True:
								radarActive = False
								time.sleep(0.3)
								#speak("Радар - офф")

							if(radarActive):
								if entityTeamID != playerTeam:
									pm.write_int(entity + m_bSpotted, 1)


				#Bhop
				if keyboard.is_pressed(bhopKey): 
					if bhopActive == 1 and bhopType == 1: #Normal
						if player and on_ground and on_ground == 257 or on_ground == 263:
							pm.write_int(client + dwForceJump, 6)
							
					if bhopActive == 1 and bhopType == 2: #legit
						if player and on_ground and on_ground == 257 or on_ground == 263:
							a = random.randint(0,5)
							time.sleep(a/100)
							pm.write_int(client + dwForceJump, 5)
							time.sleep(0.08)
							pm.write_int(client + dwForceJump, 4)

				#Trigger
				if triggerActive == 1:
					if keyboard.is_pressed(triggerKey):
						if 0 < crosshairID <= 64 and playerTeam != crosshairTeam:
							pm.write_int(client + dwForceAttack, 6)
						time.sleep(shotDelay)

				# #AutoAccept
				# if autoAccept == 1:
				# 	if keyboard.is_pressed(autoAcceptKey) and autoAcceptActive == False:
				# 		autoAcceptActive = True
				# 		pm.write_int(client + 0x44CEF0, 1)
				# 		time.sleep(0.3)
				# 		#speak("Ркс - он")
				# 	elif keyboard.is_pressed(autoAcceptKey) and autoAcceptActive == True:
				# 		autoAcceptActive = False
				# 		pm.write_int(client + 0x44CEF0, 0)
				# 		time.sleep(0.3)
				# 		#speak("Ркс - офф")

					#if(autoAcceptActive):
						 # dw_AcceptMatch -> 0x44CEF0
						#time.sleep(0.5)

				#rcs
				if rcs == 1:
					if keyboard.is_pressed(rcsKey) and rcsActive == False:
						rcsActive = True
						time.sleep(0.3)
						#speak("Ркс - он")
					elif keyboard.is_pressed(rcsKey) and rcsActive == True:
						rcsActive = False
						time.sleep(0.3)
						#speak("Ркс - офф")
					
					punchx = pm.read_float(player + m_aimPunchAngle)
					punchy = pm.read_float(player + m_aimPunchAngle + 4)
					
					view_angley = pm.read_float(engine_pointer + dwClientState_ViewAngles + 4)
					if(rcsActive):
						if pm.read_int(player + m_iShotsFired) > 2:
							new_punch = Vector3(punchx - g_oldpunchx,
												punchy - g_oldpunchy, 0)
							new_angle = Vector3(view_anglex - new_punch.x * 2.0, view_angley - new_punch.y * 2.0, 0)
							u32.mouse_event(0x0001,
											int(((new_angle.y - view_angley) / fl_sensitivity) / -0.022),
											int(((new_angle.x - view_anglex) / fl_sensitivity) / 0.022),
											0, 0)
						g_oldpunchx = punchx
						g_oldpunchy = punchy
				#aim

				# else:
				# 	target_set(Player(0))		

				# def rankreveal():
				# 	ranks = ["Unranked",
				# 				"Silver I",
				# 				"Silver II",
				# 				"Silver III",
				# 				"Silver IV",
				# 				"Silver Elite",
				# 				"Silver Elite Master",
				# 				"Gold Nova I",
				# 				"Gold Nova II",
				# 				"Gold Nova III",
				# 				"Gold Nova Master",
				# 				"Master Guardian I",
				# 				"Master Guardian II",
				# 				"Master Guardian Elite",
				# 				"Distinguished Master Guardian",
				# 				"Legendary Eagle",
				# 				"Legendary Eagle Master",
				# 				"Supreme Master First Class",
				# 				"The Global Elite"]
				# 	for i in range( 0, 32 ):
				# 		entity = pm.read_uint( client + dwEntityList + i * 0x10 )

				# 		if entity:
				# 			entityTeamID = pm.read_int(entity + m_iTeamNum)
				# 			if entityTeamID :
				# 				player_info = pm.read_uint(
				# 						(pm.read_uint( engine + dwClientState )) + dwClientState_PlayerInfo )
				# 				player_info_items = pm.read_uint( pm.read_uint( player_info + 0x40 ) + 0xC )
				# 				info = pm.read_uint( player_info_items + 0x28 + (i * 0x34) )
				# 				playerres = pm.read_uint( client + dwPlayerResource )
				# 				rank = pm.read_uint( playerres + m_iCompetitiveRanking + (i * 4 ))
				# 				wins = pm.read_uint(playerres + m_iCompetitiveWins + i * 4)
				# 				if pm.read_string( info + 0x10 ) != 'GOTV':
				# 					print(rank)
				# 					print( pm.read_string( info + 0x10 ) + "   -->   " + ranks[rank] )
				# 					print(wins)
				
				# if keyboard.is_pressed("c"):
				# 	rankreveal()

	else:
		os.system("cls")
		print("HWID ERROR!")
		print(colored(hwid, "red"))
		print("Please contact:", colored("Ruslan#7905", "cyan"))
		os.system('pause >NUL')
		
if __name__ == "__main__":
	main()
