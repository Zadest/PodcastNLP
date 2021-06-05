#! /usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import tkinter as TK

def main_without_GUI():
    print('>>> Hallo in der Konsole!')
    return

def main_with_GUI():
    print('>>> Hallo in der GUI!')
    return

if __name__ == "__main__":
    if "gui" in sys.argv:
        main_with_GUI()
    else:
        main_without_GUI()
    