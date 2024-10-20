# 一派多功能翻译器
一个简单的GUI工具，用于翻译文本或文档并重命名文件或文件夹名称。使用在线（deeptranslator）和离线（argos翻译）翻译。
---


[English](README.md) | 中文

离线翻译 Argos Translate 与在线翻译 DeepTranslator 的整合版 GUI 程序，可用来翻译文本、文档或批量翻译并重命名文件或文件夹。修复了 DeepTranslator 的一些小 bug，并对 Argos Translate 进行了优化。

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

<img src="./src/onepitranslator/resources/images/all.gif" alt="img1" width="400">

# 目录

- [功能及特点](#✨-功能及特点)
- [安装](#🚀-安装)
- [使用说明](📖-说明)
- [视频及文档链接](#🔗-链接)

###  视频 ⬆️ 的说明更详细
## ✨ 功能及特点

- 🌐 **支持多种语言**  
  支持的语言选项包括：简体中文、English、العربية、Français、Español、Português、Deutsch、한국어、Italiano、日本語、Русский、Polski、हिन्दी、Türkçe、ไทย、繁体中文。
  


- ⚙️ **多翻译引擎整合**  
  结合在线翻译（通过 DeepTranslator）和离线翻译（通过 Argos Translate），且能存储api-key，根据需要一键切换。


  
  <img src="./src/onepitranslator/resources/images/enshow4.png" alt="img5" width="300">

- 📁 **批量翻译与重命名**  
  支持批量翻译文件名或文件夹名，翻译后可手动更改，也可添加原文件名，然后重命名，重命名后支持撤销操作。



- 🔄 **多核心优化**  
  也可支持文本翻译与文档批量翻译，argos在文本量少时仅使用单核，在文本量大时自动使用全部CPU核心。


## 🚀 安装

***注意：在 Windows 上运行 Argos Translate 需要 [Microsoft Visual C++ Redistributable](https://visualstudio.microsoft.com/zh-hans/downloads/#microsoft-visual-c-redistributable-for-visual-studio-2022) 和 LLVM/OpenMP（C++ 官方发行版不包含此库，你可以尝试使用开发版，或直接下载  [libomp140.x86_64.dll](G:\GitHub\OnePiTranslator\resources\libomp140.x86_64.dll) 并将其移动到 `C:\Windows\System32`. 3 和 4 号包 将会自动安装 ,仅需按提示点下一步即可，所以无需手动下载，感谢这位up解决了这个问题 [链接](https://www.bilibili.com/read/cv36895969)***
---

### 1️⃣ 安装包（推荐 Windows 系统）



- 1.💻 **在线安装包 _大小:~25M_** [链接](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/online_install_windows_cn.exe)  
  下载后安装即用，完全不用任何代码操作。网络好的可以下载。安装后还需要下载模块，针对中国网络优化，自动设置 pypi 源为清华源。
---
- 2.📦 **无 Argos安装包  _大小:~35M_（作者推荐）** [链接](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/no_argos_install_windows_cn.exe) 

  推荐给不想改变源或不想再下载模块且仅需要在线翻译的用户，仅需下载此包即可使用在线翻译。后续如需离线翻译，可通过工作目录下的 `install_argos_translate.bat` 进行安装。
---
- 3.💽 **完整在线离线翻译安装包 _大小: ~250M_** [链接](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/local_install_windows_cn.exe)    
  包含除 argos语言包 和 CUDA 加速组件外的所有必需组件。体积较大，安装后可使用在线翻译, 离线翻译还需要单独下载语言包[链接](https://github.com/argosopentech/argos-translate?tab=readme-ov-file#packages)，或直接下载打包好的完整包⬇️⬇️⬇️⬇️
---

- 4.🖥️ **附带语言包的完整安装包 _大小: ~2G__** [链接](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/all_add_language_package_windows_cn.exe) 

  包含全部组件(除了CUDA)。体积很大 >3G。自带语言包{中文（简体）：zh，中文（繁体）：zt，英文：en，法文：fr，西班牙文：es，德文：de，韩文：ko，日文：ja，俄文：ru}
  
---
123云盘（不限速）
https://www.123pan.com/s/bS7ETd-1zZ3A.html 提取码:3141

![alt text](./src/onepitranslator/resources/images/123.png)

---
百度云链接：https://pan.baidu.com/s/1zcyFJZjk8_tyNo0SJdUNBg?pwd=3145 
提取码：3145

小程序扫码

![alt text](./src/onepitranslator/resources/images/百度云小程序.png)

### 2️⃣ Pypi 安装（推荐已安装 Python 的用户,windows用户要管理员运行pip才能安装到默认目录）
#### 在线翻译的安装：
```bash
python -m pip install onepitranslator
```

### 然后运行:

```bash
python -m  onepitranslator
```
或者只是一句
```bash
onepitranslator
```

### 注意运行后会在桌面创建快捷方式,不想要的删除即可,不会再次创建.

#### 如需使用离线翻译，可继续安装argostranslate：

```bash
python -m pip install argostranslate spacy
```

此外，离线翻译还需下载spacy 的 `xx_sent_ud_sm` 模块：

```bash
python -m spacy download xx_sent_ud_sm
```
或者手动下载：➡️
[下载链接](https://spacy.io/models/xx#xx_sent_ud_sm)

现在版本的argostranslate可能由于numpy升级的原因无法使用，可以回退版本：

```bash
python -m pip install "numpy>=1.0.0,<2.0.0"
```

下载语言包[链接](https://github.com/argosopentech/argos-translate?tab=readme-ov-file#packages)

打开软件，选择<选项与设置>里的 _安装本地翻译语言库_ 按钮进行安装

## 📖 说明

###  ⏳  关于argos和CUDA
虽然已对argos进行了优化，文本量大时会自动使用全部CPU核心，但是提升速度依然有限。
CUDA可以显著加速离线翻译时间，由于作者显卡是魔改版1080，windows下更不了驱动，因此只测试了linux下的CUDA加速,这是不同模式的时间统计图。

<img src="./src/onepitranslator/resources/images/cuda-time.png" alt="CUDA 时间统计" width="300">


### 🌍 语言设置

下载后程序应自动切换到系统所在地区的语言，如果没有，可以手动选择：

<img src="./src/onepitranslator/resources/images/cnshow4.png" alt="img3" width="300">


### 📝 翻译器选择

选择需要的翻译器，建议先通过文本翻译进行测试。大部分翻译器需要 API Key，有关是否有免费 API Key 以及申请难度，可以在《选项及设置》中查看。双击网址即可跳转。

<img src="./src/onepitranslator/resources/images/enshow2.png" alt="img4" width="300">

### 📂 文件/文件夹名批量翻译

支持选择单文件夹内的全部文件（不包括子文件夹），或单独选择几个文件（使用 SHIFT 多选或 CTRL 单选）。翻译后可双击或右键修改，选中项可按 Delete 或右键删除。支持批量重命名，并可撤销修改，退回原文件名。

  <img src="./src/onepitranslator/resources/images/cnshow5.png" alt="img6" width="300">

## 🛠️ 示例使用场景

- **翻译整合**: 整合多个翻译并具有记住apikey的功能（**一定要记得 _点保存apikey按钮_！！！**）。
- **文件名翻译**: 自动将文件或文件夹名称翻译为目标语言，方便跨语言团队协作。
- **文本翻译**: 支持多种语言的实时翻译，适合需要即时翻译文本的场景。


## 🔗 链接
- **📹 视频**:
- ***[哔哩哔哩](https://www.bilibili.com/video/BV1hvm7YfEsm/)***
- ***[西瓜视频](https://www.ixigua.com/7425847299806331418***
- ***[youtube](https://youtube.com/@onepi-i8x?si=QrX5QF_QR-iaBArL)***
- ***[tiktok](https://www.tiktok.com/@onepizen)***

- **📄 文档**: [https://github.com/OnePi-1pi/OnePiTranslator/README_zh.md](https://github.com/OnePi-1pi/OnePiTranslator/README_zh.md)
- **🌐 GitHub**: [https://github.com/OnePi-1pi/OnePiTranslator](https://github.com/OnePi-1pi/OnePiTranslator)
- **deep-translator**:https://github.com/nidhaloff/deep-translator
- **argos-translate**:https://github.com/nidhaloff/deep-translator
- **ttkbootstrap**:https://github.com/israel-dryer/ttkbootstrap

