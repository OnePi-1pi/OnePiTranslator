#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import math
import signal
import qrcode
import requests
import threading
import webbrowser
import subprocess
import regex as re
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap import font
from tkinter import filedialog 
from ttkbootstrap.constants import *
from multiprocessing import Process,Event
from onepitranslator import choose_translate
from PIL import Image,ImageTk,ImageFont,ImageDraw
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.dialogs.dialogs import FontDialog
from ttkbootstrap.localization import MessageCatalog
from onepitranslator import install_offline_translator_language as inslang


class TranslationApp:
    def __init__(self, master):
        # 初始化方法,创建主窗口和布局 框架
          # 保存传入的主窗口引用
        self.selected_translator = ttk.StringVar(value=config_dict.get("selected_translator", ""))
        self.selected_fromlang = ttk.StringVar(value=config_dict.get("selected_fromlang", ""))
        self.selected_tolang = ttk.StringVar(value=config_dict.get("selected_tolang", ""))
        self.selected_key = ttk.IntVar(value=config_dict.get("selected_key", 0))
        self.set_checkw = ttk.IntVar(value=config_dict.get("hidden_key",0))
        self.scale_time = ttk.DoubleVar(value=config_dict.get("time", 0))
        self.root = master
        self.root.bind("<Configure>", master.after(40,self.root.update_idletasks()))  
        root.resizable(True,  True)

        root.title(MessageCatalog.translate("One pi File Name Batch Translator"))
        # 右键点击窗口时,使正在选择的treeview对象重置状态
        # root.bind("<Button-3>", lambda event: (root.focus_set(), self.tree.selection_set()))
        panedwindow = ttk.PanedWindow(root, orient="vertical")
        panedwindow.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        # 创建三个横向的 Frame,用于布局管理
        # 创建三个横向的 Frame,并设置大小
        frame1 = ttk.Frame(panedwindow)
        frame1.place(relx=0.0, rely=0.0, relheight=0.12, relwidth=1.0)


        frame2 = ttk.Frame(panedwindow)
        frame2.place(relx=0.0, rely=0.12, relheight=0.08, relwidth=1.0)


        frame3 = ttk.Frame(panedwindow)
        frame3.place(relx=0.0, rely=0.2, relheight=0.8, relwidth=1.0)

        font_dialog = FontDialog(root)

        # 将三个 Frame 添加到根容器中,并设置布局属性
        # 配置主窗口的行和列权重,使得各部分能够合理分配空间
        # 创建 Labelframe 组件,分别用于放置主题和字体设置以及翻译设置\
        labelframe0 = ttk.Frame(frame1,borderwidth=0  )
        labelframe1 = ttk.Frame(frame1,borderwidth=0 )
        labelframe2 = ttk.Labelframe(frame1,labelanchor="n", text=MessageCatalog.translate("Translation Settings"), borderwidth=0 )

        # 将 Labelframe 组件添加到第一个 Frame 中
        self.style=ttk.Style()
        labelframe0.place(relx=0.0, rely=0.0, relheight=0.35, relwidth=0.4, bordermode="inside")
        labelframe1.place(relx=0.0, rely=0.35, relheight=0.65, relwidth=0.4, bordermode="inside")
        labelframe2.place(relx=0.4, rely=0.0, relheight=1.0, relwidth=0.6, bordermode="inside")
    ##########################################frame1############################################################
        #++++++++++++++++++++++++++++++++++labelframe0++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #____________________________"标题"title_____________________________________________#
        title=ttk.Label(labelframe0,text=MessageCatalog.translate("Welcome to use One Pi Multi-functional Translator, click the function buttons below to switch interfaces"),bootstyle="danger")
        title.pack(fill=X,expand=1,side=TOP)
        #++++++++++++++++++++++++++++++++++labelframe1"主题和字体"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #____________________________MessageCatalog.translate("Theme Selection")themeframe_____________________________________________#
        theme_menu = ttk.Menu(root, tearoff=0)
        # 遍历翻译,为下拉菜单添加每个选项,使用 lambda 函数关联每个选项的命令
        for theme in self.style.theme_names():
            # 使用 lambda 函数将每个主题与对应的命令关联,当选中主题时应用该主题
            theme_menu.add_radiobutton(label=theme, command=lambda th=theme : ( self.style.theme_use(th),theme_select.configure(text=th),update_font(),self.update_treeview_styles()))
        
        set_theme = config_dict.get("user_theme",DEFAULT_THEME)
        self.style.theme_use(set_theme)
        # 创建一个 Menubutton 组件,用于选择翻译引擎
        themeframe = ttk.Labelframe(labelframe1, text=MessageCatalog.translate("Theme Selection"), padding=10, bootstyle="primary"        )
        themeframe.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.4, bordermode="inside")
        theme_select = ttk.Menubutton(themeframe, text=set_theme,menu=theme_menu, bootstyle="success")
        # 将 Menubutton 放置在界面的左侧,设置外边距为5像素
        theme_select.pack( padx=5,fill=BOTH,expand=1)

        #____________________________字体大小FontSizeFrame_____________________________________________#
        FontSizeFrame = ttk.Labelframe(labelframe1,labelanchor="n", text=MessageCatalog.translate("Font Size Selection"),bootstyle="success"        )
        FontSizeFrame.place(relx=0.42, rely=0.0, relheight=1.0, relwidth=0.25, bordermode="inside")
        # 创建字体大小选择的 Spinbox 组件
        font_size_spinbox = ttk.Spinbox(FontSizeFrame,from_=0,to=72, bootstyle="info")
        self.font_size_spinbox = font_size_spinbox
        font_size_spinbox.pack(padx=5,pady=2,fill='x',expand=1)
        font_box = ttk.Button(FontSizeFrame,text='font' ,bootstyle="danger")
        font_box.pack(padx=5,pady=2,fill='x',expand=1)
        #............... 定义更新字体大小的函数......................

        self.font_size = ttk.IntVar()
        self.font_weight = ttk.StringVar()
        def update_font(event=None):
            global font_now
            #获得默认字体字典
            font_now_name = self.style.lookup('.','font')
            # style.map('.',font={'size':font_size_val,'weight':font_weight_val})
            if font_now_name:
                font_now_dic = font.Font(name=font_now_name,exists=True).actual()
                font_size_val = int(font_size_spinbox.get() or font_now_dic['size'])
                font_weight_val = self.font_weight.get() or font_now_dic['weight']
                font_now_dic.update({'size':font_size_val,'weight':font_weight_val})
                font_now = font.Font(**font_now_dic)
            else:
                default_font = font.Font().actual()
                #获得用户设置初始值或默认初始值
                usr_font_size = config_dict.get("font_size",default_font['size'])
                usr_font_weight = config_dict.get("font_weight",default_font['weight'])
                #查看现在字体大小设置框是否有值,无值则填写默认值
                font_size_val = int(font_size_spinbox.get() or usr_font_size)
                font_weight_val = self.font_weight.get() or usr_font_weight
                font_now = font.Font(**{'size':font_size_val,'weight':font_weight_val})
                

            #设置字体大小变量和设置框为当前值
            self.font_size.set(font_size_val)
            font_size_spinbox.set(font_size_val)
            #查看现在字体加粗是否选择,无值则为默认
            self.font_weight.set(font_weight_val)
            #设置全部件style为只修改大小和加粗
            self.style.configure('.',font=font_now)
            font_now_name = self.style.lookup('.','font')
            font_now_dic = font.Font(name=font_now_name,exists=True).actual()

            for i in [self.note1,self.label_alipay_text,self.label_wechat_text,self.label_bili_text,self.label_douyin_text,self.note2]:
                i.configure(font=f'-size {font_size_val+5}')
            self.adjust_row_height()
            # if style.lookup('.','font'):
            #     print(style.lookup('.','font'))
            #     print(font.Font(name=style.lookup('.','font'),exists=True).actual())
        def change_font(event=None):
            
            # 显示对话框并获取结果
            font_dialog.show()

            # 获取字体设置
            font_settings = font_dialog.result

            if font_settings:
                # 解析字体设置
                font_size_val = font_settings.cget("size")
                font_weight_val = font_settings.cget("weight")

                # 更新组件的字体
                self.style.configure('.',font=font_settings)
                # title.configure(font=new_font)
                for i in [self.note1, self.label_alipay_text, self.label_wechat_text, self.label_bili_text, self.label_douyin_text]:
                    i.configure(font=f'-size {font_size_val+5}')

                # 调整行高等布局
                self.adjust_row_height()

                # 更新字体大小 Spinbox 的显示值
                self.font_size.set(font_size_val)
                font_size_spinbox.set(font_size_val)
                self.font_weight.set(font_weight_val)
            else:
                print("Font settings are not available.")







        # 配置 Spinbox 的 command 属性,使其在值发生变化时调用 update_font_size 函数
        font_box.config(command=change_font)
        font_size_spinbox.config(command=update_font)
        font_size_spinbox.bind("<Return>",update_font)
        #____________________________"字体粗细"FontWeightFrame_____________________________________________#
        FontWeightFrame = ttk.Labelframe(labelframe1,labelanchor="n", text=MessageCatalog.translate("Font Style"), bootstyle="info")
        FontWeightFrame.place(relx=0.7, rely=0.0, relheight=1, relwidth=0.28, bordermode="inside")
        opt_normal = ttk.Radiobutton(
        master=FontWeightFrame,
        text=MessageCatalog.translate("Normal"),
        value="normal",
        variable=self.font_weight,
        bootstyle="primary",
        command=update_font)
        opt_normal.pack(side=LEFT,fill=BOTH,expand=1, padx=2, pady=2)
        opt_bold = ttk.Radiobutton(
        master=FontWeightFrame,
        text=MessageCatalog.translate("Bold"),
        value="bold",
        variable=self.font_weight,
        bootstyle="warning",
        command=update_font)
        opt_bold.pack(side=LEFT,fill=BOTH,expand=1, padx=2, pady=2)
        #++++++++++++++++++++++++++++++++++labelframe2++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #__________________________engine_selectMessageCatalog.translate("Translation Engine")_______________________________________________#
        engine_menu = ttk.Menu(root, tearoff=0)
        # 遍历翻译引擎字典,为下拉菜单添加每个引擎选项,使用 lambda 函数关联每个选项的命令
        for name in translation_engines :
            tena = MessageCatalog.translate(name)
            engine_menu.add_radiobutton(label= tena,value=name,variable=self.selected_translator, command=lambda n=tena:( self.engine_select.configure(text=n),self.update_language_menus()))
        # 创建一个 Menubutton 组件,用于选择翻译引擎
        engineframe = ttk.Labelframe(labelframe2,labelanchor="n", text=MessageCatalog.translate("Translation Engine"), padding=1, bootstyle="warning")
        engineframe.place(relx=0.02, rely=0.3, relheight=0.95, relwidth=0.21, bordermode="inside")

        usr_engine = config_dict.get("engine","GoogleTranslator")
        self.engine_select = ttk.Menubutton(engineframe, text=MessageCatalog.translate(usr_engine),menu=engine_menu, bootstyle="primary")
        self.engine_select.pack( fill=BOTH,padx=1,pady=12,expand=1)
        self.selected_translator.set(usr_engine)
        #______________________________source_lang_selectMessageCatalog.translate("Source language")___________________________________________#
        self.source_lang_menu = ttk.Menu(root, tearoff=0)
        self.target_lang_menu = ttk.Menu(root, tearoff=0)
        # 创建一个 Menubutton 组件,用于选择
        slframe = ttk.Labelframe(labelframe2,labelanchor="n", text=MessageCatalog.translate("Source language"), padding=1,bootstyle="primary"        )
        slframe.place(relx=0.27, rely=0.3, relheight=0.95, relwidth=0.21, bordermode="inside")

        usr_source_lang = config_dict.get("source_lang","")
        self.source_lang_select = ttk.Menubutton(slframe, text=MessageCatalog.translate(usr_source_lang),menu=self.source_lang_menu, bootstyle="info")
        # 将 Menubutton 放置,设置外边距为5像素
        self.source_lang_select.pack( fill=BOTH,padx=1,pady=12,expand=1)
        self.selected_fromlang.set(usr_source_lang)
        #____________________________self.target_lang_selectMessageCatalog.translate("Target Language")_____________________________________________#

        # 创建一个 Menubutton 组件,用于选择
        tgframe = ttk.Labelframe(labelframe2,labelanchor="n", text=MessageCatalog.translate("Target Language"), padding=1, bootstyle="info"        )
        tgframe.place(relx=0.52, rely=0.3, relheight=0.95, relwidth=0.21, bordermode="inside")

        self.local_code=MessageCatalog.locale() or "en"
        self.local_lang = local_dict.get(self.local_code)
        usr_target_lang =config_dict.get("target_lang",self.local_lang)
        self.target_lang_select = ttk.Menubutton(tgframe, text=MessageCatalog.translate(usr_target_lang),menu=self.target_lang_menu, bootstyle="success")
        # 将 Menubutton 放置,设置外边距为5像素
        self.target_lang_select.pack( fill=BOTH,padx=1,pady=12,expand=1)
        self.selected_tolang.set(usr_target_lang)
        self.update_language_menus()
        #__________________________Self_Lang_SelectMessageCatalog.translate("Interface Display Language")_______________________________________________#
        lang_menu = ttk.Menu(root, tearoff=0)
        # 遍历语言选项列表,为下拉菜单添加每个语言选项,使用 lambda 函数关联每个选项的命令
        set_option_lang = config_dict.get("option_lang",self.local_code)
        for lang ,langt in lang_options.items():
            if langt == set_option_lang or langt == set_option_lang[0:2]:set_option_lang,langt=lang,set_option_lang
            lang_menu.add_radiobutton(label=lang,value=langt, command=lambda l=lang,v=langt: (Self_Lang_Select.configure(text=l),switch_language(v)))
        # 创建一个 Menubutton 组件,用于选择语言
        SelfLangFrame = ttk.Labelframe(labelframe2,labelanchor="n", text=" Display Language", padding=1,bootstyle="success"        )
        SelfLangFrame.place(relx=0.77, rely=0.3, relheight=0.95, relwidth=0.21, bordermode="inside")
        
        Self_Lang_Select = ttk.Menubutton(SelfLangFrame, text=set_option_lang,menu=lang_menu, bootstyle="dark")
        # 将 Menubutton 放置在界面的左侧,设置外边距为5像素
        Self_Lang_Select.pack( fill=BOTH,padx=1,pady=12,expand=1)

    ########################### frame2 #################################
        #++++++++++++++++++++++++++++++++++labelframe3++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # _____________________________功能选择buttons____________________________________________#
        # 创建一个 Labelframe 组件,用于包含功能选择相关的控件
        labelframe3 = ttk.Labelframe(frame2,labelanchor="n", text=MessageCatalog.translate("Function Selection"),bootstyle="primary")
        labelframe3.place(relx=0, rely=0, relheight=1, relwidth=0.6, bordermode="inside")
        # Labelframe3 内容
        # 创建一个复选框组件列表,用于存储功能选择相关的控件
        self.buttons = [
            ttk.Checkbutton(labelframe3, text=MessageCatalog.translate("Filename Translation"), bootstyle="primary-toolbutton", command=lambda: self.show_frame(1)),
            ttk.Checkbutton(labelframe3, text=MessageCatalog.translate("File Content Translation"), bootstyle="warning-toolbutton", command=lambda: self.show_frame(2)),
            ttk.Checkbutton(labelframe3, text=MessageCatalog.translate("Text Translation"), bootstyle="info-toolbutton", command=lambda: self.show_frame(3)),
            ttk.Checkbutton(labelframe3, text=MessageCatalog.translate("Options and Settings"), bootstyle="success-toolbutton", command=lambda: self.show_frame(4)),
        ]

        for i,button in enumerate(self.buttons):
            button.place(relx=0.03+i*0.24, rely=0.05, relheight=0.7, relwidth=0.21)
        #++++++++++++++++++++++++++++++++++labelframe4辅助选项++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # _____________________________辅助选项buttons____________________________________________#
        # 创建一个 Labelframe 组件,用于包含辅助选项相关的控件
        labelframe4 = ttk.Labelframe(frame2,labelanchor="n", text=MessageCatalog.translate("Auxiliary Options"),bootstyle="success")
        labelframe4.place(relx=0.6, rely=0, relheight=1, relwidth=0.4, bordermode="inside")
        #.................................................................
        set_time = config_dict.get("time",0)
        #print(set_time)
        scale =self.create_scale(labelframe4, "interval",set_time)
        scale.place(relx=0.05, rely=0, relheight=1, relwidth=0.4)
        self.scale=scale
        # 创建一个复选框组件,用于逐个翻译选项
        set_singal=ttk.IntVar(value=config_dict.get("singal_t",0))
        check1 = ttk.Checkbutton(labelframe4, text=MessageCatalog.translate("Translate one by one, warning,\n it will be very slow"),variable=set_singal ,bootstyle="danger-round-toggle")
        check1.place(relx=0.5, rely=0, relheight=0.5, relwidth=0.6)
        self.singaltrans=check1

        # 创建一个复选框组件,用于使用隐藏API密钥选项
        check2 = ttk.Checkbutton(labelframe4, text=MessageCatalog.translate("Hide API Key"),  bootstyle="primary-round-toggle",variable=self.set_checkw,command=self.hidden_key)
        check2.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.6)
        self.key=check2

    ##########################################frame3############################################################
        #++++++++++++++++++++++++++++++++++labelframe3++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # _____________________________功能选择buttons____________________________________________#
                        # Sizegrip组件,用于调整窗口大小
        sizegrip = ttk.Sizegrip(root,bootstyle="primary")
        # 将Sizegrip放置在窗口底部右侧
        sizegrip.pack(side=BOTTOM, anchor=SE)
        
        # 将内容框架添加到frame3中
        self.content_frame=frame3
        # 创建四个不同的Labelframe,并存储在字典frames中,每个Labelframe对应一个功能界面
        self.frames = {
            1: self.create_frame1(),
            2: self.create_frame2(),
            3: self.create_frame3(),
            4: self.create_frame4()
        }
        usr_frame=config_dict.get("frame",1)
        # 默认显示第一个功能界面
        self.show_frame(usr_frame)
        update_font()
        self.update_treeview_styles()
