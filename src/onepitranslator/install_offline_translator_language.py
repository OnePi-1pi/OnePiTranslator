#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def read_json_file(file_path):
    try:
        file_path = Path(__file__).parent /file_path
        if file_path.exists():
            with open(file_path, "r",encoding="utf_8") as file:
                data = json.load(file)
            return data
        else:
            return False
    except Exception :
        #print($1)
        return False


def install_packages(paths, progress_bar):
    progress_bar['maximum'] = len(paths)
    progress_bar['value'] = 0
    try:
        for index, path in enumerate(paths, 1):
            package.install_from_path(path)
            progress_bar['value'] = index
            progress_bar.update_idletasks()  # 更新进度条显示,保持刷新
    except Exception as e:
        m1=MessageCatalog.translate("错误")
        m2=MessageCatalog.translate("无法从")
        m3=MessageCatalog.translate("安装")
        



        Messagebox.show_error(f'{m1}{m2}{path}{m3}:{e}')

def show_supported_languages():
    installed_packages = package.get_installed_packages()
    dlangins = []
    for item in installed_packages:
        k,v=str(item).split(' → ')
        dlangins.append([k.lower(),v.lower()])
    ll2,ll1 = [],[]
    for i in dlangins:
        j=list(reversed(i))
        ll2.extend([i,j]);dlangins.remove(j) if j in dlangins else ll1.append(i)
    ll2.extend(ll1)
    print(ll2)
    lla = ''
    for i,s in enumerate(ll2):
         lla +=(f'{MessageCatalog.translate(s[0])} → {MessageCatalog.translate(s[1])}\t')
         if  i & 1 :
            lla +='\n'
    m4=MessageCatalog.translate("Language packs installed")
    m5=MessageCatalog.translate("Installation completed.")
    m6=MessageCatalog.translate("Supported languages")
    Messagebox.show_info(f'{m4}' f'{m5}.\n\n{m6}:\n{lla}')

def select_folder():
    selected_folder = filedialog.askdirectory(initialdir=Path(__file__).parent /'argos_languages_package')
    if selected_folder:
        paths = [path.path for path in os.scandir(selected_folder) ]

        progress_bar = ttk.Progressbar(root, orient='horizontal',  mode='determinate')
        progress_bar.pack(fill='x',side='bottom',ipady= 10,padx = 10, pady=20)
        lable1=ttk.Label(root,text='⏳',font=("Default",40))
        lable1.pack(side='bottom',after=progress_bar,ipady= 10,padx = 0, pady=20)
        install_packages(paths, progress_bar)
        show_supported_languages()
    
global ttk ,package,MessageCatalog,filedialog,Path,Messagebox,json,os,root
def main():
    import ttkbootstrap as ttk
    import argostranslate.package as package
    from ttkbootstrap.localization import MessageCatalog
    from tkinter import filedialog
    from pathlib import Path
    from ttkbootstrap.dialogs.dialogs import Messagebox
    import json
    import os
    global root
    root = ttk.Window()
    MessageCatalog.load(Path(__file__).parent / 'languages')
    cond=read_json_file('config.json')
    if cond:
        l = cond.get('option_lang','en')
        if l :
            MessageCatalog.locale(l)
    root.title(MessageCatalog.translate("Install Language Pack"))
    screen_width ,screen_height= root.winfo_screenwidth(),root.winfo_screenheight()
    root.geometry(f'{screen_width//4}x{screen_height//4}+{int(3*screen_width / 8)}+{int(3*screen_height /8 )}')
    entry = ttk.Entry(root)
    entry.pack(fill='x')
    entry.insert(0,'''Down Load ⬇️ https://github.com/argosopentech/argos-translate?tab=readme-ov-file#packages''')    
    ttk.Button(root, text=MessageCatalog.translate("Select the folder where the language file (zip) is located"), command=select_folder).pack(expand=False, fill=None, padx=20, pady=20, ipadx=50, ipady=50)
    root.mainloop()

if __name__ == "__main__":

    main()
