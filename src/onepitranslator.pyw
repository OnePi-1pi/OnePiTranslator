#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing as mp
import onepi
if __name__ == "__main__":
    mp.set_start_method('spawn') 
    onepi.main()