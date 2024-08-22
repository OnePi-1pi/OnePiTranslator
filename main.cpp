#include <windows.h>
#include <string>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd) {
    // 通配符模式
    std::wstring pattern = L".\\src\\onepitranslator.py*";
    WIN32_FIND_DATA findFileData;
    HANDLE hFind = FindFirstFile(pattern.c_str(), &findFileData);

    if (hFind == INVALID_HANDLE_VALUE) {
        MessageBox(NULL, L"no such file", L"error", MB_OK);
        return 1;
    }

    std::wstring filename = findFileData.cFileName;
    std::wstring command = L"pythonw.exe .\\src\\" + filename;

    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;

    if (!CreateProcess(NULL,   
        const_cast<LPWSTR>(command.c_str()), 
        NULL, 
        NULL,  
        FALSE, 
        0,      
        NULL, 
        NULL, 
        &si,   
        &pi)  
        ) {
        MessageBox(NULL, L"failed to run one pi translator", L"error", MB_OK);
        return 1;
    }

    // 关闭句柄
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    // 关闭搜索句柄
    FindClose(hFind);

    return 0;
}
