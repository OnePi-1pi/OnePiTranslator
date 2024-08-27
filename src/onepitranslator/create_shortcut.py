import os
import sys
import subprocess
import sysconfig

def get_desktop_path():
    try:
        # 使用 xdg-user-dir 获取桌面路径
        result = subprocess.check_output(['xdg-user-dir', 'DESKTOP'], encoding='utf-8')
        return result.strip()  # 移除可能的换行符
    except subprocess.CalledProcessError:
        # 如果命令失败，返回默认的桌面路径
        return os.path.join(os.path.expanduser('~'), 'Desktop')

def create_shortcut():
    if sys.platform == 'win32':
        import win32com.client
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        path = os.path.join(desktop, "OnePiTranslator.lnk")

        target = os.path.join(sys.prefix, 'share', 'onepitranslator', 'run.exe')
        wDir = os.path.dirname(target)

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = target
        shortcut.save()
    else:
        desktop = get_desktop_path()
        icon_path = os.path.join(sysconfig.get_path('purelib'),'onepitranslator','resources','images','icon.png')

        # 使用用户的本地应用程序目录
        local_app_dir = os.path.join(os.path.expanduser('~'), '.local', 'share', 'applications')
        if not os.path.exists(local_app_dir):
            os.makedirs(local_app_dir)  # 如果目录不存在，则创建它

        desktop_entry = f"""
        [Desktop Entry]
        Name=OnePiTranslator
        Exec={sys.executable} -m onepitranslator
        Icon={icon_path}
        Type=Application
        Terminal=false
        """
        desktop_file_path = os.path.join(local_app_dir, "OnePiTranslator.desktop")
        with open(desktop_file_path, 'w') as desktop_file:
            desktop_file.write(desktop_entry)

        os.chmod(desktop_file_path, 0o755)

        # 创建桌面符号链接
        desktop_link_path = os.path.join(desktop, "OnePiTranslator.desktop")
        if not os.path.exists(desktop_link_path):
            os.symlink(desktop_file_path, desktop_link_path)

        # 更新桌面数据库
        subprocess.run(['update-desktop-database', local_app_dir], check=True)

if __name__ == "__main__":
    create_shortcut()