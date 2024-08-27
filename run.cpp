#include <windows.h>
#include <iostream>

int main() {
    // 定义要执行的命令
    std::wstring command = L"pythonw.exe -m onepitranslator";

    // 设置启动信息和进程信息
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;

    // 创建进程执行命令
    if (!CreateProcess(NULL, const_cast<LPWSTR>(command.c_str()), NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        std::cerr << "Failed to run onepitranslator" << std::endl;
        return 1;
    }

    // 关闭进程和线程句柄
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    // 程序启动后，关闭自身
    return 0;
}