#***************************************init结束*********************************************************
    def select_all(self, event):
        # 阻止默认行为
        event.widget.tag_add("sel", "1.0", "end")
        return 
    #------------------------------显示隐藏框架----------------------------------
    def show_frame(self, frame_number):
        # 遍历self.frames字典,根据frame_number显示对应的功能界面,隐藏其他界面
        for key, frame in self.frames.items():
            if key == frame_number:
                frame.place(relx=0, rely=0., relheight=1, relwidth=1, bordermode="inside")  # 显示当前选择的功能界面,填充并扩展以填满可用空间
            else:
                frame.place_forget() # 隐藏非当前选择的功能界面
        # 取消所有按钮的选中状态
        for button in self.buttons:
            button.state(["!selected"])
        # 将当前选择的功能按钮设置为选中状态
        self.buttons[frame_number - 1].state(["selected"])   
    def create_frame1(self):
    ##########################################操作区frame1############################################################
        frame = ttk.Labelframe(self.content_frame,labelanchor="n",text=MessageCatalog.translate("Batch Filename Translation") ,bootstyle="success")
        # 创建Labelframe9,包含6个按钮和Meter部件
        labelframe9 = ttk.Labelframe(frame, bootstyle="success")
        labelframe10 = ttk.Labelframe(frame, text=MessageCatalog.translate("Display Bar"),labelanchor="n", bootstyle="info")
        labelframe9.place(relx=0, rely=0., relheight=0.15, relwidth=1)
        labelframe10.place(relx=0, rely=0.17, relheight=0.83, relwidth=1)
        # 1. 选择整个文件夹的全部文件Button
        #++++++++++++++++++++++++++++++++++labelframe3++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        button1 = ttk.Button(labelframe9, text=MessageCatalog.translate("Select All Files in the Entire Folder"), bootstyle="success",command=lambda : self.up_fnames(0)) # 选择文件夹并更新文件名列表  
        button1.place(relx=0.02, rely=0.02, relheight=0.4, relwidth=0.25)
        # 2. 选择多个文件Button
        button2 = ttk.Button(labelframe9, text=MessageCatalog.translate("Select Multiple Files"), bootstyle="info",command=lambda  :self.up_fnames(1))
        button2.place(relx=0.02, rely=0.58, relheight=0.4, relwidth=0.25)
        # 3. 开始翻译文件名Button
        button3 = ttk.Button(labelframe9, text=MessageCatalog.translate("Start Translating Filenames"), bootstyle="warning",command=self.translate_list)
        button3.place(relx=0.37, rely=0.02, relheight=0.4, relwidth=0.25)
        # 4. 添加/减去原始文件名Button
        button4 = ttk.Button(labelframe9, text=MessageCatalog.translate("Add/Remove Original Filename"), bootstyle="dark",command=self.add_or_sub)
        button4.place(relx=0.37, rely=0.58, relheight=0.4, relwidth=0.25)
        # 5. 开始重命名文件→Button
        button5 = ttk.Button(labelframe9, text=MessageCatalog.translate("Start Renaming Files→"), bootstyle="danger",command=self.rename_fnames)
        button5.place(relx=0.72, rely=0.02, relheight=0.4, relwidth=0.25)
        # 6. 回退为原文件名Button←
        button6 = ttk.Button(labelframe9, text=MessageCatalog.translate("Revert to original filename←"), bootstyle="primary",command = self.back_to_source_name)
        button6.place(relx=0.72, rely=0.58, relheight=0.4, relwidth=0.25)
        # 下半部分Labelframe10,显示部分,使用treeview填充
        
        self.tree = ttk.Treeview(labelframe10, columns=("col1", "col2", "col3"), show="headings",style="info.Treeview")
        # 绑定 Treeview 大小变化事件

        x_scroll = ttk.Scrollbar(labelframe10, orient=HORIZONTAL,command=self.tree.xview)
        x_scroll.pack(side=BOTTOM, fill=X)
        y_scroll = ttk.Scrollbar(labelframe10, orient=VERTICAL,command=self.tree.yview)
        y_scroll.pack(side=RIGHT, fill=Y)
        self.tree.configure( xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,cursor="crosshair")        

        # 设置列标题
        self.tree.heading("col1", text=MessageCatalog.translate("Original filename"), anchor=CENTER)
        self.tree.heading("col2", text=MessageCatalog.translate("Translate filename, double-click to modify"), anchor=CENTER)
        self.tree.heading("col3", text=MessageCatalog.translate("Actual filename"), anchor=CENTER)
        # 设置隔行颜色
        self.tree.tag_configure("even")
        self.tree.tag_configure("odd", background=root.style.colors.success,foreground='#ffffff')
        #事件对象在绑定事件时会被自动传递给函数on_value_change的第一个参数
        self.tree.bind("<Delete>", self.delete_selected_rows)
        self.tree.bind("<Double-1>", self.on_value_change)
                # 绑定右键点击事件
        self.tree.bind("<Button-3>", self.show_menu)
        self.tree.bind("<Control-a>", self.tree_select_all)
        self.tree.bind("<Configure>", self.debounce(self.adjust_row_height, 40))
        # 创建右键菜单
        self.context_menu = ttk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="删除", command=self.delete_selected_rows)
        self.context_menu.add_command(label="修改", command=self.on_value_change)
        self.context_menu.add_command(label="全选", command=self.tree_select_all)
        self.context_menu.add_command(label="清空", command=self.upviewtree)
        # 放置Treeview
        self.tree.pack(fill=BOTH, expand=1)

        return frame
    def create_frame2(self):
        frame = ttk.Labelframe(self.content_frame, text=MessageCatalog.translate("Batch file translation uses deep-translator's built-in method, which is not very good. \nIt can only translate plain text, cannot maintain formatting, and may be rewritten in the next update"),labelanchor="n" ,bootstyle="warning")
        # 创建Labelframe9,包含选择文件的按钮
        labelframe9 = ttk.Frame(frame,borderwidth=0 )
        labelframe9.pack(fill=X,  padx=5, pady=5)
        # 1. 选择多个文件Button
        button1 = ttk.Button(labelframe9, text=MessageCatalog.translate("Select Multiple Files"),command=lambda : self.up_files(1), bootstyle="info")
        button1.pack(side=LEFT,expand=1,  padx=10, pady=0)
        # 2. 选择整个文件夹的全部文件Button
        button2 = ttk.Button(labelframe9, text=MessageCatalog.translate("Select All Files in the Entire Folder"),command=lambda : self.up_files(2), bootstyle="success")
        button2.pack(side=LEFT,expand=1,  padx=10, pady=0)
        # 3. 开始翻译
        button3 = ttk.Button(labelframe9, text=MessageCatalog.translate("Start Translation"),command=self.translate_files, bootstyle="primary")
        button3.pack(side=LEFT,expand=1,  padx=10, pady=0)
        # 4. 清空列表
        button4 = ttk.Button(labelframe9, text=MessageCatalog.translate("Clear File List"),command=lambda e:self.up_files(3), bootstyle="danger")
        button4.pack(side=LEFT,expand=1,  padx=10, pady=0)

        self.p = ttk.Progressbar(frame,bootstyle="danger-striped",maximum=300,value=300)
        self.p.pack(side=BOTTOM,fill=X)        

        # 创建一个分为两列的Treeview控件,分别显示未翻译文件和已翻译文件 
        self.treeview_left = ttk.Treeview(frame, columns=("1"), show="headings",style="info.Treeview")
        self.treeview_right = ttk.Treeview(frame, columns=("1"), show="headings",style="info.Treeview")
        # 设置列标题
        self.treeview_left.heading("1", text=MessageCatalog.translate("Selected File"), anchor=CENTER)
        self.treeview_right.heading("1", text=MessageCatalog.translate("Translated File"), anchor=CENTER)
        self.treeview_left.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)
        self.treeview_right.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)
        # 设置隔行颜色

        self.treeview_left.tag_configure("even")
        self.treeview_left.tag_configure("odd", background=root.style.colors.primary,foreground='#ffffff')
        self.treeview_right.tag_configure("even")
        self.treeview_right.tag_configure("odd", background=root.style.colors.success,foreground='#ffffff')
        self.treeview_left.bind("<Delete>",lambda e: self.delete_tree_selected(self.treeview_left,nfts))


        return frame
    def create_frame3(self):
        frame = ttk.Labelframe(self.content_frame, text=MessageCatalog.translate("Text Translation"),labelanchor="n"        ,bootstyle="info")
        # 创建左右两个能同时输入和显示的框体,两个框体中间是两个翻译按钮分别是左右箭头,待实现xy两种滚动条
        text_left = ttk.ScrolledText(frame)
        text_left.place(relx=0, rely=0, relheight=1, relwidth=0.42)
        text_left.insert(1.0, MessageCatalog.translate("Enter the text to be translated here"))
        text_left.bind("<Control-a>", self.select_all)
        translation_button = ttk.Button(frame,bootstyle="info", text=MessageCatalog.translate("Translate"), command=self.translate_text)
        translation_button.place(relx=0.46, rely=0.4,relheight=0.08,relwidth=0.08)
        text_right = ttk.ScrolledText(frame)
        text_right.place(relx=0.58, rely=0, relheight=1, relwidth=0.42)
        text_right.insert(1.0, MessageCatalog.translate("Translation results will be displayed here"))
        text_right.bind("<Control-a>", self.select_all)
        self.text_left = text_left
        self.text_right = text_right
        return frame
    def create_frame4(self):
        frame = ttk.Labelframe(self.content_frame, text=MessageCatalog.translate("Options and Settings"), labelanchor="n", borderwidth=0, bootstyle="primary") 
        # 创建下拉菜单用于选择翻译器
        self.translator_menu = ttk.Menu(frame, tearoff=0)
        for index,name in enumerate(api_dict):            
            tana = MessageCatalog.translate(name)
            if index == self.selected_key.get():initname,ininame = tana , name
            self.translator_menu.add_radiobutton(label=tana, value=index,variable = self.selected_key , command=lambda t=tana,n=name: self.creat_api_options(t,n))
        
        # 创建用于显示翻译器选项的Frame
        self.translator_options_frame = ttk.Labelframe(frame,text=MessageCatalog.translate("Set translator api_key"), bootstyle="success")
        self.translator_options_frame.place(relx=0, rely=0.02, relheight=0.4, relwidth=1, bordermode="inside")

        self.translator_select = ttk.Menubutton(self.translator_options_frame,  menu=self.translator_menu, bootstyle="info")
        self.translator_select.place(relx=0.01, rely=0.4, relheight=0.2, relwidth=0.14, bordermode="inside")

        save_api_key_button = ttk.Button(self.translator_options_frame, text=MessageCatalog.translate("Save API Key"), bootstyle="Danger",command=save_api_keys_to_file)
        save_api_key_button.place(relx=0.9, rely=0.4, relheight=0.2, relwidth=0.09,  bordermode="inside")

        self.middle_frame = ttk.Frame(frame)
        self.middle_frame.place(relx=0, rely=0.44, relheight=0.08, relwidth=1, bordermode="inside")
        # 安装本地翻译语言库Button(bootstyle="Success")的按钮,从网络下载关联模块的按钮Button(bootstyle="Primary")
        install_lang_library_button = ttk.Button(self.middle_frame, text=MessageCatalog.translate("Install Local Translation Language Library"), bootstyle="Success",command=inslang.main)
        install_lang_library_button.pack(side=LEFT,fill=BOTH,expand=1, padx=30, pady=10)
        download_module_button = ttk.Button(self.middle_frame, text=MessageCatalog.translate("Download or update modules from the network"), bootstyle="Primary",command=run_windows_model_download)
        download_module_button.pack(side=LEFT,fill=BOTH,expand=1, padx=30, pady=10)
        self.note_frame=ttk.Frame(frame)
        self.note_frame.place(relx=0, rely=0.54, relheight=0.46, relwidth=1, bordermode="inside")
        notebook = ttk.Notebook(self.note_frame, bootstyle="info")
        notebook.pack( expand=1, fill=BOTH)
        self.note1 = ttk.Text(notebook, wrap="char",spacing1=20)
    
        self.note1.insert("1.0",MessageCatalog.translate("This software is completely free. Thank you for using it! Feel free to follow my account for updates:\nYouTube: https://www.youtube.com/@onepi-i8x TikTok: https://www.tiktok.com/@onepizen \nAdditionally, if you can spare a donation so I don't have to worry about next month's medication costs,\n I would be extremely grateful! For donations over $ 1, please send a message to my account,\nand I will include your name in the thank-you list in the next update o(>ω<)o\nOf course, if you can't donate, no worries! A like on my video would also be greatly appreciated (o˘◡˘o)\nIf you encounter any issues, feel free to give me feedback, and I will try my best to fix the bugs when I have time." ))

        picframe1=ttk.Frame(notebook)
        # WeChat 框架
        wechat_frame = ttk.Frame(picframe1)
        wechat_frame.pack(side=LEFT, padx=50)

        self.label_wechat_text = ttk.Label(wechat_frame, text=MessageCatalog.translate("WeChat"),cursor='hand2')
        self.label_wechat_text.pack(side=TOP)
        self.label_wechat_text.bind("<Button-1>", lambda event:( webbrowser.open(wechat)))
        label_wechat = ttk.Label(wechat_frame, image=wechat_image,cursor='hand2')
        label_wechat.pack(side=TOP)
        label_wechat.bind("<Button-1>", lambda event:( webbrowser.open(wechat)))

        # Alipay 框架
        alipay_frame = ttk.Frame(picframe1)
        alipay_frame.pack(side=LEFT, padx=50)
        
        self.label_alipay_text = ttk.Label(alipay_frame, text=MessageCatalog.translate("PayPal"),cursor='hand2')
        self.label_alipay_text.pack(side=TOP)
        self.label_alipay_text.bind("<Button-1>", lambda event:( webbrowser.open(alipay)))
        label_alipay = ttk.Label(alipay_frame, image=alipay_image,cursor='hand2')
        label_alipay.pack(side=TOP)
        label_alipay.bind("<Button-1>", lambda event:( webbrowser.open(alipay)))


        picframe2 = ttk.Frame(notebook) 
        # bilibili_youtube 框架
        bilibili_youtube_frame = ttk.Frame(picframe2)
        bilibili_youtube_frame.pack(side=LEFT, padx=50)
        self.label_bili_text = ttk.Label(bilibili_youtube_frame, text=MessageCatalog.translate("YouTube"),cursor='hand2')
        self.label_bili_text.pack(side=TOP)
        self.label_bili_text.bind("<Button-1>", lambda event:( webbrowser.open(bilibili_youtube)))
        label_bili = ttk.Label(bilibili_youtube_frame, image=bilibili_youtube_image,cursor='hand2')
        label_bili.pack(side=TOP)
        label_bili.bind("<Button-1>", lambda event:( webbrowser.open(bilibili_youtube)))

        # Douyin 框架
        douyin_frame = ttk.Frame(picframe2)
        douyin_frame.pack(side=LEFT, padx=50)
        self.label_douyin_text = ttk.Label(douyin_frame, text=MessageCatalog.translate("TikTok"),cursor='hand2')
        self.label_douyin_text.pack(side=TOP)
        self.label_douyin_text.bind("<Button-1>", lambda event:( webbrowser.open(douyin)))
        label_douyin = ttk.Label(douyin_frame, image=douyin_image,cursor='hand2')
        label_douyin.pack(side=TOP)
        label_douyin.bind("<Button-1>", lambda event:( webbrowser.open(douyin)))


        self.note2 = ttk.Text(notebook, wrap="char",spacing1=20)
        self.note2.insert("1.0",MessageCatalog.translate("Software Version: 1.00\n© 2024 OnePi. All rights reserved.\nAuthor: OnePi\nGitHub Address: https://github.com/OnePi-1pi/onepitranslator\nThis software need open-source modules including: ttkbootstrap, Argos-translate, deep-translate, but no modifications have been made to the original code."))


        notebook.add(self.note1, text=MessageCatalog.translate("One Pi's Muttering"), sticky=NSEW)  # 第一个标签页,包含文本和布局选项
        notebook.add(picframe1, text=MessageCatalog.translate("Donation Portal")) 
        notebook.add(picframe2, text=MessageCatalog.translate("Media Accounts"))  
        notebook.add(self.note2, text=MessageCatalog.translate("Software Information"))
        self.creat_api_options(initname,ininame)
        root.update_idletasks()
        return frame


