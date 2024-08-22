#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#参数传入:需要翻译的列表或文本,原语言,目标语言,api_key,间隔时间,逐行翻译

import os
import time
import math
import signal
import requests
import regex as re
from pathlib import Path
import deep_translator as dt 
from functools import partial 
from multiprocessing import Process, Pipe
from deep_translator.validate import is_input_valid
from concurrent.futures import ProcessPoolExecutor 
from deep_translator.exceptions import  MicrosoftAPIerror

# 设置环境变量以使用GPU
os.environ["ARGOS_DEVICE_TYPE"] = "auto"
def loadModel():
    global argotransmodel
    from argostranslate.translate import translate as argotransmodel
argodict ={'chinese (simplified)': 'zh', 'chinese (traditional)': 'zt', 'english': 'en', 'french': 'fr', 'spanish': 'es', 'german': 'de', 'korean': 'ko', 'japanese': 'ja', 'russian': 'ru'}
googledict={'auto': 'auto', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'english': 'en', 'arabic': 'ar', 'french': 'fr', 'spanish': 'es', 'portuguese': 'pt', 'german': 'de', 'korean': 'ko', 'italian': 'it', 'japanese': 'ja', 'russian': 'ru', 'vietnamese': 'vi', 'polish': 'pl', 'hindi': 'hi', 'turkish': 'tr', 'thai': 'th', 'swedish': 'sv', 'dutch': 'nl', 'czech': 'cs', 'greek': 'el', 'hebrew': 'iw', 'danish': 'da', 'finnish': 'fi', 'hungarian': 'hu', 'romanian': 'ro', 'slovak': 'sk', 'serbian': 'sr', 'bulgarian': 'bg', 'croatian': 'hr', 'lithuanian': 'lt', 'latvian': 'lv', 'estonian': 'et', 'slovenian': 'sl', 'maltese': 'mt', 'catalan': 'ca', 'galician': 'gl', 'basque': 'eu', 'albanian': 'sq', 'malayalam': 'ml', 'tamil': 'ta', 'telugu': 'te', 'kannada': 'kn', 'marathi': 'mr', 'sinhala': 'si', 'khmer': 'km', 'myanmar': 'my', 'lao': 'lo', 'nepali': 'ne', 'amharic': 'am', 'javanese': 'jw', 'sundanese': 'su', 'welsh': 'cy', 'swahili': 'sw', 'xhosa': 'xh', 'zulu': 'zu', 'yoruba': 'yo', 'igbo': 'ig', 'hausa': 'ha', 'pashto': 'ps', 'punjabi': 'pa', 'gujarati': 'gu', 'odia (oriya)': 'or', 'turkmen': 'tk', 'uyghur': 'ug', 'uzbek': 'uz', 'tatar': 'tt', 'tajik': 'tg', 'afrikaans': 'af', 'irish': 'ga', 'yiddish': 'yi', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'cebuano': 'ceb', 'chichewa': 'ny', 'corsican': 'co', 'dhivehi': 'dv', 'dogri': 'doi', 'esperanto': 'eo', 'ewe': 'ee', 'filipino': 'tl', 'frisian': 'fy', 'georgian': 'ka', 'guarani': 'gn', 'haitian creole': 'ht', 'hawaiian': 'haw', 'hmong': 'hmn', 'icelandic': 'is', 'ilocano': 'ilo', 'indonesian': 'id', 'kazakh': 'kk', 'kinyarwanda': 'rw', 'konkani': 'gom', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'latin': 'la', 'lingala': 'ln', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'maori': 'mi', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'norwegian': 'no', 'oromo': 'om', 'persian': 'fa', 'quechua': 'qu', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'somali': 'so', 'tigrinya': 'ti', 'tsonga': 'ts', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur'}
libredict ={'auto': 'auto', 'chinese (simplified)': 'zh', 'chinese (traditional)': 'zh', 'english': 'en', 'arabic': 'ar', 'french': 'fr', 'spanish': 'es', 'portuguese': 'pt', 'german': 'de', 'korean': 'ko', 'italian': 'it', 'japanese': 'ja', 'russian': 'ru', 'vietnamese': 'vi', 'polish': 'pl', 'hindi': 'hi', 'turkish': 'tr', 'irish': 'ga', 'indonesian': 'id'}
mymemorydict ={'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'english': 'en-GB', 'arabic': 'ar-SA', 'french': 'fr-FR', 'spanish': 'es-ES', 'portuguese': 'pt-PT', 'german': 'de-DE', 'korean': 'ko-KR', 'italian': 'it-IT', 'japanese': 'ja-JP', 'russian': 'ru-RU', 'vietnamese': 'vi-VN', 'polish': 'pl-PL', 'hindi': 'hi-IN', 'turkish': 'tr-TR', 'thai': 'th-TH', 'swedish': 'sv-SE', 'dutch': 'nl-NL', 'czech': 'cs-CZ', 'greek': 'el-GR', 'hebrew': 'he-IL', 'danish': 'da-DK', 'finnish': 'fi-FI', 'hungarian': 'hu-HU', 'romanian': 'ro-RO', 'slovak': 'sk-SK', 'bulgarian': 'bg-BG', 'croatian': 'hr-HR', 'lithuanian': 'lt-LT', 'latvian': 'lv-LV', 'estonian': 'et-EE', 'slovenian': 'sl-SI', 'maltese': 'mt-MT', 'catalan': 'ca-ES', 'galician': 'gl-ES', 'basque': 'eu-ES', 'albanian': 'sq-AL', 'malayalam': 'ml-IN', 'telugu': 'te-IN', 'kannada': 'kn-IN', 'marathi': 'mr-IN', 'sinhala': 'si-LK', 'khmer': 'km-KH', 'lao': 'lo-LA', 'nepali': 'ne-NP', 'amharic': 'am-ET', 'javanese': 'jv-ID', 'sundanese': 'su-ID', 'welsh': 'cy-GB', 'swahili': 'sw-KE', 'xhosa': 'xh-ZA', 'zulu': 'zu-ZA', 'yoruba': 'yo-NG', 'hausa': 'ha-NE', 'pashto': 'ps-PK', 'punjabi': 'pa-IN', 'gujarati': 'gu-IN', 'turkmen': 'tk-TM', 'uzbek': 'uz-UZ', 'tatar': 'tt-RU', 'tajik': 'tg-TJ', 'afrikaans': 'af-ZA', 'yiddish': 'yi-YD', 'acehnese': 'ace-ID', 'akan': 'ak-GH', 'antigua and barbuda creole english': 'aig-AG', 'arabic egyptian': 'ar-EG', 'aragonese': 'an-ES', 'armenian': 'hy-AM', 'assamese': 'as-IN', 'asturian': 'ast-ES', 'austrian german': 'de-AT', 'awadhi': 'awa-IN', 'ayacucho quechua': 'quy-PE', 'azerbaijani': 'az-AZ', 'bahamas creole english': 'bah-BS', 'bajan': 'bjs-BB', 'balinese': 'ban-ID', 'balkan gipsy': 'rm-RO', 'bambara': 'bm-ML', 'banjar': 'bjn-ID', 'bashkir': 'ba-RU', 'belarusian': 'be-BY', 'belgian french': 'fr-BE', 'bemba': 'bem-ZM', 'bengali': 'bn-IN', 'bhojpuri': 'bho-IN', 'bihari': 'bh-IN', 'bislama': 'bi-VU', 'borana': 'gax-KE', 'bosnian': 'bs-BA', 'bosnian (cyrillic)': 'bs-Cyrl-BA', 'breton': 'br-FR', 'buginese': 'bug-ID', 'burmese': 'my-MM', 'catalan valencian': 'cav-ES', 'cebuano': 'ceb-PH', 'central atlas tamazight': 'tzm-MA', 'central aymara': 'ayr-BO', 'central kanuri (latin script)': 'knc-NG', 'chadian arabic': 'shu-TD', 'chamorro': 'ch-GU', 'cherokee': 'chr-US', 'chhattisgarhi': 'hne-IN', 'chinese trad. (hong kong)': 'zh-HK', 'chinese (traditional macau)': 'zh-MO', 'chittagonian': 'ctg-BD', 'chokwe': 'cjk-AO', 'classical greek': 'grc-GR', 'comorian ngazidja': 'zdj-KM', 'coptic': 'cop-EG', 'crimean tatar': 'crh-RU', 'crioulo upper guinea': 'pov-GW', 'dari': 'prs-AF', 'dimli': 'diq-TR', 'dyula': 'dyu-CI', 'dzongkha': 'dz-BT', 'eastern yiddish': 'ydd-US', 'emakhuwa': 'vmw-MZ', 'english australia': 'en-AU', 'english canada': 'en-CA', 'english india': 'en-IN', 'english ireland': 'en-IE', 'english new zealand': 'en-NZ', 'english singapore': 'en-SG', 'english south africa': 'en-ZA', 'english us': 'en-US', 'esperanto': 'eo-EU', 'ewe': 'ee-GH', 'fanagalo': 'fn-FNG', 'faroese': 'fo-FO', 'fijian': 'fj-FJ', 'filipino': 'fil-PH', 'flemish': 'nl-BE', 'fon': 'fon-BJ', 'french canada': 'fr-CA', 'french swiss': 'fr-CH', 'friulian': 'fur-IT', 'fula': 'ff-FUL', 'gamargu': 'mfi-NG', 'garo': 'grt-IN', 'georgian': 'ka-GE', 'gilbertese': 'gil-KI', 'glavda': 'glw-NG', 'grenadian creole english': 'gcl-GD', 'guarani': 'gn-PY', 'guyanese creole english': 'gyn-GY', 'haitian creole french': 'ht-HT', 'halh mongolian': 'khk-MN', 'hawaiian': 'haw-US', 'higi': 'hig-NG', 'hiligaynon': 'hil-PH', 'hill mari': 'mrj-RU', 'hmong': 'hmn-CN', 'icelandic': 'is-IS', 'igbo ibo': 'ibo-NG', 'igbo ig': 'ig-NG', 'ilocano': 'ilo-PH', 'indonesian': 'id-ID', 'inuktitut greenlandic': 'kl-GL', 'irish gaelic': 'ga-IE', 'italian swiss': 'it-CH', 'jamaican creole english': 'jam-JM', 'jingpho': 'kac-MM', "k'iche'": 'quc-GT', 'kabiyè': 'kbp-TG', 'kabuverdianu': 'kea-CV', 'kabylian': 'kab-DZ', 'kalenjin': 'kln-KE', 'kamba': 'kam-KE', 'kanuri': 'kr-KAU', 'karen': 'kar-MM', 'kashmiri (devanagari script)': 'ks-IN', 'kashmiri (arabic script)': 'kas-IN', 'kazakh': 'kk-KZ', 'khasi': 'kha-IN', 'kikuyu kik': 'kik-KE', 'kikuyu ki': 'ki-KE', 'kimbundu': 'kmb-AO', 'kinyarwanda': 'rw-RW', 'kirundi': 'rn-BI', 'kisii': 'guz-KE', 'kongo': 'kg-CG', 'konkani': 'kok-IN', 'northern kurdish': 'kmr-TR', 'kurdish sorani': 'ckb-IQ', 'kyrgyz': 'ky-KG', 'latgalian': 'ltg-LV', 'latin': 'la-XN', 'ligurian': 'lij-IT', 'limburgish': 'li-NL', 'lingala': 'ln-LIN', 'lombard': 'lmo-IT', 'luba-kasai': 'lua-CD', 'luganda': 'lg-UG', 'luhya': 'luy-KE', 'luo': 'luo-KE', 'luxembourgish': 'lb-LU', 'maa': 'mas-KE', 'macedonian': 'mk-MK', 'magahi': 'mag-IN', 'maithili': 'mai-IN', 'malagasy': 'mg-MG', 'malay': 'ms-MY', 'maldivian': 'dv-MV', 'mandara': 'mfi-CM', 'manipuri': 'mni-IN', 'manx gaelic': 'gv-IM', 'maori': 'mi-NZ', 'margi': 'mrt-NG', 'mari': 'mhr-RU', 'marshallese': 'mh-MH', 'mende': 'men-SL', 'meru': 'mer-KE', 'mijikenda': 'nyf-KE', 'minangkabau': 'min-ID', 'mizo': 'lus-IN', 'mongolian': 'mn-MN', 'montenegrin': 'sr-ME', 'morisyen': 'mfe-MU', 'moroccan arabic': 'ar-MA', 'mossi': 'mos-BF', 'ndau': 'ndc-MZ', 'ndebele': 'nr-ZA', 'nigerian fulfulde': 'fuv-NG', 'niuean': 'niu-NU', 'north azerbaijani': 'azj-AZ', 'sesotho': 'nso-ZA', 'northern uzbek': 'uzn-UZ', 'norwegian bokmål': 'nb-NO', 'norwegian nynorsk': 'nn-NO', 'nuer': 'nus-SS', 'nyanja': 'ny-MW', 'occitan': 'oc-FR', 'occitan aran': 'oc-ES', 'odia': 'or-IN', 'oriya': 'ory-IN', 'urdu': 'ur-PK', 'palauan': 'pau-PW', 'pali': 'pi-IN', 'pangasinan': 'pag-PH', 'papiamentu': 'pap-CW', 'persian': 'fa-IR', 'pijin': 'pis-SB', 'plateau malagasy': 'plt-MG', 'portuguese brazil': 'pt-BR', 'potawatomi': 'pot-US', 'punjabi (pakistan)': 'pnb-PK', 'quechua': 'qu-PE', 'rohingya': 'rhg-MM', 'rohingyalish': 'rhl-MM', 'romansh': 'roh-CH', 'rundi': 'run-BI', 'saint lucian creole french': 'acf-LC', 'samoan': 'sm-WS', 'sango': 'sg-CF', 'sanskrit': 'sa-IN', 'santali': 'sat-IN', 'sardinian': 'sc-IT', 'scots gaelic': 'gd-GB', 'sena': 'seh-ZW', 'serbian cyrillic': 'sr-Cyrl-RS', 'serbian latin': 'sr-Latn-RS', 'seselwa creole french': 'crs-SC', 'setswana (south africa)': 'tn-ZA', 'shan': 'shn-MM', 'shona': 'sn-ZW', 'sicilian': 'scn-IT', 'silesian': 'szl-PL', 'sindhi snd': 'snd-PK', 'sindhi sd': 'sd-PK', 'somali': 'so-SO', 'sotho southern': 'st-LS', 'south azerbaijani': 'azb-AZ', 'southern pashto': 'pbt-PK', 'southwestern dinka': 'dik-SS', 'spanish argentina': 'es-AR', 'spanish colombia': 'es-CO', 'spanish latin america': 'es-419', 'spanish mexico': 'es-MX', 'spanish united states': 'es-US', 'sranan tongo': 'srn-SR', 'standard latvian': 'lvs-LV', 'standard malay': 'zsm-MY', 'swati': 'ss-SZ', 'swiss german': 'de-CH', 'syriac (aramaic)': 'syc-TR', 'tagalog': 'tl-PH', 'tahitian': 'ty-PF', 'tamashek (tuareg)': 'tmh-DZ', 'tamasheq': 'taq-ML', 'tamil india': 'ta-IN', 'tamil sri lanka': 'ta-LK', 'taroko': 'trv-TW', 'tetum': 'tet-TL', 'tibetan': 'bo-CN', 'tigrinya': 'ti-ET', 'tok pisin': 'tpi-PG', 'tokelauan': 'tkl-TK', 'tongan': 'to-TO', 'tosk albanian': 'als-AL', 'tsonga': 'ts-ZA', 'tswa': 'tsc-MZ', 'tswana': 'tn-BW', 'tumbuka': 'tum-MW', 'tuvaluan': 'tvl-TV', 'twi': 'tw-GH', 'udmurt': 'udm-RU', 'ukrainian': 'uk-UA', 'uma': 'ppk-ID', 'umbundu': 'umb-AO', 'uyghur uig': 'uig-CN', 'uyghur ug': 'ug-CN', 'venetian': 'vec-IT', 'vincentian creole english': 'svc-VC', 'virgin islands creole english': 'vic-US', 'wallisian': 'wls-WF', 'waray (philippines)': 'war-PH', 'west central oromo': 'gaz-ET', 'western persian': 'pes-IR', 'wolof': 'wo-SN'}
baidudict={'auto': 'auto', 'chinese (simplified)': 'zh', 'chinese (traditional)': 'cht', 'english': 'en', 'arabic': 'ara', 'french': 'fra', 'spanish': 'spa', 'portuguese': 'pt', 'german': 'de', 'korean': 'kor', 'italian': 'it', 'japanese': 'jp', 'russian': 'ru', 'vietnamese': 'vie', 'polish': 'pl', 'thai': 'th', 'swedish': 'swe', 'dutch': 'nl', 'czech': 'cs', 'greek': 'el', 'danish': 'dan', 'finnish': 'fin', 'hungarian': 'hu', 'romanian': 'ro', 'bulgarian': 'bul', 'estonian': 'est', 'slovenian': 'slo', 'chinese (classical)': 'wyw', 'yueyu': 'yue'}
ponsdict  ={'chinese (simplified)': 'zh-cn', 'english': 'en', 'arabic': 'ar', 'french': 'fr', 'spanish': 'es', 'portuguese': 'pt', 'german': 'de', 'italian': 'it', 'russian': 'ru', 'polish': 'pl', 'turkish': 'tr', 'swedish': 'sv', 'dutch': 'nl', 'czech': 'cs', 'greek': 'el', 'danish': 'da', 'hungarian': 'hu', 'bulgarian': 'bg', 'slovenian': 'sl', 'latin': 'la', 'norwegian': 'no', 'elvish': 'elv'}
lingueedict  ={'chinese (simplified)': 'chinese', 'english': 'english', 'french': 'french', 'spanish': 'spanish', 'portuguese': 'portuguese', 'german': 'german', 'italian': 'italian', 'japanese': 'japanese', 'russian': 'russian', 'polish': 'polish', 'swedish': 'swedish', 'dutch': 'dutch', 'czech': 'czech', 'greek': 'greek', 'danish': 'danish', 'finnish': 'finnish', 'hungarian': 'hungarian', 'romanian': 'romanian', 'bulgarian': 'bulgarian', 'latvian': 'latvian', 'estonian': 'estonian', 'slovenian': 'slovenian', 'maltese': 'maltese', 'slovakian': 'slovakian', 'laotian': 'laotian'}
microsoftdict ={'auto': 'auto', 'chinese (simplified)': 'zh-hans', 'chinese (traditional)': 'zh-hant', 'english': 'en', 'arabic': 'ar', 'french': 'fr', 'spanish': 'es', 'german': 'de', 'korean': 'ko', 'italian': 'it', 'japanese': 'ja', 'russian': 'ru', 'vietnamese': 'vi', 'polish': 'pl', 'hindi': 'hi', 'turkish': 'tr', 'thai': 'th', 'swedish': 'sv', 'dutch': 'nl', 'czech': 'cs', 'greek': 'el', 'hebrew': 'he', 'danish': 'da', 'finnish': 'fi', 'hungarian': 'hu', 'romanian': 'ro', 'slovak': 'sk', 'bulgarian': 'bg', 'croatian': 'hr', 'lithuanian': 'lt', 'latvian': 'lv', 'estonian': 'et', 'slovenian': 'sl', 'maltese': 'mt', 'catalan': 'ca', 'galician': 'gl', 'basque': 'eu', 'albanian': 'sq', 'malayalam': 'ml', 'tamil': 'ta', 'telugu': 'te', 'kannada': 'kn', 'marathi': 'mr', 'sinhala': 'si', 'khmer': 'km', 'lao': 'lo', 'nepali': 'ne', 'amharic': 'am', 'welsh': 'cy', 'swahili': 'sw', 'xhosa': 'xh', 'zulu': 'zu', 'yoruba': 'yo', 'igbo': 'ig', 'hausa': 'ha', 'pashto': 'ps', 'kashmiri': 'ks', 'punjabi': 'pa', 'gujarati': 'gu', 'turkmen': 'tk', 'uyghur': 'ug', 'tatar': 'tt', 'afrikaans': 'af', 'irish': 'ga', 'assamese': 'as', 'azerbaijani': 'az', 'bashkir': 'ba', 'bhojpuri': 'bho', 'bangla': 'bn', 'tibetan': 'bo', 'bodo': 'brx', 'bosnian': 'bs', 'dogri': 'doi', 'lower sorbian': 'dsb', 'divehi': 'dv', 'persian': 'fa', 'filipino': 'fil', 'fijian': 'fj', 'faroese': 'fo', 'french (canada)': 'fr-ca', 'konkani': 'gom', 'chhattisgarhi': 'hne', 'upper sorbian': 'hsb', 'haitian creole': 'ht', 'armenian': 'hy', 'indonesian': 'id', 'inuinnaqtun': 'ikt', 'icelandic': 'is', 'inuktitut': 'iu', 'inuktitut (latin)': 'iu-latn', 'georgian': 'ka', 'kazakh': 'kk', 'kurdish (northern)': 'kmr', 'kurdish (central)': 'ku', 'kyrgyz': 'ky', 'lingala': 'ln', 'ganda': 'lug', 'chinese (literary)': 'lzh', 'maithili': 'mai', 'malagasy': 'mg', 'māori': 'mi', 'macedonian': 'mk', 'mongolian (cyrillic)': 'mn-cyrl', 'mongolian (traditional)': 'mn-mong', 'manipuri': 'mni', 'malay': 'ms', 'hmong daw': 'mww', 'myanmar (burmese)': 'my', 'norwegian': 'nb', 'sesotho sa leboa': 'nso', 'nyanja': 'nya', 'odia': 'or', 'querétaro otomi': 'otq', 'dari': 'prs', 'portuguese (brazil)': 'pt', 'portuguese (portugal)': 'pt-pt', 'rundi': 'run', 'kinyarwanda': 'rw', 'sindhi': 'sd', 'samoan': 'sm', 'shona': 'sn', 'somali': 'so', 'serbian (cyrillic)': 'sr-cyrl', 'serbian (latin)': 'sr-latn', 'sesotho': 'st', 'tigrinya': 'ti', 'klingon (latin)': 'tlh-latn', 'klingon (piqad)': 'tlh-piqd', 'setswana': 'tn', 'tongan': 'to', 'tahitian': 'ty', 'ukrainian': 'uk', 'urdu': 'ur', 'uzbek (latin)': 'uz', 'yucatec maya': 'yua', 'cantonese (traditional)': 'yue'}
deepldict ={'chinese (simplified)': 'zh', 'chinese (traditional)': 'zh', 'english': 'en', 'french': 'fr', 'spanish': 'es', 'portuguese': 'pt', 'german': 'de', 'italian': 'it', 'japanese': 'ja', 'russian': 'ru', 'polish': 'pl', 'turkish': 'tr', 'swedish': 'sv', 'dutch': 'nl', 'czech': 'cs', 'greek': 'el', 'danish': 'da', 'finnish': 'fi', 'hungarian': 'hu', 'romanian': 'ro', 'slovak': 'sk', 'bulgarian': 'bg', 'lithuanian': 'lt', 'latvian': 'lv', 'estonian': 'et', 'slovenian': 'sl', 'indonesian': 'id', 'ukrainian': 'uk'}
papagodict={'auto': 'auto', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'english': 'en', 'french': 'fr', 'spanish': 'es', 'korean': 'ko', 'japanese': 'ja', 'vietnamese': 'vi', 'thai': 'th', 'indonesia': 'id'}
yandexdict = googledict
chatgptdict = googledict

corenum = os.cpu_count()
t1 = time.time()
try_num = 1
#将正则表达式的样式编译为一个 正则表达式对象 pr
pr=re.compile(r'[^\p{L}\p{N}\p{M}\n]')




def wait_time(x):
    if x <= 30:
        return max(x,8)
    elif x <= 300:
        scaled_a = (x - 30) / 270
        b = x * (1 - 0.9 * math.log10(1 + scaled_a * 9))
        return b
    else:
        return x / 10

def run_target(pipe,func, arg):
    try:
        result = func(arg)
        pipe.send(result)
    except BaseException as e:
        pipe.send(e)
    pipe.close()

def run_with_timeout(func, arg):
    global result
    result = None
    wtime=wait_time(len(arg))
    parent_conn, child_conn = Pipe()  # 创建一个管道
    # 创建 Process 对象,将目标函数和参数传递给它
    if wtime < 100:
        result =  func(arg)
    else:
        p = Process(target=run_target, args=(child_conn,func, arg))
        
        p.start()
        child_pid =p.pid
        p.join(wtime)
        # 如果子进程超时,尝试终止,不成功则终止父进程
        if p.is_alive():
            os.kill(child_pid, signal.SIGTERM)
            raise TimeoutError('网络超时')
        result = parent_conn.recv()
    return result
    # 尝试获取结果,如果超时可能需要处理异常或返回特定值

def s2l(slist_or_str,split_len = 0):
    #先检查是否为字符串 
    if isinstance(slist_or_str,str):
        #是字符串则转为小写替换下划线后原样输出
        ss=re.sub('[_-]',' ',slist_or_str.lower())
        ss = ss.strip()
    else:
        #不是字符串则替换符号为空格并将每个元素加换行符形成字符串存为ss
        ss=pr.sub(' ','\n'.join(slist_or_str).lower())
    #如果指定了分割长度
    if split_len != 0 :
        #则使用指定分割
        split_num = len(ss)//split_len+1
    else:
        #使用默认分割
        split_num = corenum
        split_len = 200
    if len(ss) >= split_len :
        #判断符号数量是否足够分割
        for split_str in ['\n',';' ,'.' , '。',' ' ,',' ,'，',"'" ,'"' ,'_','-','']:
            if ss.count(split_str) >= split_num:
                break
        #如果足够，即split_str数量>=分割数
        if split_str != '':
            splen=len(ss)//split_num
            #初始化位置坐标i
            sl=[]
            i,j=0,0
            for _ in range(split_num-1):
                i=ss.rfind(split_str,i,i+splen+2)
                if i == j-1 :
                    i += splen
                else :
                    sl.append(ss[j:i])
                    j=i+1
            if j-1 < len(ss)-2:
                sl.append(ss[j:])
        #如果无法找到合适的分割符，则直接切片
        else:
            # 使用生成的索引序列来分割文本
            sl = [ss[i:i + split_len] for i in split_num ]
        return sl, split_str
    else:
        return ss,'\n'

def OfflineTranslantor(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    # 参数:slist_or_str: 待翻译的字符串或字符串列表.slg: 源语言代码,'auto'表示自动识别.tlg: 目标语言代码.key: 翻译引擎的API密钥.sleep_time: 调用翻译API之间的间隔时间,用于防止请求过于频繁.singaltrans: 布尔值,指示是否对每个单独的文件名进行翻译.返回:翻译后的字符串或字符串列表.
    # 打印调试信息
    slg=argodict[slg]
    tlg=argodict[tlg]
    translate_text_partial = partial(argotransmodel, from_code=slg, to_code=tlg)

    if singaltrans:
        if isinstance(slist_or_str,str):
            ss_or_sl = pr.sub(' ',slist_or_str.lower())
        else:
            ss_or_sl = pr.sub(' ' , '\n'.join(slist_or_str).lower())
            ss_or_sl = ss_or_sl.strip()
        ss_or_sl = ss_or_sl.splitlines()
        split_str ='\n'
    else:
        ss_or_sl,split_str = s2l(slist_or_str)
    if isinstance(ss_or_sl,str):
        tstr = argotransmodel(ss_or_sl,from_code=slg, to_code=tlg)
        tstr = pr.sub(' ', tstr)
        tlist = tstr.split(split_str)
    else:
        with ProcessPoolExecutor(max_workers=corenum) as executor:
            tmap = executor.map(translate_text_partial,ss_or_sl)
        tlist = [pr.sub(' ', i) for i in tmap]
    if isinstance(slist_or_str,str) or any(' ' in s for s in slist_or_str):
        #进来时是字符串或有空格
        o_o=' '
    else:
        #进来时是列表
        o_o='_'
    #去除两侧空格
    mmt = map(lambda x :pr.sub(o_o, x.strip()), tlist) 
    tlist_or_str = split_str.join(mmt)
    return tlist_or_str


# async def async_translate(func, arg):
#     async with asyncio.timeout(max(len(arg), 5)):
#         return  await asyncio.to_thread(func, arg)

#写没有key与source时的情况，直接从deep-translator对应父类代码里扒的。
class libnokeytr(dt.LibreTranslator):
    def __init__(
        self,
        base_url: str = None,
        languages: dict = libredict ,
        source: str = "auto",
        target: str = "en",
        payload_key = None,
        element_tag = None,
        element_query = None,
        api_key= None,
        **url_params,
    ):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self._base_url = base_url
        self._languages = languages
        self._supported_languages = list(self._languages.keys())
        self._source, self._target = source, target
        self._url_params = url_params
        self._element_tag = element_tag
        self._element_query = element_query
        self.payload_key = payload_key
        self.api_key = api_key
    def translate(self, text: str, **kwargs) :
        return super().translate(text, **kwargs)

class micnosourcetr(dt.MicrosoftTranslator):
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)
    def translate(self, text: str, **kwargs) -> str:

        response = None
        if is_input_valid(text):
            if self._source != 'auto':
                self._url_params["from"] = self._source
            self._url_params["to"] = self._target

            valid_microsoft_json = [{"text": text}]
            try:
                response = requests.post(
                    self._base_url,
                    params=self._url_params,
                    headers=self.headers,
                    json=valid_microsoft_json,
                    proxies=self.proxies,
                )
            except requests.exceptions.RequestException:
                pass

            # Where Microsoft API responds with an api error, it returns a dict in response.json()
            if type(response.json()) is dict:
                error_message = response.json()["error"]
                raise MicrosoftAPIerror(error_message)
            # Where it responds with a translation, its response.json() is a list
            # e.g. [{'translations': [{'text':'Hello world!', 'to': 'en'}]}]
            elif type(response.json()) is list:
                all_translations = [
                    i["text"] for i in response.json()[0]["translations"]
                ]
                return "\n".join(all_translations)


def translate_file(func, path,newpath):
    try:
        trans_text = func(path)
        if trans_text:
            with open(newpath, 'w',encoding='utf_8') as f:
                f.write(trans_text)
    except Exception as e:
        with open(Path(__file__).parent /'error.er', 'w',encoding='utf_8') as f:
            f.write(str(e))
    return

def DoTranslate(funt,split_len,slist_or_str, sleep_time, singaltrans,argdict):
    #文档翻译
    if  isinstance(slist_or_str,Path):
        txtpath = slist_or_str.with_suffix('.txt')
        sstem=txtpath.stem
        for i in range(1000):
            newpath = txtpath.with_stem(f"{sstem}{'_translated' + str(i)}")
            if not newpath.exists(): break
        p = Process(target=translate_file,args=(funt(**argdict).translate_file, slist_or_str,newpath),daemon=1)
        p.start()
        child_pid =p.pid
        return newpath,child_pid
    #文件和文件名翻译
    t2 = time.time()
    tlist_or_str = None
    if singaltrans:
        if isinstance(slist_or_str,str):
            ss_or_sl = slist_or_str.lower()
        else:
            ss_or_sl = pr.sub(' ' , '\n'.join(slist_or_str).lower())      
        ss_or_sl = ss_or_sl.splitlines()
        split_str = '\n'
    else:
        ss_or_sl,split_str = s2l(slist_or_str,split_len = split_len)
    
    if isinstance(ss_or_sl,str):
        ss_or_sl = re.sub('\n',' ;;\n',ss_or_sl)  
        tstr = run_with_timeout(funt(**argdict).translate, ss_or_sl)
        tlist_or_str = re.sub('[;；]','', tstr)
        time.sleep(sleep_time)


    else:
        trantext =None
        tls = []
        for text in ss_or_sl:
            text = re.sub('\n',' ;;\n',text)  
            # 翻译每一段，并使用传入的翻译函数
            trantext=run_with_timeout(funt(**argdict).translate, text)
            time.sleep(sleep_time)

            if isinstance(trantext, str):
                tls.append(re.sub('[;；]','',trantext).strip())
            else:
                raise TimeoutError('error,nothing return')
        tlist_or_str = split_str.join(tls)

    if isinstance(slist_or_str,str):
        return tlist_or_str
    elif any(' ' in s for s in slist_or_str):
        o_o=' '
    else:
        o_o='_'
    tlist_or_str = pr.sub(o_o , tlist_or_str).strip()
    return tlist_or_str

# async def async_translate(func, arg):
#     async with asyncio.timeout(max(len(arg), 5)):
#         return  await asyncio.to_thread(func, arg)

def DictTranslate(funt,slist_or_str, sleep_time, argdict):
        #因为是词典，进行单个单词翻译
    if isinstance(slist_or_str,str):
        slist_or_str=re.sub('\n','',slist_or_str)
        slist=slist_or_str.split(' ')
        tlist=[]
        for text in slist:
            tlist.append(funt(**argdict).translate(text))
            time.sleep(sleep_time)
        if len(slist) <= 1 :
            return tlist
        else:
            return ' '.join(tlist)
    else:
        tall=[]
        for ti in slist_or_str:
            tlist=[]
            slist=re.sub('\n','',slist)
            slist=ti.split(' ')
            for text in slist:
                tlist.append(funt(**argdict).translate(text))
                time.sleep(sleep_time)
            if len(slist) <= 1 :
                tall.append(tlist)
            else:
                tall.append(' '.join(tlist))
        return tall



def PonsTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    argdict = {'source':ponsdict[slg], 'target':ponsdict[tlg]}
    return DictTranslate(dt.PonsTranslator,slist_or_str, sleep_time, argdict)#定义LingueeTranslator函数

def LingueeTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    argdict = {'source':lingueedict[slg], 'target':lingueedict[tlg]}
    return DictTranslate(dt.LingueeTranslator,slist_or_str, sleep_time, argdict) 




def detection(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    if isinstance(slist_or_str,str):  
        return dt.single_detection(slist_or_str,api_key=key[0])
    else:
        return dt.batch_detection(slist_or_str,api_key=key[0])
   



def GoogleTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =3000
    argdict = {'source':googledict[slg], 'target':googledict[tlg]}
    return DoTranslate(dt.GoogleTranslator,split_len,slist_or_str,sleep_time, singaltrans,argdict)

def LibreTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =3000
    if key[0][:4] != 'http':
        key[0] = 'https://'+key[0]
    if key[1] :
        fun=dt.LibreTranslator
    else :
        fun=libnokeytr
    argdict = {'source':libredict[slg], 'target':libredict[tlg],'base_url':key[0],'api_key':key[1]}
    return DoTranslate(fun,split_len,slist_or_str,sleep_time, singaltrans,argdict)           

def BaiduTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =2000
    argdict = {'source':baidudict[slg], 'target':baidudict[tlg], 'appid':key[0], 'appkey':key[1]}
    return DoTranslate(dt.BaiduTranslator,split_len,slist_or_str,sleep_time, singaltrans,argdict)

def MyMemoryTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =400
    argdict = {'source':mymemorydict[slg], 'target':mymemorydict[tlg]}
    return DoTranslate(dt.MyMemoryTranslator,split_len,slist_or_str,sleep_time, singaltrans,argdict)

def DeeplTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =3000
    if key[0][-2:] == 'fx':
        usekey=True
    else:
        usekey=False
    argdict = {'source':deepldict[slg], 'target':deepldict[tlg],'api_key':key[0], 'use_free_api':usekey}
    return DoTranslate(dt.DeeplTranslator,split_len,slist_or_str,sleep_time, singaltrans,argdict)

def YandexTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =1000
    argdict = {'source':googledict[slg], 'target':googledict[tlg],'api_key':key[0]}
    return DoTranslate(dt.YandexTranslator,split_len,slist_or_str,sleep_time, singaltrans,argdict)            

def MicrosoftTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =3000
    argdict = {'target':microsoftdict[tlg],'api_key':key[0]}
    
    if key[1]:
        argdict['region'] = key[1]
    if slg == 'auto':
        func = micnosourcetr
    else:
        argdict['source'] = microsoftdict[slg]
        func = dt.MicrosoftTranslator
    return DoTranslate(func,split_len,slist_or_str,sleep_time, singaltrans,argdict)            

def ChatGptTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =1000
    if slg == 'auto':
        argdict = {'target':googledict[tlg],'api_key':key[0]}
    else:
        argdict = {'source':googledict[slg], 'target':googledict[tlg],'api_key':key[0]}
    return DoTranslate(dt.ChatGptTranslator,split_len,slist_or_str,sleep_time, singaltrans,argdict)  

def PapagoTranslator(slist_or_str, slg, tlg, key, sleep_time, singaltrans):
    split_len =1000
    argdict = {'source':papagodict[slg], 'target':papagodict[tlg],'client_id':key[0], 'secret_key':key[1]}
    return DoTranslate(dt.PapagoTranslator,split_len,slist_or_str,sleep_time, singaltrans,argdict)            



