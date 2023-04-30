import requests
import urllib3
urllib3.disable_warnings()



offsets = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
response = requests.get(offsets, verify=False).json()

dwClientState = int(response["signatures"]["dwClientState"])
dwClientState_GetLocalPlayer = int(response["signatures"]["dwClientState_GetLocalPlayer"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
dwClientState_MaxPlayer = int(response["signatures"]["dwClientState_MaxPlayer"])
dwClientState_State = int(response["signatures"]["dwClientState_State"])
dwEntityList = int(response["signatures"]["dwEntityList"])
dwGlobalVars = int(response["signatures"]["dwGlobalVars"])
dwViewMatrix = int(response["signatures"]["dwViewMatrix"])

#Netvars
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_iHealth = int(response["netvars"]["m_iHealth"])
m_lifeState = int(response["netvars"]["m_lifeState"])
m_nTickBase = int(response["netvars"]["m_nTickBase"])
m_iShotsFired = int(response["netvars"]["m_iShotsFired"])
m_iCrossHairID = int(response["netvars"]["m_iCrosshairId"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
m_Local = int(response["netvars"]["m_Local"])
m_bSpottedByMask = int(response["netvars"]["m_bSpottedByMask"])
m_bSpotted = int(response["netvars"]["m_bSpotted"])
m_fFlags = int(response["netvars"]["m_fFlags"])
m_aimPunchAngle = int(response["netvars"]["m_aimPunchAngle"])
m_iItemDefinitionIndex = int(response["netvars"]["m_iItemDefinitionIndex"])
m_hActiveWeapon = int(response["netvars"]["m_hActiveWeapon"])
m_bIsScoped = int(response["netvars"]["m_bIsScoped"])
m_iAccountID = int(response["netvars"]["m_iAccountID"])
m_bHasDefuser = int(response["netvars"]["m_bHasDefuser"])
m_hObserverTarget = int(response["netvars"]["m_hObserverTarget"])
m_bDormant = int(response["signatures"]["m_bDormant"])




m_hOwnerEntity = int(response["netvars"]["m_hOwnerEntity"])