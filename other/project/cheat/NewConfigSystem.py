from glob import glob1
from locale import getlocale
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

urllib3.disable_warnings()

u32 = windll.user32

try:
	from subprocess import DEVNULL
except ImportError:
	DEVNULL = os.open(os.devnull, os.O_RDWR)

hwid = str(str(subprocess.check_output('wmic csproduct get uuid', stdin=DEVNULL, stderr=DEVNULL)).strip().replace(r"\r", "").split(r"\n")[1].strip())
users = requests.get("https://pastebin.com/raw/VS7ThBDw", verify=False)
currDate1 = requests.get("https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Amsterdam").json()
currDate = str(currDate1["date"])
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
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
# ---------------------------------- Auto update Offsets ----------------------------------

def getUsers():
	global userHwid, userName, userConfig, userDiscord, userExpiryDate
	usersData = users.json()
	userHwid = list(usersData["users"][hwid])
	userConfig = userHwid[0]
	userName = userHwid[1]
	userExpiryDate = userHwid[2]
	#userName = object(usersData["users"][hwid[0]])

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
	config = requests.get("https://pastebin.com/raw/" + userConfig, verify=False).json()

def console():
	os.system("cls")
	print(userHwid)
	print(userConfig)
	print(userName)
	print(userExpiryDate)
	print(currDate)


def main():
	if hwid in users.text:
		av()
		getUsers()
		autoConfig()
		console()
		if userExpiryDate > currDate: #Проверка если дата больше чем текущая то чит не запускать
			print("done")
		else:
			print("not done")

	else:
		os.system("cls")
		print("HWID ERROR!")
		print(colored(hwid, "red"))
		print("Please contact:", colored("Ruslan#7905", "cyan"))
		os.system('pause >NUL')
		
if __name__ == "__main__":
	main()
