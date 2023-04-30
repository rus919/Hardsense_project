import ctypes
import platform
import math
from ctypes import Structure, c_char, c_float, c_int16, c_int32, c_int64, c_int8, c_long, c_uint32, c_uint64, create_string_buffer, create_unicode_buffer, pointer, sizeof, windll
import pymem
import pymem.process
import requests
from win32api import GetAsyncKeyState
import urllib3

urllib3.disable_warnings()

print("HARDSENSE | 1.8 BETA TEST")

ntdll = windll.ntdll
k32 = windll.kernel32
u32 = windll.user32
user32 = ctypes.windll.user32

g_glow = True
g_aimbot = True
g_aimbot_rcs = True
g_aimbot_head = True
g_aimbot_fov = 10.5 / 180.0
g_aimbot_smooth = 0.5

g_previous_tick = 0
g_current_tick = 0

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
dwClientState_ViewAngles = int( response["signatures"]["dwClientState_ViewAngles"] )
dwClientState_GetLocalPlayer = int( response["signatures"]["dwClientState_GetLocalPlayer"] )
dwClientState_MaxPlayer = int( response["signatures"]["dwClientState_MaxPlayer"] )
dwClientState_State = int( response["signatures"]["dwClientState_State"] )
dwSensitivity = int( response["signatures"]["dwSensitivity"] )
m_bDormant = int(response["signatures"]["m_bDormant"])

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
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
m_lifeState = int(response["netvars"]["m_lifeState"])
m_nTickBase = int(response["netvars"]["m_nTickBase"])
m_Local = int(response["netvars"]["m_Local"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_iShotsFired = int(response["netvars"]["m_iShotsFired"])
#m_nForceBone = int(response["netvars"]["m_nForceBone"])
m_aimPunchAngle = int(response["netvars"]["m_aimPunchAngle"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])


# ---------------------------------- Auto update Offsets ----------------------------------

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

engine_pointer = pm.read_uint( engine + dwClientState )
maxClients = pm.read_uint(engine_pointer + dwClientState_MaxPlayer)

class Vector3(Structure):
	_fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]


# class PROCESSENTRY32(Structure):
# 	_fields_ = [
# 		("dwSize", c_uint32),
# 		("cntUsage", c_int32),
# 		("th32ProcessID", c_uint32),
# 		("th32DefaultHeapID", c_int64),
# 		("th32ModuleID", c_uint32),
# 		("cntThreads", c_uint32),
# 		("th32ParentProcessID", c_uint32),
# 		("pcPriClassBase", c_uint32),
# 		("dwFlags", c_uint32),
# 		("szExeFile", c_char * 260)
# 	]


# class Process:
# 	@staticmethod
# 	def get_process_handle(name):
# 		handle = 0
# 		entry = PROCESSENTRY32()
# 		snap = k32.CreateToolhelp32Snapshot(0x00000002, 0)
# 		entry.dwSize = sizeof(PROCESSENTRY32)
# 		while k32.Process32Next(snap, pointer(entry)):
# 			if entry.szExeFile == name.encode("ascii", "ignore"):
# 				handle = k32.OpenProcess(0x430, 0, entry.th32ProcessID)
# 				break
# 		k32.CloseHandle(snap)
# 		return handle

# 	@staticmethod
# 	def get_process_peb(handle, wow64):
# 		buffer = (c_uint64 * 6)(0)
# 		if wow64:
# 			if ntdll.NtQueryInformationProcess(handle, 26, pointer(buffer), 8, 0) == 0:
# 				return buffer[0]
# 		else:
# 			if ntdll.NtQueryInformationProcess(handle, 0, pointer(buffer), 48, 0) == 0:
# 				return buffer[1]
# 		return 0

# 	def __init__(self, name):
# 		self.mem = self.get_process_handle(name)
# 		if self.mem == 0:
# 			raise Exception("Process [" + name + "] not found!")
# 		self.peb = self.get_process_peb(self.mem, True)
# 		if self.peb == 0:
# 			self.peb = self.get_process_peb(self.mem, False)
# 			self.wow64 = False
# 		else:
# 			self.wow64 = True

# 	def read_i32(self, address, length=4):
# 		buffer = c_uint32()
# 		ntdll.NtReadVirtualMemory(self.mem, address, pointer(buffer), length, 0)
# 		return buffer.value

class Player:
	def __init__(self, address):
		self.address = address

	def get_team_num(self):
		# return pm.read_int(self.address + m_iTeamNum)
		playerTeam = pm.read_uint(player + m_iTeamNum)
		return playerTeam
		#player = pm.read_int(client + dwLocalPlayer)
		#return pm.read_int(player + m_iTeamNum)

	def get_health(self):    
		try:
			health = pm.read_int(player + m_iHealth)
			return health
		except Exception:
			raise

	def get_eye_pos(self):
		vectorx = pm.read_float( player + m_vecViewOffset )
		vectory = pm.read_float( player + m_vecViewOffset + 4 )
		vectorz = pm.read_float( player + m_vecViewOffset + 8 )
		originx = pm.read_float( player + m_vecOrigin )
		originy = pm.read_float( player + m_vecOrigin + 4 )
		originz = pm.read_float( player + m_vecOrigin + 8 )
		return Vector3(vectorx + originx, vectory + originy, vectorz + originz)

	def get_vec_punch(self):
		return Vector3(
			pm.read_float(player + m_aimPunchAngle),
			pm.read_float(player + m_aimPunchAngle + 0x4),
			pm.read_float(player + m_aimPunchAngle + 0x8)
		)

	def get_bone_pos(self, index):
		a0 = 0x30 * index
		a1 = pm.read_int(self.address + m_dwBoneMatrix)
		return Vector3(
			pm.read_float(a1 + a0 + 0x0C),
			pm.read_float(a1 + a0 + 0x1C),
			pm.read_float(a1 + a0 + 0x2C)
		)

	def is_valid(self):
		health = self.get_health()
		player = pm.read_int(client + dwLocalPlayer)

		return self.address != 0 and pm.read_int(player + m_lifeState) == 0 and 0 < health < 1338

		# for i in range(1, maxClients):
		# 	entity = pm.read_uint( client + dwEntityList + i * 0x10 )

		# 	if entity:
		# 		try:
		# 			entityHp = pm.read_int(entity + m_iHealth)
		# 		except:
		# 			k32.Sleep(2)
		# 			print("error2")
		# 			continue
		# 		valid = self.address != 0 and pm.read_int(player + m_lifeState) == 0 and 0 < entityHp < 1338
		# return valid



def get_view_angles():
	return Vector3(
		pm.read_float(engine_pointer + dwClientState_ViewAngles),
		pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4),
		pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x8)
	)