#***************************************小部件*********************************************************

    #---------------------------创建滑块-------------------------------------
    def create_scale(self,master, scale_title,set_time):
        scale_title = MessageCatalog.translate(scale_title)
        self.master = master
        #print(set_time)
        # 初始值
        # 设置一个变量,以参数text为名字,并赋值为初始值
        master.setvar(scale_title, f"{float(set_time):#.3g}s")

        # 创建一个新的框架容器,用来包含频带的所有控件
        container = ttk.Frame(master, borderwidth=0)

        # 创建一个标签,用于显示,锚定中心
        hdr = ttk.Label(container, text=scale_title, anchor=W,bootstyle=INFO        )
        hdr.place(relx=0, rely=0.02,relwidth=0.7,relheight=0.4)

        # 根选择不同的样式
        bootstyle = SUCCESS if isinstance(scale_title,str) else INFO

        # 创建一个滑动条
        scale = ttk.Scale(
            master=container,  # 滑动条的父容器
            orient=HORIZONTAL,  # 滑动条的方向
            from_=0,  # 滑动条的最小值
            to=60,  # 滑动条的最大值
            value=set_time,  # 滑动条的初始值
            variable= self.scale_time,
            command=lambda x=set_time, y=scale_title: master.setvar(y, f"{float(x):#.3g}s"),  # 滑动条移动时更新值
            bootstyle=bootstyle,  # 使用选择的样式
        )
        self.scale=scale
        scale.place(relx=0, rely=0.5,relwidth=1,relheight=0.4)
        # 创建并放置显示滑动条当前值的标签
        Scale_label = ttk.Label(master=container, textvariable = scale_title,bootstyle=INFO  ,anchor=W)
        Scale_label.place(relx=0.7, rely=0.02,relwidth=0.3,relheight=0.4)
        return container  
    #---------------------------创建api展示存储界面-------------------------------------
    def creat_api_options(self, t,n):
            # 销毁之前的设置frame
        self.translator_select.configure(text=t)
        if hasattr(self, "api_entry_frame"):
            self.api_entry_frame.destroy()

        self.api_entry_frame = ttk.LabelFrame(self.translator_options_frame,text=MessageCatalog.translate("Enter apikey here, leave blank if not needed"), labelanchor="n", borderwidth=0, bootstyle="danger")
        self.api_entry_frame.place(relx=0.17, rely=0.08, relheight=0.9, relwidth=0.71, bordermode="inside")

        # 创建控件
        for key, value in api_dict[n].items():
            # #print (key, value)
            if key.startswith("label"):
                # 创建标签
                label = ttk.Label(self.api_entry_frame, text=MessageCatalog.translate(value),bootstyle="info")
                label.pack(expand=1, padx=10, pady=2)
            elif key.startswith("entry"):
                showchr=""
                # 创建输入框
                if key.endswith("3"):
                    showchr=""
                elif self.key.instate(["selected"]) :
                    showchr="*"
                entry = ttk.Entry(self.api_entry_frame,bootstyle="primary",show=showchr)
                entry.insert(0,value)
                entry.pack(fill=X,expand=1, padx=10, pady=5)
                if key.endswith("3"):
                    entry.bind("<Double-Button-1>", lambda event:( webbrowser.open(value)))
                entry.bind("<KeyRelease>", lambda event, n = n , k=key, e=entry :self.update_api_dict(n,k,e) )

        return 
        #定义更新显示名函数分别对应:全部清空,只更新第一列和第三列,更新第二列,更新第三列,
    #---------------------------更新文件名翻译展示框-------------------------------------
    def upviewtree(self,pathadd=None,colnum=None):
        global dict_path_colid_trand
        if colnum:
            for i, key in enumerate(pathadd):
                #条件表达式选择奇偶
                tag = "odd" if i & 1  else "even"
                #只重设tag
                if colnum == "retag":
                    rowid = dict_path_colid_trand[key][0]
                    self.tree.item(rowid, tags=[tag])
                elif colnum == "col1":
                    # 如果是新选中的选项,则只更新第一列,并把对应的第二三列值设为空,文件名+后缀名
                    t1,t2,t3 = key.stem,"",key.name
                    if key not in dict_path_colid_trand:
                        rowid = self.tree.insert("", END, values=(t1,t2,t3),tags=tag)
                        #新增为{path:[colid]}
                        dict_path_colid_trand[key]=[rowid]
                        #print(key.name,rowid)
                    else:
                        #key已经存在则一定是回退名称的调用,只需改变第三列
                        rowid = dict_path_colid_trand[key][0]
                        self.tree.set(rowid,"col3",t3)

                    
                else: 
                    #如果是翻译后的更新,则只修改colnum列对应的值为dict_path_colid_trand中的对应值
                    c,t=dict_path_colid_trand[key]
                    if colnum == "col3":
                        t += key.suffix
                    self.tree.set(c,colnum,t)

        else:
        #清空treeview
            global pathall,dict_source_renamed,s_name_add_flag
            #清空显示
            self.tree.delete(*self.tree.get_children())
            # 重设初始状态
            pathall = [] # 存储原文件名路径的列表  
            dict_path_colid_trand = {}#键为原文件名,值为翻译后文件名 
            dict_source_renamed = {}
            s_name_add_flag=True     #设置默认要加原文件名

        self.tree.update_idletasks()
        #更新列表项后调整显示大小
        self.adjust_row_height()
        return None
    #---------------------------创建展示框右键菜单-------------------------------------
    def show_menu(self, event):
        # 定位菜单到鼠标的位置
        self.context_menu.post(event.x_root, event.y_root)
        
        return 
    #---------------------------值变化时改变TreeView-------------------------------------
    def on_value_change(self,event=None):
        selected_item = self.tree.selection()
        if selected_item:
            # 获取单元格的y对应的行id
            row_id = selected_item[0] #self.tree.identify_row(event.y)
            col_id = "#2"
            #tree.bbox(selected_item[0], col_id)获取指定单元格的边界框(bounding box),并将其位置和尺寸信息存储在变量 x/y/width 和 height 中.
            x, y, width, height = self.tree.bbox(row_id, col_id)
            # 在 self.tree(即 Treeview 控件)中创建了一个 Entry 控件
            edit_entry = ttk.Entry(self.tree)
            #使用 place() 方法将 Entry 控件放置在指定的位置和大小.x 和 y 是单元格的左上角坐标,width 和 height 是单元格的宽度和高度
            edit_entry.place(x=x, y=y , width=width)
            #将单元格原来的值插入到 Entry 控件中.0 表示插入到文本框的起始位置.
            edit_entry.insert(0, self.tree.set(row_id, col_id))
            #将焦点设置到 Entry 控件上,使其成为当前活动控件.这样,用户可以立即开始编辑文本,无需额外点击.
            edit_entry.focus()
            edit_entry.bind("<Escape>", lambda e: self.save_edit(edit_entry,row_id, col_id))
            edit_entry.bind("<Return>", lambda e: self.save_edit(edit_entry,row_id, col_id))
            #将 save_edit 函数绑定到 Entry 控件的 <FocusOut> 事件上.当 Entry 控件失去焦点(例如用户点击了窗口的其他部分)时,save_edit 函数就会被调用.
            edit_entry.bind("<FocusOut>", lambda e: self.save_edit(edit_entry,row_id, col_id))
        return 


