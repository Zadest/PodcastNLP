#! /usr/bin/env python3
# -*- coding: utf8 -*-

import os
import matplotlib.pyplot as plt
import speech_recognition as sr
from decorators import timer

@timer
def test():
    print("Hallo!")

if __name__ == "__main__":
    print("Hello!")
    test()
