#pragma once

typedef struct _SHELL_CONTEXT
{
	void* pLinkerClass;
	void* pMemoryClass;
	void* pPluginHookList;
	IMAGE_NT_HEADERS* pNTHeaders;
	IMAGE_SECTION_HEADER* pSectionHeader;
} SHELL_CONTEXT, *PSHELL_CONTEXT;

typedef struct _HOOK_ENTRY
{
	DWORD Offset;
	DWORD Length;
} HOOK_ENTRY, *PHOOK_ENTRY;

#define NORMAL				0x00000001
#define BEFORE_LICENSING	0x00000002
#define NO_PROTECT			0x00000004
#define GET_LICENSE			0x00000008

//�������Ψһ������ͬʱ���ö��֣�
//NORMAL���Ͳ�����ڿ�������ʼ����ɺ�����������ǰִ�У�����ʹ�ÿ��ṩ��API
//BEFORE_LICENSING���Ͳ�����ڿ�������ʼ�����ǰִ�У�������ʹ�ÿ��ṩ��API
//GET_LICENSE���Ͳ����DllMain������Ȩ�ļ���Ϣ���ṹ���£�
//typedef struct _GET_LICENSE_STRUCT {
//	void* pKeyBuf;
//	DWORD dwKeySize;
//} GET_LICENSE_STRUCT, *PGET_LICENSE_STRUCT;
//
//pKeyBuf�ɲ�������ڴ棬������DllMain(DLL_PROCESS_DETACH)���ͷ�
//
//NO_PROTECT��ʾ������������룬����������ͬʱ����
//

typedef DWORD (__stdcall *pfnAddPluginHook)(SHELL_CONTEXT* Context, HOOK_ENTRY NewHookEntry);
typedef DWORD (__stdcall *pfnGetPluginFuncRVA)(SHELL_CONTEXT* Context, char* FuncName);


void WINAPI InitPluginSettings(char* pFileName);
BOOL WINAPI GetPluginEnabled();
void WINAPI PluginProcess(BYTE* pImageBuf, pfnAddPluginHook fnAddPluginHook, pfnGetPluginFuncRVA fnGetPluginFuncRVA, SHELL_CONTEXT* Context);
DWORD WINAPI GetPluginContextSize();
void WINAPI GetPluginContext(void* pContext);
void WINAPI GetPluginBinName(char* pNameBuf, DWORD Size);
DWORD WINAPI GetPluginType();
void WINAPI ShowPluginOptions();