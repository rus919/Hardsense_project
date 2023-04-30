B9='cyan'
B8='cls'
A2='m_Local'
O=0.0
N=str
J='signatures'
I=print
H=True
G=False
F='netvars'
D=float
B=int
from os import system
import os as P,pymem,pymem.process,keyboard as M,time as E,math,re,requests as T,ctypes as S,random as R,secrets as Q,sys
from termcolor import colored as b
import subprocess as Z,urllib3 as a
from ctypes import *
from win32api import GetAsyncKeyState as i
from psutil import process_iter as d,NoSuchProcess as e,AccessDenied as f,ZombieProcess as g
from math import isnan as W,sqrt,asin,atan
from itertools import repeat
a.disable_warnings()
h=windll.kernel32
A3=windll.user32
try:from subprocess import DEVNULL as U
except ImportError:U=P.open(P.devnull,P.O_RDWR)
try:
	class X:
		def fuck(B):
			for A in d():
				try:
					for C in B:
						if C.lower()in A.name().lower():A.kill()
				except (e,f,g):pass
		def crow():A=['http','traffic','wireshark','fiddler','packet'];return X.fuck(names=A)
	X.crow()
except:pass
A5=S.windll.user32
h=windll.kernel32
A4=windll.ntdll
j=N(N(Z.check_output('wmic csproduct get uuid',stdin=U,stderr=U)).strip().replace('\\r','').split('\\n')[1].strip())
A6=T.get('\u0068\u0074\u0074\u0070\u0073\u003a\u002f\u002f\u0070\u0061\u0073\u0074\u0065\u0062\u0069\u006e\u002e\u0063\u006f\u006d\u002f\u0072\u0061\u0077\u002f\u0078\u0044\u006d\u0053\u0069\u0053\u0031\u0051',verify=G)
try:A=pymem.Pymem('csgo.exe');K=pymem.process.module_from_name(A.process_handle,'client.dll').lpBaseOfDll;A7=pymem.process.module_from_name(A.process_handle,'engine.dll').lpBaseOfDll
except:I('Для начала вам нужно запустить CS:GO!');E.sleep(10);exit()
y='https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
C=T.get(y,verify=G).json()
Am=B(C[J]['dwLocalPlayer'])
An=B(C[J]['dwClientState'])
Ao=B(C[J]['dwGlowObjectManager'])
A8=B(C[J]['dwEntityList'])
k=B(C[J]['dwForceJump'])
A9=B(C[J]['dwForceAttack'])
L=B(C[J]['dwClientState_ViewAngles'])
AX=B(C[J]['dwClientState_GetLocalPlayer'])
Ap=B(C[J]['dwClientState_MaxPlayer'])
AY=B(C[J]['dwClientState_State'])
Aq=B(C[J]['m_bDormant'])
AZ=B(C[J]['dwbSendPackets'])
Ar=B(C[F]['m_iCrosshairId'])
l=B(C[F]['m_iTeamNum'])
As=B(C[F]['m_fFlags'])
At=B(C[F]['m_iGlowIndex'])
Au=B(C[F]['m_iHealth'])
Av=B(C[F]['m_bIsDefusing'])
m=B(C[F]['m_clrRender'])
Aw=B(C[F]['m_bSpotted'])
AA=B(C[F]['m_iShotsFired'])
c=B(C[F]['m_aimPunchAngle'])
Aa=B(C[F]['m_nTickBase'])
Ab=B(C[F]['m_lifeState'])
n=B(C[F]['m_vecOrigin'])
Ax=B(C[F]['m_vecViewOffset'])
Ac=B(C[F][A2])
Ad=B(C[F][A2])
Ay=B(C[F]['m_dwBoneMatrix'])
Az=B(C[F]['m_bSpottedByMask'])
def A_(handle,length=100):A=length;B=S.create_string_buffer(A);A5.GetWindowTextA(handle,S.byref(B),A);return B.value
class Ae(Structure):_fields_=[('x',c_float),('y',c_float),('z',c_float)]
def B0():B='users';global V,Y;A=A6.json();V=N(A[B][j]);Y=N(A[B][V])
def B1():B='a779d2b2687c01783d4ba406d6db003d29bfeff7f88954b5cca35db6b3e7023f';C='649e2b944d01a13fbbb65c369cc793ed';D=0x239a71042f4115b17cb838414d2b0efbc0a132cbf7055987a8811ab6aae250fd9e7cdc5942df4cd1037646d5d6c28b49f9c1bdf86255b46f30ff5a0e544a9a3b91d018e8207f35385f7ea3051915f3ab;E=['6bc002242812283c2f7d6769d08df1ecf06f1492f10e5c0babd7d6dd095eb4570ccffd3c0f850317b8a10a77b2a45e7f9c6da9e06e35d44d1786d3c887ed1ca7',6421467839|412,0x208d194f959ea7602,0x36357c3dbc268e83bf600ee06c05fb3ec21ae6d48f164fe76ba7e8972b4816c56456d0d9bcd2e7,0x13d2bf54d9778c6ac576bd767214147,0x11055b575d2066ef983c3fe5];I(B);I(C);I(D);I(E);A=Q.token_hex(nbytes=64);F=R.randint(1,999),Q.token_urlsafe(32);G=Q.token_bytes(64);H=Q.token_hex(nbytes=128);J=[Q.token_hex(nbytes=64),R.random(),0x208d194f959ea7602,R.randint(0xa6539930bf6bff4584db8346b786151c91d1eac1fe9754bd25d5374e6376efae8a0000000000000000000000000000,0x5d8f062b6bacbf971abb79d7c73b6be01206140d1f351faa6547ef1c17f2e6d22da0000000000000000000000000000),R.randint(0x1ed09bead87c0378d8e6400000000,0x115557b419c5c1f3fa018400000000),Q.token_hex(nbytes=16)];I(A);I(F);I(G);I(H);I(J);S.windll.kernel32.SetConsoleTitleW(A)
def B2():J='rcs';I='radar';H='trigger';F='bhop';E='chams';C='glow';global o,p,AB;global q,z,A0;global AC,r,AD,s,t,u,AE,AF,AG,AH,AI,AJ,AK,AL,AM,AN,AO,AP;global AQ,v,AR,AS,AT;global AU,w;global AV,x;A=T.get('https://pastebin.com/raw/'+V,verify=G).json();o=B(A[F]['bhopEnable']);p=B(A[F]['bhopType']);AB=N(A[F]['bhopKey']);q=B(A[H]['triggerActive']);z=N(A[H]['triggerKey']);A0=D(A[H]['ShotDelay']);AC=B(A[C]['glowActive']);r=N(A[C]['glowToggleKey']);AD=B(A[C]['glowByHP']);s=B(A[C]['glowDefaultRed']);t=B(A[C]['glowDefaultGreen']);u=B(A[C]['glowDefaultBlue']);AE=D(A[C]['glowAlpha']);AF=B(A[C]['glowDefusingRed']);AG=B(A[C]['glowDefusingGreen']);AH=B(A[C]['glowDefusingBlue']);AI=B(A[C]['glowMidHp']);AJ=B(A[C]['glowMidColorRed']);AK=B(A[C]['glowMidColorGreen']);AL=B(A[C]['glowMidColorBlue']);AM=B(A[C]['glowLowHp']);AN=B(A[C]['glowLowColorRed']);AO=B(A[C]['glowLowColorGreen']);AP=B(A[C]['glowLowColorBlue']);AQ=B(A[E]['chamsActive']);v=N(A[E]['chamsToggleKey']);AR=B(A[E]['chamsRed']);AS=B(A[E]['chamsGreen']);AT=B(A[E]['chamsBlue']);AU=B(A[I]['radarActive']);w=N(A[I]['radarToggleKey']);AV=B(A[J]['rcsActive']);x=N(A[J]['rcsToggleKey'])
def B3():P.system(B8);I('User:',b(Y,B9));I('Version:',b('1.8 BETA','magenta'))
def B4(first,second):
	if W(first)or W(second):return G
	else:return H
