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
from math import isnan, sqrt, asin, atan
from itertools import repeat
urllib3.disable_warnings()

k32 = windll.kernel32
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
users = requests.get("https://pastebin.com/raw/VS7ThBDw", verify=False)
currDate1 = requests.get("https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Amsterdam").json()
currDate = str(currDate1["date"])

try:
	pm = pymem.Pymem("csgo.exe")
	client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
	engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
except:
	print("Run CS:GO before starting", colored("HARDSENSE", "red"))
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
dwbSendPackets = int(response["signatures"]["dwbSendPackets"])

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
m_nTickBase = int(response["netvars"]["m_nTickBase"])
m_lifeState = int(response["netvars"]["m_lifeState"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
m_Local = int(response["netvars"]["m_Local"])
m_nForceBone = int(response["netvars"]["m_Local"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
m_bSpottedByMask = int(response["netvars"]["m_bSpottedByMask"])
# ---------------------------------- Auto update Offsets ----------------------------------

def GetWindowText(handle, length=100):

	window_text = ctypes.create_string_buffer(length)
	user32.GetWindowTextA(
		handle,
		ctypes.byref(window_text),
		length
	)

	return window_text.value

def getUsers():
	global userHwid, userName, userConfig, userDiscord, userExpiryDate
	usersData = users.json()
	userHwid = list(usersData["users"][hwid])
	userConfig = userHwid[0]
	userName = userHwid[1]
	userExpiryDate = userHwid[2]

def av():
	aa0 = "a779d2b2687c01783d4ba406d6db003d29bfeff7f88954b5cca35db6b3e7023f"
	aa1 = "649e2b944d01a13fbbb65c369cc793ed"
	aa2 = 634522979280582856943583417864215043553732516036833547407673484229549188531778767436206111157265100988522719961647899025697046388675241184343995293811266961044261395238311757794962183074214827
	aa3 = ["6bc002242812283c2f7d6769d08df1ecf06f1492f10e5c0babd7d6dd095eb4570ccffd3c0f850317b8a10a77b2a45e7f9c6da9e06e35d44d1786d3c887ed1ca7", 6421467839|412, 37528940968531359234, 1766808553236511598249957914423320888445826969670139386686364123287996035227569576721816277735,  1646849682681777278692270805931344199, 5267721142988091488659587045] 

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
	print(colored("HARDSENSE", "red"))
	print("User:", colored(userName, "cyan"))
	print("Version:", colored("1.9.1 BETA", "magenta"))
	print("Expiry date:", colored(userExpiryDate, "green"))

def nanchecker(first, second):
	if isnan( first ) or isnan( second ):
		return False
	else:
		return True

def checkangles(x, y):
	if x > 89:
		return False
	elif x < -89:
		return False
	elif y > 360:
		return False
	elif y < -360:
		return False
	else:
		return True

def normalizeAngles(viewAngleX, viewAngleY):
	if viewAngleX > 89:
		viewAngleX -= 360
	if viewAngleX < -89:
		viewAngleX += 360
	if viewAngleY > 180:
		viewAngleY -= 360
	if viewAngleY < -180:
		viewAngleY += 360
	return viewAngleX, viewAngleY

def calc_distance(current_x, current_y, new_x, new_y):
	distancex = new_x - current_x
	if distancex < -89:
		distancex += 360
	elif distancex > 89:
		distancex -= 360
	if distancex < 0.0:
		distancex = -distancex

	distancey = new_y - current_y
	if distancey < -180:
		distancey += 360
	elif distancey > 180:
		distancey -= 360
	if distancey < 0.0:
		distancey = -distancey
	return distancex, distancey

def calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3):
	try:
		delta_x = localpos1 - enemypos1
		delta_y = localpos2 - enemypos2
		delta_z = localpos3 - enemypos3
		hyp = sqrt( delta_x * delta_x + delta_y * delta_y + delta_z * delta_z )
		x = asin( delta_z / hyp ) * 57.295779513082
		y = atan( delta_y / delta_x ) * 57.295779513082
		if delta_x >= 0.0:
			y += 180.0
	except:
		return 0,0
	return x, y

def autobhop(player, on_ground):
	if keyboard.is_pressed(bhopKey) and bhopActive == 1: 
		if bhopType == 1: #Normal
			if player and on_ground and on_ground == 257 or on_ground == 263:
				pm.write_int(client + dwForceJump, 6)
				
		if bhopType == 2: #legit
			if player and on_ground and on_ground == 257 or on_ground == 263:
				a = random.randint(0,5)
				time.sleep(a/100)
				pm.write_int(client + dwForceJump, 5)
				time.sleep(0.08)
				pm.write_int(client + dwForceJump, 4)

def main():
	if hwid in users.text:
		av()
		getUsers()
		autoConfig()
		console()

		glowActive = True
		chamsActive = True
		radarActive = True
		rcsActive = True
		
		oldpunchx = 0.0
		oldpunchy = 0.0

		if userExpiryDate > currDate:
			while True:
				aim = 1
				aimkey = 5
				aimrcs = True
				
				target_bone = 8

				aimfov = 3
				target = None
				olddistx = 111111111111
				olddisty = 111111111111

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
						playerTeam = pm.read_uint(player + m_iTeamNum)
						glowManager = pm.read_int(client + dwGlowObjectManager)
						engine_pointer = pm.read_uint( engine + dwClientState )
						maxClients = pm.read_uint(engine_pointer + dwClientState_MaxPlayer)
					except:
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
							spotted = pm.read_int(entity + m_bSpottedByMask)
						except:
							time.sleep( 2 )
							continue

						#Glow
						if glow == 1:
							if keyboard.is_pressed(glowKey) and glowActive == False:
								glowActive = True
								time.sleep(0.3)
							elif keyboard.is_pressed(glowKey) and glowActive == True:
								glowActive = False
								time.sleep(0.3)

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
						#aim
						if aim == 1 and playerTeam != entityTeamID and entityHp > 0:
							entity_bones = pm.read_uint( entity + m_dwBoneMatrix )
							localpos_x_angles = pm.read_float( engine_pointer + dwClientState_ViewAngles )
							localpos_y_angles = pm.read_float( engine_pointer + dwClientState_ViewAngles + 0x4 )
							localpos1 = pm.read_float( player + m_vecOrigin )
							localpos2 = pm.read_float( player + m_vecOrigin + 4 )
							localpos_z_angles = pm.read_float( player + m_vecViewOffset + 0x8 )
							localpos3 = pm.read_float( player + m_vecOrigin + 8 ) + localpos_z_angles
							try:
								entitypos_x = pm.read_float( entity_bones + 0x30 * target_bone + 0xC )
								entitypos_y = pm.read_float( entity_bones + 0x30 * target_bone + 0x1C )
								entitypos_z = pm.read_float( entity_bones + 0x30 * target_bone + 0x2C )
							except:
								continue
							X, Y = calcangle( localpos1, localpos2, localpos3, entitypos_x, entitypos_y, entitypos_z )
							newdist_x, newdist_y = calc_distance( localpos_x_angles, localpos_y_angles, X, Y )
							if newdist_x < olddistx and newdist_y < olddisty and newdist_x <= aimfov and newdist_y <= aimfov:
								olddistx, olddisty = newdist_x, newdist_y
								target, target_hp, target_dormant = entity, entityHp, dormant
								target_x, target_y, target_z = entitypos_x, entitypos_y, entitypos_z
						if aim == 1 and GetAsyncKeyState(aimkey) != 0 and player:
							if target and target_hp > 0 and not target_dormant:
								pitch, yaw = calcangle( localpos1, localpos2, localpos3, target_x, target_y, target_z )
								normalize_x, normalize_y = normalizeAngles( pitch, yaw )
								punchx = pm.read_float( player + m_aimPunchAngle )
								punchy = pm.read_float( player + m_aimPunchAngle + 0x4 )

								if aimrcs and pm.read_uint( player + m_iShotsFired ) > 1:
									pm.write_float( engine_pointer + dwClientState_ViewAngles, normalize_x - (punchx * 2) )
									pm.write_float( engine_pointer + dwClientState_ViewAngles + 0x4, normalize_y - (punchy * 2) )
								else:
									pm.write_float( engine_pointer + dwClientState_ViewAngles, normalize_x )
									pm.write_float( engine_pointer + dwClientState_ViewAngles + 0x4, normalize_y )

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
								time.sleep(0.05)
								radarActive = False
								time.sleep(0.3)
								#speak("Радар - офф")

							if(radarActive):
								if entityTeamID != playerTeam:
									pm.write_int(entity + m_bSpotted, 1)
				#Bhop
				autobhop(player, on_ground)

				#Trigger
				if triggerActive == 1:
					if GetAsyncKeyState(5) != 0:
						if 0 < crosshairID <= 64 and playerTeam != crosshairTeam:
							pm.write_int(client + dwForceAttack, 6)
							time.sleep(0.2)

				if triggerActive == 1:
					if GetAsyncKeyState(18) != 0:
						if 0 < crosshairID <= 64 and playerTeam != crosshairTeam:
							pm.write_int(client + dwForceAttack, 6)
							time.sleep(0.2)

				#rcs
				if rcs == 1:
					if keyboard.is_pressed(rcsKey) and rcsActive == False:
						rcsActive = True
						time.sleep(0.3)
					elif keyboard.is_pressed(rcsKey) and rcsActive == True:
						rcsActive = False
						time.sleep(0.3)

					if(rcsActive):
						if pm.read_uint( player + m_iShotsFired ) > 2:
							rcs_x = pm.read_float( engine_pointer + dwClientState_ViewAngles )
							rcs_y = pm.read_float( engine_pointer + dwClientState_ViewAngles + 0x4 )
							punchx = pm.read_float( player + m_aimPunchAngle )
							punchy = pm.read_float( player + m_aimPunchAngle + 0x4 )
							newrcsx = rcs_x - (punchx - oldpunchx) * 2
							newrcsy = rcs_y - (punchy - oldpunchy) * 2
							oldpunchx = punchx
							oldpunchy = punchy
							if nanchecker( newrcsx, newrcsy ) and checkangles( newrcsx, newrcsy ):
								pm.write_float( engine_pointer + dwClientState_ViewAngles, newrcsx )
								pm.write_float( engine_pointer + dwClientState_ViewAngles + 0x4, newrcsy )
						else:
							oldpunchx = 0.0
							oldpunchy = 0.0
							newrcsx = 0.0
							newrcsy = 0.0

		elif userExpiryDate < currDate:
			print("Expired")
		else:
			print("Error")

	else:
		os.system("cls")
		print("HWID ERROR!")
		print(colored(hwid, "red"))
		print("Please contact:", colored("Ruslan#7905", "cyan"))
		os.system('pause >NUL')
		
if __name__ == "__main__":
	main()