#***************************************主体界面结束,功能区开始*********************************************************
    def update_treeview_styles(self):
        # 获取当前主题的颜色
        primary_color = root.style.colors.primary
        success_color = root.style.colors.success
        light_color = '#ffffff'
        # 重新配置标签样式
        self.tree.tag_configure("even")
        self.tree.tag_configure("odd", background=primary_color,foreground=light_color)
        self.treeview_left.tag_configure("odd", background=primary_color, foreground=light_color)
        self.treeview_right.tag_configure("odd", background=success_color, foreground=light_color)
        self.upviewtree(pathadd = pathall ,colnum = "retag")
    #---------------------------界面防抖-------------------------------------
    def debounce(self, func, wait):
        def debounced_func(*args, **kwargs):
            if hasattr(self, "_debounce_timer"):
                self._debounce_timer.cancel()
            self._debounce_timer = threading.Timer(wait / 1000, func, args, kwargs)
            self._debounce_timer.start()
        return debounced_func
    #---------------------------treeview全选功能-------------------------------------
    def tree_select_all(self,event=None):
        # 取消选择所有已有的选中项
        self.tree.selection_remove(self.tree.get_children())
        # 选中所有项
        for item in self.tree.get_children():
            self.tree.selection_add(item)
            # 递归选中子项
            self.tree.selection_add(self.tree.get_children(item))
        return 
    #---------------------------更新语言选项功能-------------------------------------
    def update_language_menus(self,event=None):
        config_dict["engine"] = self.selected_translator.get()
        self.langsfrom_to = engineslang[self.selected_translator.get()]
        # 遍历,为下拉菜单添加每个选项,使用 lambda 函数关联每个选项的命令
        self.source_lang_menu.delete(0,END)    
        for name in self.langsfrom_to:
            tfna = MessageCatalog.translate(name)
            self.source_lang_menu.add_radiobutton(label=tfna,value=name,variable=self.selected_fromlang, command=lambda n=tfna: self.source_lang_select.configure(text=MessageCatalog.translate(n)))
        self.target_lang_menu.delete(0,END)
        if self.selected_fromlang.get() not in self.langsfrom_to:
            self.selected_fromlang.set(self.langsfrom_to.get("auto","english"))
            self.source_lang_select.configure(text=MessageCatalog.translate(self.selected_fromlang.get()))

        for name in self.langsfrom_to:
            if name != "auto":
                ttna = MessageCatalog.translate(name)
                self.target_lang_menu.add_radiobutton(label=ttna,value=name,variable=self.selected_tolang, command=lambda n=ttna: self.target_lang_select.configure(text=MessageCatalog.translate(n)))
        if self.selected_tolang.get() not in self.langsfrom_to:
            localyes = self.langsfrom_to.get(self.local_lang,False)
            if localyes:
                settolang = self.local_lang
            else:
                settolang = "english"

            self.selected_tolang.set(settolang)
            self.target_lang_select.configure(text=MessageCatalog.translate(settolang))
        return 
    #---------------------------删除选择行功能-------------------------------------
    def delete_selected_rows(self,event=None):
        global pathall,dict_path_colid_trand,dict_source_renamed
        selected_items = self.tree.selection()
        
        for item in reversed(selected_items):
            for key, value in dict_path_colid_trand.items():
                if value[0] == item: 
                    # 删除字典中的条目
                    del dict_path_colid_trand[key]
                    if key in dict_source_renamed: del dict_source_renamed[key]
                    pathall.remove(key)
                    break  # 找到匹配项后退出循环
            self.tree.delete(item)
        self.upviewtree(pathadd = pathall ,colnum = "retag")
        self.adjust_row_height()
        return "break"
     #---------------------------删除选择行功能-------------------------------------
    #---------------------------删除选择项 功能-------------------------------------
    def delete_tree_selected(self,treename,treeitem,event=None):
        # print(treeitem)
        selected_items = treename.selection()
        for item in reversed(selected_items):
            item_text = treename.set(item,'1') 
            if item_text:
                for path in treeitem:

                    if item_text == path.name:
                        treename.delete(item)
                        treeitem.remove(path)
            self.up_files()
        return "break"

    #---------------------------自动调整行高-------------------------------------
    def adjust_row_height(self,event=None):
        if self.tree.get_children():
            total_height = self.tree.winfo_height()
            row_height = total_height // 20
            self.style.configure("info.Treeview", rowheight=row_height)
            self.tree.update_idletasks()
        return "break"
    #---------------------------隐藏apikey功能-------------------------------------
    def hidden_key(self,event=None):
        self.translator_menu.invoke(self.selected_key.get())
        return 
    #---------------------------接收用户的treeview输入-------------------------------------
    def save_edit(self,edit_entry, row_id, col_id):
        global dict_path_colid_trand
        #从 Entry 控件中获取用户输入的新值.
        new_value = edit_entry.get()
        #销毁 Entry 控件
        self.tree.set(row_id,col_id,new_value)
        edit_entry.destroy()
        # #print(row_id,new_value)
        #将新值更新到 dst 字典中对应的键
        # #print(dict_path_colid_trand)
        if new_value :
            for key,vlist in  dict_path_colid_trand.copy().items():
                # #print(key,vlist)
                if  vlist[0] == row_id: 
                    dict_path_colid_trand[key] =[row_id, new_value]
                    # #print("key,new_value",key,new_value)
                    #print("key,new_value",key,new_value)
                    break
                
        return 


