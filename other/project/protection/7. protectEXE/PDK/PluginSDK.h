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

//插件类型唯一，不可同时设置多种：
//NORMAL类型插件，在壳体代码初始化完成后、主程序启动前执行，可以使用壳提供的API
//BEFORE_LICENSING类型插件，在壳体代码初始化完成前执行，不可以使用壳提供的API
//GET_LICENSE类型插件，DllMain返回授权文件信息，结构如下：
//typedef struct _GET_LICENSE_STRUCT {
//	void* pKeyBuf;
//	DWORD dwKeySize;
//} GET_LICENSE_STRUCT, *PGET_LICENSE_STRUCT;
//
//pKeyBuf由插件分配内存，并可在DllMain(DLL_PROCESS_DETACH)中释放
//
//NO_PROTECT表示不保护插件代码，可与插件类型同时设置
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