class Math:
	@staticmethod
	def sin_cos(radians):
		return [math.sin(radians), math.cos(radians)]

	@staticmethod
	def rad2deg(x):
		return x * 3.141592654

	@staticmethod
	def deg2rad(x):
		return x * 0.017453293

	@staticmethod
	def angle_vec(angles):
		s = Math.sin_cos(Math.deg2rad(angles.x))
		y = Math.sin_cos(Math.deg2rad(angles.y))
		return Vector3(s[1] * y[1], s[1] * y[0], -s[0])

	@staticmethod
	def vec_normalize(vec):
		radius = 1.0 / (math.sqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z) + 1.192092896e-07)
		vec.x *= radius
		vec.y *= radius
		vec.z *= radius
		return vec

	@staticmethod
	def vec_angles(forward):
		if forward.y == 0.00 and forward.x == 0.00:
			yaw = 0
			pitch = 270.0 if forward.z > 0.00 else 90.0
		else:
			yaw = math.atan2(forward.y, forward.x) * 57.295779513
			if yaw < 0.00:
				yaw += 360.0
			tmp = math.sqrt(forward.x * forward.x + forward.y * forward.y)
			pitch = math.atan2(-forward.z, tmp) * 57.295779513
			if pitch < 0.00:
				pitch += 360.0
		return Vector3(pitch, yaw, 0.00)

	@staticmethod
	def vec_clamp(v):
		if 89.0 < v.x <= 180.0:
			v.x = 89.0
		if v.x > 180.0:
			v.x -= 360.0
		if v.x < -89.0:
			v.x = -89.0
		v.y = math.fmod(v.y + 180.0, 360.0) - 180.0
		v.z = 0.00
		return v

	@staticmethod
	def vec_dot(v0, v1):
		return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

	@staticmethod
	def vec_length(v):
		return v.x * v.x + v.y * v.y + v.z * v.z

	@staticmethod
	def get_fov(va, angle):
		a0 = Math.angle_vec(va)
		a1 = Math.angle_vec(angle)
		return Math.rad2deg(math.acos(Math.vec_dot(a0, a1) / Math.vec_length(a0)))

def get_target_angle(local_p, target, bone_id):
	m = target.get_bone_pos(bone_id)
	c = local_p.get_eye_pos()
	c.x = m.x - c.x
	c.y = m.y - c.y
	c.z = m.z - c.z
	c = Math.vec_angles(Math.vec_normalize(c))
	if g_aimbot_rcs and pm.read_uint( player + m_iShotsFired ) > 1:
		p = local_p.get_vec_punch()
		c.x -= p.x * 2.0
		c.y -= p.y * 2.0
		c.z -= p.z * 2.0
	return Math.vec_clamp(c)