#***************************************纯后台区*********************************************************
    #---------------------------接收用户选择文件-------------------------------------
    def up_fnames(self , n = 0): 
        sal = None
        if n :
            sal = filedialog.askopenfilenames()
            if sal:
                sal = map(Path , sal)
        else:   
            sal =filedialog.askdirectory()
            if sal :
                sal = Path(sal).iterdir()
        if sal:
            global pathall
            pathadd =   list(set(sal) - set(pathall))
            pathall +=  pathadd
            
            self.upviewtree(colnum="col1",pathadd=pathadd)
            self.upviewtree(pathadd = pathall ,colnum = "retag")
        return 

    def up_files(self , n = 0): 
        #print(n)
        sfl = []
        global nfts
        if n == 1 :
            sfl = filedialog.askopenfilenames()
            if sfl:
                sfl = map(Path , sfl)
        elif n == 2:   
            sfl =filedialog.askdirectory()
            if sfl :
                sfl = Path(sfl).iterdir()
        elif n == 3 :  
            self.treeview_left.delete(*self.treeview_left.get_children())
            self.treeview_right.delete(*self.treeview_right.get_children())
            nfts=[]
            return None
        if sfl:
            sfl =  list(set(sfl))
            for i, key in enumerate(sfl):

                if key not in nfts and key.is_file() :
                    self.treeview_left.insert("", END, values=(key.name,))
                    nfts.append(key) 
        for i,v in enumerate(self.treeview_left.get_children()):
            #条件表达式选择奇偶
            tag = "odd" if (i) & 1  else "even"
            self.treeview_left.item(v, tags=[tag])

        return 

    #---------------------------列表翻译方法-------------------------------------
    def translate_list(self):
        global dict_path_colid_trand
        # 
        stemmed_words = list(map(lambda x: x.stem ,dict_path_colid_trand))
        txt_length = sum(map(len , stemmed_words ))
        
        # 
        # 翻译translate,接受文本并返回翻译后的文本
        if txt_length:
            wtime=wait_time(txt_length)
            # print(stemmed_words)
            translated_text = self.translate_all(wtime,stemmed_words)
            if translated_text:
                # print(repr(translated_text))
                translated_text = translated_text.strip()
                translated_list = translated_text.splitlines()
                slen = len(dict_path_colid_trand)
                #如果返回的和传入的行数不一致，则尝试再使用其他分隔符分割：
                #大于时
                if len(translated_list) > slen:
                    #尝试替换空行
                    lines = translated_text.splitlines()
                    cleaned_lines = [line for line in lines if line.strip()]
                    if len(cleaned_lines) > slen:
                        Messagebox.show_question(message=repr(translated_text),title= 'turn number more wrong')
                        return False
                    elif len(cleaned_lines) <= slen:
                        translated_list='\n'.join(cleaned_lines)
                #小于时
                if len(translated_list) < slen:
                    #先尝试替换常见符号
                    for split_str in [';' ,'.' , '。',' ' ,',' ,'，',"'" ,'"' ,'_','-','']:

                        translated_temp = re.sub(split_str, "\n",translated_text)
                        translated_list = translated_temp.splitlines()
                        if len(translated_list)  == slen:
                            #print(f'{split_str=}')
                            break
                    #替换结束后如果长度小于原始，则替换全部符号
                    if split_str == '':
                        translated_temp = re.sub(r"[^\p{L}\p{N}\p{M}\n]", "\n",translated_text)
                        translated_list = translated_temp.splitlines()
                    #替换结束后如果长度大于原始，则直接报错
                if len(translated_list) != slen:
                    Messagebox.show_question(message=repr(translated_text),title= 'turn number less wrong')
                    return False
                for i,key in enumerate(dict_path_colid_trand):
                    dict_path_colid_trand[key] = [dict_path_colid_trand[key][0],translated_list[i]]
                # 
                self.upviewtree(colnum="col2",pathadd=pathall)
        return None
    #---------------------------文档翻译方法-------------------------------------
    def translate_files(self):
        global nfts
        targs = {"slg":self.selected_fromlang.get(),"tlg":self.selected_tolang.get(),"key":None,"sleep_time":self.scale_time.get(),"singaltrans":self.singaltrans.instate(["selected"])}
        engine = self.selected_translator.get()
        apikd = api_dict.get(engine,{})
        if engine in no_file_trans:
            Messagebox.show_question(
                message=MessageCatalog.translate("This translation engine cannot translate documents"),
                title="engine error")
            return False            
        elif apikd.get("entry1") or apikd.get("entry2"):
            targs["key"] = [apikd.get("entry1"),apikd.get("entry2")]
        elif engine in api_dict :
            Messagebox.show_question(
                message=MessageCatalog.translate("Missing API settings, please check if the API or URL in the <Options and Settings> area is set correctly"),
                title="api_key need")
            return False
        for file in nfts:
            targs["slist_or_str"] = file
            errorf=Path("error.er")

            
            try  :
                ff = 0
                newpath,child_pid = translation_engines[engine](**targs)
                #print(newpath,child_pid)
                
                for i in range(300):
                    self.p.configure(value=i)
                    self.root.update()# 更新GUI
                    if errorf.exists() and errorf.is_file():
                        #print("找到错误文件")
                        self.treeview_right.insert("", END, values=(MessageCatalog.translate("Translation failed")))
                        with open(Path(__file__).parent /"error.er",encoding="utf_8") as f:
                            e = f.read()
                        errorf.unlink()
                        raise ValueError(e)
                    if newpath.exists():
                        ff = 1
                        self.p.configure(value=300)
                        break  # 如果newpath存在，立即退出循环
                    
                    self.root.after(1000)  # 等待1秒
                

                if ff :
                    #print(file,"翻译成功")
                    self.treeview_right.insert("", END, values=(newpath.name,))
                    
                else:
                    os.kill(child_pid, signal.SIGTERM)
                    #print(file,"翻译失败")
                    self.treeview_right.insert("", END, values=(MessageCatalog.translate("Translation failed")))
                    
            except Exception as e :
                #print("错1",e)
                mt = type(e).__name__
                mm = str(e)
                if mm:
                    pass
                else:
                    mm = mt
                # Messagebox.show_question(message=mm,title= mt)
            for i,v in enumerate(self.treeview_right.get_children()):
                #条件表达式选择奇偶
                tag = "odd" if (i) & 1  else "even"
                self.treeview_right.item(v, tags=[tag])

        return None
    #---------------------------文本翻译方法-------------------------------------
    def translate_text(self):
        # 读取左边文本框中的内容
        slistortext = self.text_left.get(1.0,END)
        txt_length = len(slistortext)
        # 翻译translate,接受文本并返回翻译后的文本
        if txt_length :
            wtime=wait_time(txt_length)
            translated_text = self.translate_all(wtime,slistortext)
            if translated_text:
                # 清空右边文本框,并插入翻译后的内容
                self.text_right.delete(1.0,END)
                self.text_right.insert(1.0, translated_text)
        return None
    #---------------------------翻译总体方法-------------------------------------
    def translate_all(self,wtime,slistortext):
        event = Event()
        event.clear()
        targs = {}
        targs = {"slist_or_str":slistortext,"slg":self.selected_fromlang.get(),"tlg":self.selected_tolang.get(),"key":None,"sleep_time":self.scale_time.get(),"singaltrans":self.singaltrans.instate(["selected"])}
        engine = self.selected_translator.get()
        apikd = api_dict.get(engine,{})
        if apikd.get("entry1") or apikd.get("entry2"):
            targs["key"] = [apikd.get("entry1"),apikd.get("entry2")]
        elif engine in api_dict :
            Messagebox.show_question(
                message=MessageCatalog.translate("Missing API settings, please check if the API or URL in the <Options and Settings> area is set correctly"),
                title="api_key need")
            return False
        if wtime >= 100 or wtime >= 10 and engine == 'OfflineTranslantor' :
            Process(target=creat_meter, args=(wtime,targs["sleep_time"],MessageCatalog.translate("Translating"),event),daemon=True).start()
        
        try  :
            # 翻译文本并返回翻译后的文本
            # 
            translated = translation_engines[engine](**targs)
        except AttributeError as a:
            event.set()
            Messagebox.show_question(message=MessageCatalog.translate("No corresponding translation found"),title= str(a))

        except requests.exceptions.RequestException as e:
            event.set()
            Messagebox.show_question(message=f'{MessageCatalog.translate("network error")} {type(e)}',title= str(e))
                                                        
        except BaseException as e:
            event.set()
            mt = type(e).__name__
            mm = str(e)
            if mm:
                pass
            else:
                mm = mt
            if mt == "ElementNotFoundInGetRequest":
                mm = MessageCatalog.translate("No translation found.")
            Messagebox.show_question(message=mm,title= mt)

        except:
            event.set()
            
            Messagebox.show_question(message=MessageCatalog.translate("Unknown Error"),title= MessageCatalog.translate("Error"))
        else:
            return translated
        finally:
            event.set()
        return None
    #---------------------------增加删除原文件名-------------------------------------
    def add_or_sub(self,event=None):
        
        global dict_path_colid_trand
        global s_name_add_flag
        addpath = []
        for key , vlist in dict_path_colid_trand.items():
            #判断是不是还没有翻译后的值
            if  len(vlist) >= 2:
                s = f"_{key.stem}"
                if s_name_add_flag and s not in vlist[1]:
                    vlist[1] += s
                    addpath.append(key)
                else:
                    try:
                        vlist[1] = vlist[1].replace(s, "")
                        addpath.append(key)
                    except:
                        continue
        if addpath:
            self.upviewtree(pathadd = addpath ,colnum = "col2")
            s_name_add_flag ^= 1
        return "break"
    #---------------------------重命名-------------------------------------
    def rename_fnames(self,event=None):
        global dict_path_colid_trand ,dict_source_renamed
        errors = 0
        for key , value in dict_path_colid_trand.items():
            #测试是不是有翻译后的值，或两者相同
            if len(value) >= 2 :
                #如果原始路径在已命名文件字典里 
                if key in dict_source_renamed:
                    #现在文件名是已重命名过的名称
                    nowname = dict_source_renamed[key]
                else:
                    #现在文件名没变，还是原来的
                    nowname = key
                #如果现在文件名和要重命名的相同，进入下一次循环
                if nowname == value[1]:
                    continue
                #否则新名称为更换名字为要重命名的名称的现在文件名
                newpath = nowname.with_stem(value[1])
                try:
                    #重命名现在的文件名
                    dict_source_renamed[key] = nowname.rename(newpath)
                    #命名后如果现在的文件名还存在则重命名失败，引发异常，将重命名的文件名回退回现在的
                #重命名过程报错
                except :
                    errors += 1
                if nowname.exists():
                    dict_source_renamed[key] = nowname
                #如果新老文件名都不存在，虽然不知道发生了什么，还是直接退回初始文件名
                elif not newpath.exists():
                    dict_source_renamed[key] = key
                
        if errors :
            Messagebox.show_question(message=f'{MessageCatalog.translate("The number of renamed error files")}:{errors}',title=MessageCatalog.translate("Error Warning"))
        self.upviewtree(pathadd = dict_source_renamed ,colnum = "col3")
        self.adjust_row_height()
        return None
    #---------------------------回退为原文件名-------------------------------------
    def back_to_source_name(self,event=None):
        global dict_path_colid_trand ,dict_source_renamed
        error = 0
        for source , newname in dict_source_renamed.copy().items():
            try :
                dict_source_renamed.pop(newname.rename(source))
                if newname.exists():
                    dict_source_renamed[source] = newname
                    raise NameError
            except:
                error = 1
        if error:
            Messagebox.show_question(message = MessageCatalog.translate("Failed to revert the file name, the failed file:\nOriginal name: Should be the current name")+'\n'+ f'{dict_source_renamed}',title=MessageCatalog.translate("Error Warning"))
        self.upviewtree(pathadd = pathall ,colnum = "col1")
        self.adjust_row_height()
        return None
    #---------------------------存储api密钥-------------------------------------
    def update_api_dict(self,n, k, entry_widget):
    # 更新 api_dict
        api_dict[n][k] = entry_widget.get()
        return 

