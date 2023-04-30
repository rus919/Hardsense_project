import pymem, keyboard
import ctypes, sys, os
from itertools import repeat
#i'm importing itertools because it's faster for loops, i've optimized a lot this thing

#Offsets
#some of the offsets can't be found in hazedumper
#others can be found here
#https://raw.githubusercontent.com/naaax123/Python-CSGO-Cheat/main/offsets/offsets.json
dwClientState = 5808068
dwLocalPlayer = 14378476
m_hMyWeapons = 11784
dwEntityList = 81600028
m_iItemDefinitionIndex = 12218
m_nModelIndex = 600
m_iViewModelIndex = 10704
m_iEntityQuality = 12220
m_iItemIDHigh = 12240
m_nFallbackPaintKit = 12760
m_flFallbackWear = 12768
m_nFallbackStatTrak = 12772
m_nFallbackSeed = 12764
m_hActiveWeapon = 12040
m_hViewModel = 13064

knife_ids = {
	"Gold knife" : 519,
	"Spectral knife" : 604,
	"Bayonet" : 612,
	"Classic knife" : 615,
	"Flip knife" : 618,
	"Gut knife" : 621,
	"Karambit" : 624,
	"M9 Bayonet" : 627,
	"Huntsman" : 630,
	"Falchion knife" : 633,
	"Bowie knife" : 636,
	"Butterfly knife" : 639,
	"Shadow daggers" : 642,
	"Cord knife" : 646,
	"Canis knife" : 649,
	"Ursus knife" : 652,
	"Navaja" : 655,
	"Nomad knife" : 658,
	"Stiletto knife" : 661,
	"Talon knife": 664,
	"Skeleton knife" : 667
}

knifeDefinitionIndex_dict = {
	"Gold knife" : 41,
	"Spectral knife" : 505,
	"Bayonet" : 500,
	"Classic knife" : 503,
	"Flip knife" : 505,
	"Gut knife" : 506,
	"Karambit" : 507,
	"M9 Bayonet" : 508,
	"Huntsman" : 509,
	"Falchion knife" : 512,
	"Bowie knife" : 514,
	"Butterfly knife" : 515,
	"Shadow daggers" : 516,
	"Paracord knife" : 517,
	"Survival knife" : 518,
	"Ursus knife" : 519,
	"Navaja" : 520,
	"Nomad knife" : 521,
	"Stiletto knife" : 522,
	"Talon knife": 523,
	"Skeleton knife" : 525
}

CtKnife = 522
TKnife = 547
cachedPlayer = 0
modelIndex = 0
entityQuality = 3

try :
	pm = pymem.Pymem("csgo.exe")
except :
	MessageBox = ctypes.windll.user32.MessageBoxW
	MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
	exit()

client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
engine_state = pm.read_int( engine + dwClientState )

while 1 :
	# if b == 500 : #reading cfg every 500 times to avoid lag, but here there is no cfg so you can delete that
	knifeID = 612
	knifeDefinitionIndex = 500
	#knifeID and knifeDefinitionIndex must be the same type see knifeDefinitionIndex_dict and knife_ids
	paintKit = 42 #whatever paintkit
	fallbackwear = 0
	seed = 0
	knife_st = True
	knife_stv = 10

		# b = 0
	
	# b = b + 1

	localPlayer = pm.read_uint(client + dwLocalPlayer)

	if localPlayer == 0:
		modelIndex = 0
		continue

	elif localPlayer != cachedPlayer:
		modelIndex = 0
		cachedPlayer = localPlayer
		
	if paintKit > 0 and modelIndex > 0 :

		for i in repeat(0, 8) :

			currentWeapon = pm.read_uint(localPlayer + m_hMyWeapons + i * 0x04) & 0xfff
			currentWeapon = pm.read_uint(client + dwEntityList + (currentWeapon - 1) * 0x10)
			if currentWeapon == 0:continue

			weaponID = pm.read_short(currentWeapon + m_iItemDefinitionIndex)

			fallbackPaint = paintKit
			if weaponID != 42 and weaponID != 59 and weaponID != knifeDefinitionIndex :continue

			else:

				pm.write_short(currentWeapon + m_iItemDefinitionIndex, knifeDefinitionIndex)
				pm.write_uint(currentWeapon + m_nModelIndex, modelIndex)
				pm.write_uint(currentWeapon + m_iViewModelIndex, modelIndex)
				pm.write_int(currentWeapon + m_iEntityQuality, entityQuality)

			pm.write_int(currentWeapon + m_iItemIDHigh, -1)
			pm.write_uint(currentWeapon + m_nFallbackPaintKit, fallbackPaint)
			pm.write_float(currentWeapon + m_flFallbackWear,fallbackwear)

			if knife_st :
				stattrack_v = knife_stv
				pm.write_int( currentWeapon + m_nFallbackStatTrak, stattrack_v )
			
			pm.write_int( currentWeapon + m_nFallbackSeed, seed )


	for _ in repeat(None, 100) :
		ActiveWeapon = pm.read_int( localPlayer + m_hActiveWeapon) & 0xfff
		ActiveWeapon = pm.read_int( client + dwEntityList + (ActiveWeapon - 1) * 0x10 )

		if ActiveWeapon == 0:

			continue

		weaponID = pm.read_short( ActiveWeapon + m_iItemDefinitionIndex )

		weaponViewModelId = pm.read_int( ActiveWeapon + m_iViewModelIndex )

		if weaponID == 42 and weaponViewModelId > 0:
			modelIndex = weaponViewModelId + (knifeID - CtKnife)
		elif weaponID == 59 and weaponViewModelId > 0:
			modelIndex = weaponViewModelId + (knifeID - TKnife)
		elif weaponID != knifeDefinitionIndex or modelIndex == 0 :
			continue
		knifeViewModel = pm.read_uint( localPlayer + m_hViewModel ) & 0xfff
		knifeViewModel = pm.read_uint( client + dwEntityList + (knifeViewModel - 1) * 0x10 )

		if knifeViewModel == 0: continue
		pm.write_uint( knifeViewModel + m_nModelIndex, modelIndex)
		
		if keyboard.is_pressed( "f6" ):
			pm.write_int( engine_state + 0x174, -1 )