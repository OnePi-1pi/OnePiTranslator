#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import math
import signal
import threading
import webbrowser
import subprocess
from pathlib import Path
import multiprocessing as mp
from tkinter import filedialog 
from multiprocessing import Process,Event
import tkinter as tk

a = tk.Tk()
a.geometry('500x1000+1000+700')
b = tk.Button(a)
a.mainloop()