#***********************************************函数**************************************************************
#---------------------------读取json文件-------------------------------------
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
        return False
#---------------------------循环存储-------------------------------------
def periodic_save(self):
    config_dict.update({"windowsplacesize": self.root.geometry(),"user_theme":self.style.theme_use(),"font_size":self.font_size_spinbox.get(),"font_weight":self.font_weight.get() ,"source_lang":self.selected_fromlang.get(),"target_lang":self.selected_tolang.get(),"singal_t":self.singaltrans.instate(["selected"]),"time":str(self.scale_time.get()),"hidden_key":self.set_checkw.get(),"selected_key":self.selected_key.get()})

    with open(Path(__file__).parent /"config.json", "w",encoding="utf_8") as config_file:
        json.dump(config_dict, config_file, indent=4)
    self.root.after(30000, lambda: periodic_save(self))

def save_api_keys_to_file():
    # 将 api_dict 保存到本地文件
    jsp = Path(__file__).parent /"api_key.json"
    with open(jsp, "w",encoding="utf_8") as f:
        json.dump(api_dict, f, ensure_ascii=False, indent=4)
    if jsp.exists():
         Messagebox.show_question(message=f'{MessageCatalog.translate("file path:")}{jsp}',title= MessageCatalog.translate('Successfully saved'))
    else:
        Messagebox.show_question(message='can not find the json file',title= MessageCatalog.translate('Save failed'))
    return

