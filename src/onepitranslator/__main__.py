# src/onepitranslator/__main__.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing as mp
from onepitranslator import onepi
import os
import subprocess

def main():
    first_run_marker = os.path.expanduser('~/.onepitranslator_first_run')
    if not os.path.exists(first_run_marker):
        # 检查是否已经创建了快捷方式
        if not os.path.exists(os.path.expanduser('~/Desktop/OnePiTranslator.lnk')) and \
           not os.path.exists(os.path.expanduser('~/Desktop/OnePiTranslator.desktop')):
            # 如果快捷方式不存在，则创建
            subprocess.run(['onepitranslator-create-shortcut'], check=True)
        
        # 创建标记文件，表示已运行过
        with open(first_run_marker, 'w') as f:
            f.write('This file indicates that OnePiTranslator has been run for the first time.')
    
    mp.set_start_method('spawn')
    onepi.main()
if __name__ == "__main__":
    main()