_target_bone = 0
# _bones = [5, 4, 3, 0, 7, 8]
_bones = [0, 3, 4, 5, 6, 7, 8, 70, 71, 72, 73, 77, 78, 79, 80, 11, 12, 13, 41, 42, 43]


def target_set(target):
	global _target
	_target = target


def get_best_target(va, local_p):
	global _target_bone
	a0 = 9999.9
	for i in range(1, maxClients):
		entity = Player(pm.read_int(client + dwEntityList + i * 0x10))
		if not entity.is_valid():
			continue
		# if pm.read_uint(player + m_iTeamNum) == pm.read_int(entity + m_iTeamNum):
		# 	continue
		if g_aimbot_head:
			fov = Math.get_fov(va, get_target_angle(local_p, entity, 8))
			if fov < a0:
				a0 = fov
				target_set(entity)
				_target_bone = 8
		else:
			for j in range(0, _bones.__len__()):
				fov = Math.get_fov(va, get_target_angle(local_p, entity, _bones[j]))
				if fov < a0:
					a0 = fov
					target_set(entity)
					_target_bone = _bones[j]
	return a0 != 9999


def aim_at_target(sensitivity, va, angle):
	global g_current_tick
	global g_previous_tick
	y = pm.read_float( engine_pointer + dwClientState_ViewAngles ) - angle.x
	x = pm.read_float( engine_pointer + dwClientState_ViewAngles + 0x4 ) - angle.y
	if y > 89.0:
		y = 89.0
	elif y < -89.0:
		y = -89.0
	if x > 180.0:
		x -= 360.0
	elif x < -180.0:
		x += 360.0
	if math.fabs(x) / 180.0 >= g_aimbot_fov:
		target_set(Player(0))
		return
	if math.fabs(y) / 89.0 >= g_aimbot_fov:
		target_set(Player(0))
		return
	x = (x / sensitivity) / 0.022
	y = (y / sensitivity) / -0.022
	if g_aimbot_smooth > 1.00:
		sx = 0.00
		sy = 0.00
		if sx < x:
			sx += 1.0 + (x / g_aimbot_smooth)
		elif sx > x:
			sx -= 1.0 - (x / g_aimbot_smooth)
		if sy < y:
			sy += 1.0 + (y / g_aimbot_smooth)
		elif sy > y:
			sy -= 1.0 - (y / g_aimbot_smooth)
	else:
		sx = x
		sy = y
	if g_current_tick - g_previous_tick > 0:
		g_previous_tick = g_current_tick
		u32.mouse_event(0x0001, int(sx), int(sy), 0, 0)

def GetWindowText(handle, length=100):

	window_text = ctypes.create_string_buffer(length)
	user32.GetWindowTextA(
		handle,
		ctypes.byref(window_text),
		length
	)

	return window_text.value