def B5(x,y):
	if x>89:return G
	elif x<-89:return G
	elif y>360:return G
	elif y<-360:return G
	else:return H
def B6(viewAngleX,viewAngleY):
	B=viewAngleY;A=viewAngleX
	if A>89:A-=360
	if A<-89:A+=360
	if B>180:B-=360
	if B<-180:B+=360
	return A,B
def B7(current_x,current_y,new_x,new_y):
	A=new_x-current_x
	if A<-89:A+=360
	elif A>89:A-=360
	if A<O:A=-A
	B=new_y-current_y
	if B<-180:B+=360
	elif B>180:B-=360
	if B<O:B=-B
	return A,B
def AW(localpos1,localpos2,localpos3,enemypos1,enemypos2,enemypos3):
	try:
		A=localpos1-enemypos1;B=localpos2-enemypos2;C=localpos3-enemypos3;E=sqrt(A*A+B*B+C*C);F=asin(C/E)*57.295779513082;D=atan(B/A)*57.295779513082
		if A>=O:D+=180.0
	except:return 0,0
	return F,D
def A1():
	if j in A6.text:
		B1();B0();B2();B3();Q=H;S=H;T=H;U=H;y=O;z=O
		while H:
			AX=1;BA=5;BB=H;A0=8;AY=3;AZ=None;Aa=111111111111;Ab=111111111111
			if not A_(A5.GetForegroundWindow()).decode('cp1252')=='Counter-Strike: Global Offensive - Direct3D 9':E.sleep(1);continue
			if K and A7 and A:
				try:B=A.read_int(K+Am);J=A.read_int(B+As);A1=A.read_int(B+Ar);BC=A.read_uint(K+A8+(A1-1)*16);Ac=A.read_uint(BC+l);N=A.read_uint(B+l);V=A.read_int(K+Ao);F=A.read_uint(A7+An);BD=A.read_uint(F+Ap)
				except:E.sleep(5);continue
			for BE in range(1,BD):
				C=A.read_uint(K+A8+BE*16)
				if C:
					try:W=A.read_int(C+At);d=A.read_int(C+l);BF=A.read_int(C+Av);X=A.read_int(C+Au);Ad=A.read_uint(C+Aq);BV=A.read_int(C+Az)
					except:E.sleep(2);continue
					if AC==1:
						if M.is_pressed(r)and Q==G:Q=H;E.sleep(0.3)
						elif M.is_pressed(r)and Q==H:Q=G;E.sleep(0.3)
						if Q:
							Y,Z,a=D(s/255),D(t/255),D(u/255)
							if d!=N and not Ad:
								if AD==1:
									if X>50:Y,Z,a=D(s/255),D(t/255),D(u/255)
									if X<AI:Y,Z,a=D(AJ/255),D(AK/255),D(AL/255)
									if X<AM:Y,Z,a=D(AN/255),D(AO/255),D(AP/255)
								if BF:Y,Z,a=D(AF/255),D(AG/255),D(AH/255)
								A.write_float(V+W*56+8,D(Y));A.write_float(V+W*56+12,D(Z));A.write_float(V+W*56+16,D(a));A.write_float(V+W*56+20,D(AE));A.write_int(V+W*56+40,1)
					if AX==1 and N!=d and X>0:
						A2=A.read_uint(C+Ay);BG=A.read_float(F+L);BH=A.read_float(F+L+4);Ae=A.read_float(B+n);Af=A.read_float(B+n+4);BI=A.read_float(B+Ax+8);Ag=A.read_float(B+n+8)+BI
						try:Ah=A.read_float(A2+48*A0+12);Ai=A.read_float(A2+48*A0+28);Aj=A.read_float(A2+48*A0+44)
						except:continue
						BJ,BK=AW(Ae,Af,Ag,Ah,Ai,Aj);A3,A4=B7(BG,BH,BJ,BK)
						if A3<Aa and A4<Ab and A3<=AY and A4<=AY:Aa,Ab=A3,A4;AZ,BL,BM=C,X,Ad;BN,BO,BP=Ah,Ai,Aj
					if AX==1 and i(BA)!=0 and B:
						if AZ and BL>0 and not BM:
							BQ,BR=AW(Ae,Af,Ag,BN,BO,BP);Ak,Al=B6(BQ,BR);e=A.read_float(B+c);f=A.read_float(B+c+4)
							if BB and A.read_uint(B+AA)>1:A.write_float(F+L,Ak-e*2);A.write_float(F+L+4,Al-f*2)
							else:A.write_float(F+L,Ak);A.write_float(F+L+4,Al)
					if AQ==1:
						if M.is_pressed(v)and S==G:S=H;E.sleep(0.3)
						elif M.is_pressed(v)and S==H:S=G;E.sleep(0.3)
						if S:
							if d!=N:A.write_int(C+m,AR);A.write_int(C+m+1,AS);A.write_int(C+m+2,AT)
					if AU==1:
						if M.is_pressed(w)and T==G:T=H;E.sleep(0.3)
						elif M.is_pressed(w)and T==H:E.sleep(0.05);T=G;E.sleep(0.3)
						if T:
							if d!=N:A.write_int(C+Aw,1)
			if M.is_pressed(AB):
				if o==1 and p==1:
					if B and J and J==257 or J==263:A.write_int(K+k,6)
				if o==1 and p==2:
					if B and J and J==257 or J==263:BS=R.randint(0,5);E.sleep(BS/100);A.write_int(K+k,5);E.sleep(0.08);A.write_int(K+k,4)
			if q==1:
				if i(5)!=0:
					if 0<A1<=64 and N!=Ac:A.write_int(K+A9,6);E.sleep(0.2)
			if q==1:
				if i(18)!=0:
					if 0<A1<=64 and N!=Ac:A.write_int(K+A9,6);E.sleep(0.2)
			if AV==1:
				if M.is_pressed(x)and U==G:U=H;E.sleep(0.3)
				elif M.is_pressed(x)and U==H:U=G;E.sleep(0.3)
				if U:
					if A.read_uint(B+AA)>2:
						BT=A.read_float(F+L);BU=A.read_float(F+L+4);e=A.read_float(B+c);f=A.read_float(B+c+4);g=BT-(e-y)*2;h=BU-(f-z)*2;y=e;z=f
						if B4(g,h)and B5(g,h):A.write_float(F+L,g);A.write_float(F+L+4,h)
					else:y=O;z=O;g=O;h=O
	else:P.system(B8);I('HWID ERROR!');I(b(j,'red'));I('Please contact:',b('Ruslan#7905',B9));P.system('pause >NUL')
if __name__=='__main__':A1()