#语言选择退出
def switch_language(lang_code):
    confirm=MessageCatalog.translate("confirm")
    cancel=MessageCatalog.translate("cancel")
    # 弹出确认对话框
    result = Messagebox.show_question(
        message=(MessageCatalog.translate("Are you sure you want to switch language? The application will close.")),
        title="Confirm Exit",
        buttons=[cancel+":secondary", confirm+":primary"]
    )
        # 设置新的语言环境
    config_dict["option_lang"] = lang_code
    with open(Path(__file__).parent / "config.json", "w",encoding="utf_8") as config_file:
        json.dump(config_dict, config_file, indent=4)
    MessageCatalog.locale(lang_code)
    
    if result == confirm:
        # 退出应用程序
        sys.exit()
        
    return

def creat_meter(duration,sleeptime,txt,event):
    rootm = ttk.Window()
    rootm.place_window_center()
    tall = int((duration+sleeptime)*5)
    meter = ttk.Meter(master=rootm,
                metersize=300,            # 设置 meter 的大小
                padding=20,               # 设置内边距
                amounttotal=200,          # 设置进度条的最大值为100
                amountused=0,             # 设置初始进度为0
                metertype="full",         # 设置 meter 类型为完整的圆形
                interactive=False,        # 禁用用户交互
                showtext=False,
                textfont="-size 20 -weight bold",  # 设置进度条中间文本的字体
                stripethickness=2,        # 设置条纹厚度为
                subtext=txt+'...',   # 设置子文本
                bootstyle="success"          # 设置进度条的样式
            )
    meter.pack()
    rootm.update()
    mmn=0
    def update_meter(count):
        if event.is_set() or count == 200:#
            rootm.destroy()
            return 1
        count += 1
        meter.configure(amountused=count)
        meter.update()
        rootm.after(tall,update_meter,count)
    mmn = update_meter(0)
    if mmn:
        return
    else:
        rootm.mainloop()

def wait_time(x):
    if x <= 30:
        return x
    elif x <= 300:
        scaled_a = (x - 30) / 270
        b = x * (1 - 0.9 * math.log10(1 + scaled_a * 9))
        return b
    else:
        return x / 10

def generate_qr_code(data, size=200):
    # 生成 QR 码
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.LANCZOS)

    return ImageTk.PhotoImage(img)

def run_windows_model_download():
        # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
        # 使用管理员权限运行批处理文件
    batch_file_path = os.path.join(current_dir, "run_this_to_upgrade_modules.bat")
    
    try:
        # 执行批处理文件
        result = subprocess.run([batch_file_path], capture_output=True, text=True, check=True)
        print(MessageCatalog.translate("success"))
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)