if __name__ == "__main__":
	# try:
	# 	mem = Process('csgo.exe')
	# except Exception as e:
	# 	print(e)
	# 	exit(0)

	while True:
		if GetWindowText( user32.GetForegroundWindow() ).decode( 'cp1252' ) == "Counter-Strike: Global Offensive - Direct3D 9":
			try:
				_target = pm.read_int(client + dwLocalPlayer)

				self = Player(pm.read_int(client + dwEntityList + pm.read_int(engine_pointer + dwClientState_GetLocalPlayer) * 0x10))

				global player
				player = pm.read_int(client + dwLocalPlayer)

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
						sensitivity = 2.0
						view_angle = get_view_angles()
					except:
						print("error3")
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
							#self = pm.read_int(entity + localPlayer)
							#self = get_client_entity(get_local_player())
						except:
							print("error4")
							k32.sleep( 2 )
							continue

						#Glow
						if entityTeamID != playerTeam and not dormant:
							pm.write_float(glowManager + entityGlow * 0x38 + 0x8, 1.0) #R
							pm.write_float(glowManager + entityGlow * 0x38 + 0xC , 1.0) #G
							pm.write_float(glowManager + entityGlow * 0x38 + 0x10, 0.0) #B
							pm.write_float(glowManager + entityGlow * 0x38 + 0x14, 0.6) #A
							pm.write_int( glowManager + entityGlow * 0x38 + 0x28, 1 ) #enable

						target_set(entity)
						

						#if GetAsyncKeyState(18) != 0 and self.address != 0 and pm.read_int(player + m_lifeState) == 0 and 0 < self.get_health() < 1338:
				if GetAsyncKeyState(18) != 0 and player and entityHp > 0:
					# print(entityHp)
					#print(getHealth())
					player = pm.read_int(client + dwLocalPlayer)
					g_current_tick = pm.read_int(player + m_nTickBase)
					if not get_best_target(view_angle, self) and dormant and not pm.read_int(player + m_lifeState) > 1:
						continue
					

					aim_at_target(2.0, view_angle, get_target_angle(self, _target, _target_bone))

					if pm.read_uint( player + m_iCrosshairId ) == 0:
						continue
				else:
					target_set(Player(0))

					#print(self.get_health())

				# if GetAsyncKeyState(18) != 0 and self.address != 0 and pm.read_int(player + m_lifeState) == 0 and 0 < self.get_health() < 1338:
				# 	print(getHealth())
				# 	player = pm.read_int(client + dwLocalPlayer)
				# 	g_current_tick = pm.read_int(player + m_nTickBase)
				# 	if not get_best_target(view_angle, self):
				# 		continue
				# 	aim_at_target(2.0, view_angle, get_target_angle(self, _target, _target_bone))

				# 	if pm.read_uint( player + m_iCrosshairId ) == 0:
				# 		continue
				# else:
				# 	target_set(Player(0))

				# if GetAsyncKeyState(18) != 0:
				# 	cross_id = self.get_cross_index()
				# 	if cross_id == 0:
				# 		continue
				# 	cross_target = Entity.get_client_entity(cross_id - 1)
				# 	player = pm.read_int(client + dwLocalPlayer)
				# 	g_current_tick = pm.read_int(player + m_nTickBase)
				# 	if not _target.is_valid() and not get_best_target(view_angle, self):
				# 		continue
				# 	aim_at_target(fl_sensitivity, view_angle, get_target_angle(self, _target, _target_bone))

				# 	if self.get_team_num() != cross_target.get_team_num() and cross_target.get_health() > 0:
				# 		aim_at_target(fl_sensitivity, view_angle, get_target_angle(self, _target, _target_bone))
				# 		#k32.Sleep(50)
				# 		u32.mouse_event(0x0002, 0, 0, 0, 0)
				# 		k32.Sleep(50)
				# 		u32.mouse_event(0x0004, 0, 0, 0, 0)
				# else:
				# 	target_set(Player(0))
				
				# if g_rcs:
				# 	current_punch = self.get_vec_punch()
				# 	if self.get_shots_fired > 1:
				# 		new_punch = Vector3(current_punch.x - g_old_punch.x,
				# 							current_punch.y - g_old_punch.y, 0)
				# 		new_angle = Vector3(view_angle.x - new_punch.x * 2.0, view_angle.y - new_punch.y * 2.0, 0)
				# 		u32.mouse_event(0x0001,
				# 						int(((new_angle.y - view_angle.y) / fl_sensitivity) / -0.022),
				# 						int(((new_angle.x - view_angle.x) / fl_sensitivity) / 0.022),
				# 						0, 0)
				# 	g_old_punch = current_punch

					# if GetAsyncKeyState(18) != 0:
					# 	player = pm.read_int(client + dwLocalPlayer)
					# 	g_current_tick = pm.read_int(player + m_nTickBase)
					# 	if not _target.is_valid() and not get_best_target(view_angle, self):
					# 		continue
					# 	aim_at_target(fl_sensitivity, view_angle, get_target_angle(self, _target, _target_bone))

					# 	cross_id = self.get_cross_index()
					# 	if cross_id == 0:
					# 		continue
					# 	cross_target = Entity.get_client_entity(cross_id - 1)

					# 	if self.get_team_num() != cross_target.get_team_num() and cross_target.get_health() > 0:
					# 		aim_at_target(fl_sensitivity, view_angle, get_target_angle(self, _target, _target_bone))
					# 		#k32.Sleep(25)
					# 		u32.mouse_event(0x0002, 0, 0, 0, 0)
					# 		k32.Sleep(50)
					# 		u32.mouse_event(0x0004, 0, 0, 0, 0)
					# else:
					# 	target_set(Player(0))
					# if g_rcs:
					# current_punch = self.get_vec_punch()
					# if pm.read_int(player + m_iShotsFired) > 1:
					# 	new_punch = Vector3(current_punch.x - g_old_punch.x,
					# 						current_punch.y - g_old_punch.y, 0)
					# 	new_angle = Vector3(view_angle.x - new_punch.x * 2.0, view_angle.y - new_punch.y * 2.0, 0)
					# 	u32.mouse_event(0x0001,
					# 					int(((new_angle.y - view_angle.y) / fl_sensitivity) / -0.022),
					# 					int(((new_angle.x - view_angle.x) / fl_sensitivity) / 0.022),
					# 					0, 0)
					# g_old_punch = current_punch
			except ValueError:
				continue
		else:
			g_previous_tick = 0
			target_set(Player(0))

