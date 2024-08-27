
# OnePi Multi-functional Translator
A simple GUI tool for translating text or documents and renaming files or folder names. Uses online (deeptranslator) and offline (Argos Translate) translation.
---

English | [中文](README_zh.md)

An integrated GUI program of offline translation Argos Translate and online translation DeepTranslator, which can be used to translate text, documents or batch translate and rename files or folders. Fixed some minor bugs in DeepTranslator and optimized Argos Translate.

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

<img src="./resources/images/all.gif" alt="img1" width="400">

# Table of Contents

- [Features](#✨-features)
- [Installation](#🚀-installation)
- [Instructions](#📖-instructions)
- [Video and Documentation Links](#🔗-links)

### The video ⬆️ provides more detailed instructions
## ✨ Features

- 🌐 **Supports Multiple Languages**  
  Supported language options include: Simplified Chinese, English, العربية, Français, Español, Português, Deutsch, 한국어, Italiano, 日本語, Русский, Polski, हिन्दी, Türkçe, ไทย, Traditional Chinese.
  


- ⚙️ **Multiple Translation Engine Integration**  
  Combines online translation (via DeepTranslator) and offline translation (via Argos Translate), and can store API keys, switching between them with one click as needed.


  
  <img src="./resources/images/enshow4.png" alt="img5" width="300">

- 📁 **Batch Translation and Renaming**  
  Supports batch translation of file names or folder names, which can be manually changed after translation, and original file names can be added, then renamed, with undo operation supported after renaming.

  <img src="./resources/images/cnshow5.png" alt="img6" width="300">



## 🚀 Installation

### 1️⃣ Installation Package (Recommended for Windows Systems)

---

***Note: Running Argos Translate on Windows requires the [Microsoft Visual C++ Redistributable](https://visualstudio.microsoft.com/zh-hans/downloads/#microsoft-visual-c-redistributable-for-visual-studio-2022) and LLVM/OpenMP (the official C++ release does not include this library; you can try the development version or simply download [libomp140.x86_64.dll](G:\GitHub\OnePiTranslator\resources\libomp140.x86_64.dll) and move it to `C:\Windows\System32`).  package 3 and 4 will auto install it ,so no additional download is needed.***
---


- 1.💻 **Online Installation Package _size:~25M_** [Link](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/online_install_windows.exe)

  Download and install to use, no code operation required at all. Suitable for those with good internet connection. After installation, modules still need to be downloaded. 

- 2.📦 **Package without Argos (Author's Recommendation) _size:~35M_** [Link](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/no_argos_install_windows.exe)
  
  Only need to download this package to use online translation. If offline translation is needed later, it can be installed through `install_argos_translate.bat` in the working directory.

- 3.💽 **Complete Online and Offline Translation Installation Package _size: ~250M_** [Link](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/all_local_install_windows.exe)  
  Includes all necessary components except for the Argos language pack and the CUDA acceleration component. The size is relatively large, and after installation, online translation can be used. Offline translation requires the separate download of language packs [Link](https://github.com/argosopentech/argos-translate?tab=readme-ov-file#packages), or you can directly download the well-packaged complete package ↓↓↓↓.

- 4.🖥️ **Complete Installation Package with Language Packs Package _size: ~2G__** [Link](https://github.com/OnePi-1pi/OnePiTranslator/releases/download/V1.0.0/all_add_language_package_windows.exe)   
  Includes all components (except CUDA). The size is very large. Comes with language packs {Simplified Chinese: zh, Traditional Chinese: zt, English: en, French: fr, Spanish: es, German: de, Korean: ko, Japanese: ja, Russian: ru}.



### 2️⃣ PyPI Installation (for Users with Python Already Installed)
#### just install online translate

```bash
python -m pip install onepitranslator
```

### then run :

```bash
python -m  onepitranslator
```
### Note that a shortcut will be created on the desktop after running, just delete it if you don't want it, and it will not be created again.

#### If you need to use offline translation, you can continue to install argostranslate:

```bash
python -m pip install argostranslate spacy
```

In addition, offline translation also requires downloading the `xx_sent_ud_sm` module of spacy:

```bash
python -m spacy download xx_sent_ud_sm
```
Or download manually: ➡️
[Download Link](https://spacy.io/models/xx#xx_sent_ud_sm)

The current version of argostranslate may not be available due to the numpy upgrade, so you can roll back the version:

```bash
python -m pip install "numpy>=1.0.0,<2.0.0"
```
download language packs [Link](https://github.com/argosopentech/argos-translate?tab=readme-ov-file#packages)

run software  select _Options and Settings_ choose _Install Local Translation Language Library_ to install language packs

## 📖 Instructions

### ⏳  Regarding Argos and CUDA
Although Argos has been optimized and will automatically use all CPU cores when dealing with large volumes of text, the speed increase is still limited.
CUDA can significantly speed up offline translation time. Since the author's graphics card is a modified version of the gtx1080, and the driver cannot be updated under Windows, only the CUDA acceleration on Linux has been tested. This is a time statistics chart for different modes.

  <img src="./resources/images/cuda-time.png" alt="CUDA Time Statistics" width="300">
### 🌍 Language Settings

After downloading, the program should automatically switch to the language of the system's region. If not, you can manually select:

<img src="./resources/images/cnshow4.png" alt="img3" width="300">



### 📝 Translator Selection

Choose the needed translator, it's recommended to test with text translation first. Most translators require an API Key. You can check in 'Options and Settings' for information about free API Keys and application difficulty. Double-click the URL to jump to it.

<img src="./resources/images/enshow2.png" alt="img4" width="300">


### 📂 Batch Translation of File/Folder Names

Supports selecting all files within a single folder (including subfolders), or selecting several files individually (use SHIFT for multiple selection or CTRL for single selection). After translation, you can double-click or right-click to modify, selected items can be deleted by pressing Delete or right-clicking. Supports batch renaming and can undo changes to revert to original file names.

## 🛠️ Example Use Cases

- **Translation Integration**: Integrates multiple translations and has the function of remembering API keys (**Remember to _click the save API key button_!!!**).
- **File Name Translation**: Automatically translates file or folder names into the target language, facilitating cross-language team collaboration.
- **Text Translation**: Supports real-time translation in multiple languages, suitable for scenarios requiring instant text translation.

## 🔗 Links
- **📹 Videos**:
- ***[youtube](https://youtube.com/@onepi-i8x?si=QrX5QF_QR-iaBArL)***
- ***[tiktok](https://www.tiktok.com/@onepizen)***
- ***[Bilibili](https://www.bilibili.com/video/BV1mQe5ePEUp/?share_source=copy_web&vd_source=2479572e87b2a5619bdc6332186b5269)***
- ***[Xigua Video](https://www.ixigua.com/7403916189837853195)***

- **📄 Documentation**: [https://github.com/OnePi-1pi/OnePiTranslator/README_zh.md](https://github.com/OnePi-1pi/OnePiTranslator/README_zh.md)
- **🌐 GitHub**: [https://github.com/OnePi-1pi/OnePiTranslator](https://github.com/OnePi-1pi/OnePiTranslator)
- **deep-translator**: https://github.com/nidhaloff/deep-translator
- **argos-translate**: https://github.com/nidhaloff/deep-translator
- **ttkbootstrap**: https://github.com/israel-dryer/ttkbootstrap

## ❓ Unresolved Issues
When using CUDA to accelerate argostranslate translation, the GPU cannot exert its full capability, seemingly due to an I/O bottleneck. The versions of torch, CUDA, and drivers all match. Attempts to adjust torch parameters, including increasing Batch Size, have not resolved this issue.

<img src="./resources/images/CUDAandNV.jpg" alt="img1" width="300">

---