def main():

    global config_dict,json_f_dict,api_dict,font_now
    font_now=None
    api_dict={'LibreTranslator': {'label1': 'The mirror website used for translation', 'entry1': 'https://translate.terraprint.co', 'label2': 'apikey', 'entry2': '', 'label3': 'Double click the URL below to see more mirror addresses, do not enter the API key for mirror\n addresses that do not require an API key, location: varies', 'entry3': 'https://github.com/LibreTranslate/LibreTranslate#mirrors'},
 'BaiduTranslator': {'label1': 'User ID (App ID)', 'entry1': '', 'label2': 'Translation key (App Key)', 'entry2': '', 'label3': 'Get a free appid and appkey, it is very simple \nif you have passed the real-name authentication, requires a phone number. Location: China', 'entry3': 'http://api.fanyi.baidu.com/product/113'},
 'YandexTranslator': {'label1': 'apikey', 'entry1': '', 'label3': 'Paid API application website, no free API, the application process is quite cumbersome. Location: Russia', 'entry3': 'https://yandex.cloud/en-ru/docs/translate/api-ref/authentication'},
 'MicrosoftTranslator': {'label1': 'apikey', 'entry1': '', 'label2': "Location/Region, note: it's not Endpoints", 'entry2': '', 'label3': 'Free API acquisition address (Log in to Azure - Create resource - Translator service - Deploy - View key),\n account registration requires a mobile phone and VISA card (with fee verification), location: distributed', 'entry3': 'https://portal.azure.com/?quickstart=true#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/TextTranslation'},
 'DeeplTranslator': {'label1': 'apikey', 'entry1': '', 'label3': 'Free API acquisition website, requires a VISA card from Europe/America or other regions. Location: Germany', 'entry3': 'https://www.deepl.com/en/docs-api/'},
 'PapagoTranslator': {'label1': 'Client ID', 'entry1': '', 'label2': 'Secret Key', 'entry2': '', 'label3': 'API application address is as follows, no free API, requires a phone number. Location: South Korea', 'entry3': 'https://www.ncloud.com/join/info'},
 'ChatGptTranslator': {'label1': 'apikey', 'entry1': '', 'label3': 'API acquisition website is as follows, note:\n the free version (chatgpt3.5) API does not have translation functionality.', 'entry3': 'https://platform.openai.com/settings/profile?tab=api-keys'},
 'detection': {'label1': 'apikey', 'entry1': '', 'label3': 'Only for testing language types, free API acquisition website is as follows, \napplication is very simple. Location: distributed', 'entry3': 'https://detectlanguage.com/'}}
    config_dict={}
    json_f_dict = {'api_key.json':api_dict,'config.json':config_dict}
    for filename , dictname in json_f_dict.items():
        conval = read_json_file(filename)
        if conval : dictname.update(conval)
    global lang_options
    lang_options = {
    "简体中文": "zh_cn",
    "English": "en",
    "العربية": "ar",
    "Français": "fr",
    "Español": "es",
    "Português": "pt",
    "Deutsch": "de",
    "한국어": "ko",
    "Italiano": "it",
    "日本語": "ja",
    "Русский": "ru",
    "Polski": "pl",
    "हिन्दी": "hi",
    "Türkçe": "tr",
    "ไทย": "th",
    "繁体中文": "zh_tw"}

    global translation_engines
    translation_engines={'OfflineTranslantor': choose_translate.OfflineTranslantor, 'GoogleTranslator': choose_translate.GoogleTranslator, 'LibreTranslator': choose_translate.LibreTranslator, 'MyMemoryTranslator': choose_translate.MyMemoryTranslator, 'BaiduTranslator': choose_translate.BaiduTranslator, 'PonsTranslator': choose_translate.PonsTranslator, 'LingueeTranslator': choose_translate.LingueeTranslator, 'YandexTranslator': choose_translate.YandexTranslator, 'MicrosoftTranslator': choose_translate.MicrosoftTranslator, 'DeeplTranslator': choose_translate.DeeplTranslator,  'PapagoTranslator': choose_translate.PapagoTranslator, 'ChatGptTranslator': choose_translate.ChatGptTranslator, 'detection': choose_translate.detection}
    global engineslang
    engineslang={'OfflineTranslantor' : choose_translate.argodict  ,'GoogleTranslator' : choose_translate.googledict ,'LibreTranslator' : choose_translate.libredict  ,'MyMemoryTranslator' : choose_translate.mymemorydict  ,'BaiduTranslator' : choose_translate.baidudict ,'PonsTranslator' : choose_translate.ponsdict   ,'LingueeTranslator' : choose_translate.lingueedict  ,'YandexTranslator' : choose_translate.googledict  ,'MicrosoftTranslator' : choose_translate.microsoftdict  ,'DeeplTranslator' : choose_translate.deepldict  ,'PapagoTranslator' : choose_translate.papagodict  ,'ChatGptTranslator' : choose_translate.googledict  ,'detection': {} }
    global local_dict
    local_dict= {'zh': 'chinese (simplified)','zh-cn': 'chinese (simplified)','zh_cn': 'chinese (simplified)', 'zh_hk': 'chinese (simplified)', 'zh_sg': 'chinese (simplified)','zh-tw': 'chinese (traditional)', 'zh_tw': 'chinese (traditional)', 'en': 'english','en_au': 'english', 'en_be': 'english', 'en_bw': 'english', 'en_ca': 'english', 'en_gb': 'english', 'en_hk': 'english', 'en_ie': 'english', 'en_in': 'english', 'en_nz': 'english', 'en_ph': 'english', 'en_sg': 'english', 'en_za': 'english', 'en_zw': 'english', 'ar': 'arabic','ar_in': 'arabic', 'ar_jo': 'arabic', 'ar_lb': 'arabic', 'ar_sy': 'arabic', 'fr': 'french','fr_be': 'french', 'fr_ca': 'french', 'fr_ch': 'french', 'es': 'spanish','es_ar': 'spanish', 'es_bo': 'spanish', 'es_cl': 'spanish', 'es_co': 'spanish', 'es_cr': 'spanish', 'es_do': 'spanish', 'es_ec': 'spanish', 'es_gt': 'spanish', 'es_hn': 'spanish', 'es_mx': 'spanish', 'es_ni': 'spanish', 'es_pa': 'spanish', 'es_pe': 'spanish', 'es_pr': 'spanish', 'es_py': 'spanish', 'es_sv': 'spanish', 'es_uy': 'spanish', 'es_ve': 'spanish', 'pt': 'portuguese','pt_br': 'portuguese', 'de': 'german','de_at': 'german', 'de_be': 'german', 'ko': 'korean','ko_kr': 'korean', 'it': 'italian','it_ch': 'italian', 'ja': 'japanese','ru': 'russian', 'ru_ua': 'russian', 'vi': 'vietnamese', 'pl': 'polish', 'hi': 'hindi','hi_in': 'hindi', 'tr': 'turkish', 'th': 'thai', 'sv': 'swedish', 'nl': 'dutch','nl_be': 'dutch', 'cs': 'czech', 'el': 'greek', 'he': 'hebrew', 'da': 'danish', 'fi': 'finnish', 'hu': 'hungarian', 'ro': 'romanian', 'sk': 'slovak', 'sr': 'serbian', 'bg': 'bulgarian', 'hr': 'croatian', 'lt': 'lithuanian', 'lv': 'latvian', 'et': 'estonian', 'sl': 'slovenian', 'mt': 'maltese', 'ca': 'catalan', 'gl': 'galician', 'eu': 'basque', 'sq': 'albanian', 'ml': 'malayalam','ta': 'tamil', 'ta_in': 'tamil', 'te': 'telugu','te': 'telugu','te_in': 'telugu', 'kn': 'kannada','mr': 'marathi',  'mr_in': 'marathi', 'si': 'sinhala', 'km': 'khmer', 'my': 'myanmar', 'lo': 'lao', 'ne': 'nepali', 'am': 'amharic', 'jw': 'javanese', 'su': 'sundanese', 'cy': 'welsh', 'sw': 'swahili', 'xh': 'xhosa', 'zu': 'zulu', 'yo': 'yoruba', 'ig': 'igbo', 'ha': 'hausa', 'ps': 'pashto', 'ks': 'kashmiri', 'pa': 'punjabi', 'gu': 'gujarati', 'or': 'odia (oriya)', 'tk': 'turkmen', 'ug': 'uyghur', 'uz': 'uzbek', 'tt': 'tatar', 'tg': 'tajik', 'yue': 'cantonese', 'af': 'afrikaans', 'ga': 'irish', 'kl': 'kalaallisut', 'kw': 'cornish', 'gv': 'manx', 'yi': 'yiddish'}
    global no_file_trans
    no_file_trans=['OfflineTranslantor','PonsTranslator', 'LingueeTranslator', 'detection']
    global pathall
    pathall= [] # 存储原文件名路径的列表  
    global dict_path_colid_trand
    dict_path_colid_trand= {}#键为原文件名,值为翻译后文件名 
    global dict_source_renamed
    dict_source_renamed= {}#键为原文件名,值为重命名后文件名
    global s_name_add_flag
    s_name_add_flag=True     #设置默认要加原文件名
    global nfts
    nfts= []#存储已选择的文件名




###############################################################
    global root
    root = ttk.Window()
    MessageCatalog.load(Path(__file__).parent/ 'languages')
    l = config_dict.get('option_lang',MessageCatalog.locale())
    lc = lang_options.values()
    if l in lc :
        MessageCatalog.locale(l)
    elif l[:2] in lc :
        MessageCatalog.locale(l[:2])
    global  wechat  
    wechat =  "https://payapp.weixin.qq.com/qr/AQE1c5clFl0Tf6geackLIkuy?t=vwEG#wechat_pay"
    global  wechat_image  
    wechat_image =  generate_qr_code(wechat,300)

    
    global  alipay  
    alipay =  MessageCatalog.translate("https://www.paypal.me/onepizen")
    global  alipay_image  
    alipay_image =  generate_qr_code(alipay,300)


    global  bilibili_youtube  
    bilibili_youtube =  MessageCatalog.translate("https://youtube.com/@onepi-i8x?si=QrX5QF_QR-iaBArL")
    global  bilibili_youtube_image  
    bilibili_youtube_image =  generate_qr_code(bilibili_youtube, 300)

    global  douyin  
    douyin =  MessageCatalog.translate("https://www.tiktok.com/@onepizen")
    global  douyin_image  
    douyin_image =  generate_qr_code(douyin, 300)



    app = TranslationApp(root)
    if config_dict.get('windowsplacesize',False):
        root.geometry(config_dict['windowsplacesize'])  
    else:
        root.geometry("1080x1024")
        root.place_window_center()
    root.update_idletasks()
    app.root.after(1000,periodic_save,app)
    try:
        threading.Thread(target=choose_translate.loadModel).start()
    except:
        print('no argos')
    root.mainloop()
    
if __name__ == '__main__':
    main()
