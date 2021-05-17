#! /usr/bin/env python3
# -*- coding: utf8 -*-

import os
import matplotlib.pyplot as plt
from decorators import timer

@timer
def countOccurance(text):
    if type(text) == str:
       text = text.split(' ')
    wordOccurances = {}
    for token in text:
        if token in wordOccurances:
            wordOccurances[token] += 1
            continue
        wordOccurances[token] = 1
    return wordOccurances

@timer
def showOccurances(wordOccurances):
    plt.bar(wordOccurances.keys(),wordOccurances.values())
    plt.show()

@timer
def test():
    print("Hallo!")

if __name__ == "__main__":
    print("Hello!")
    lorem='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis viverra nec dolor et laoreet. Nullam euismod mi nisi. Aliquam tristique laoreet efficitur. Maecenas volutpat nibh quis tincidunt fringilla. Etiam suscipit elit tortor, dignissim varius massa euismod vitae. In molestie sem sed nunc eleifend, sollicitudin posuere metus dapibus. In quis lacus mauris. Suspendisse facilisis, odio nec ullamcorper porta, nisl risus efficitur mi, ut pulvinar lectus turpis at massa. Aliquam erat volutpat. Maecenas et quam scelerisque, molestie ipsum vel, finibus tellus. Donec interdum fringilla massa, in bibendum libero congue at. Nulla imperdiet mollis maximus. Ut vehicula iaculis turpis, a volutpat mi eleifend vitae. Nunc placerat ante sed lectus iaculis, sit amet eleifend felis pharetra.\
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis viverra nec dolor et laoreet. Nullam euismod mi nisi. Aliquam tristique laoreet efficitur. Maecenas volutpat nibh quis tincidunt fringilla. Etiam suscipit elit tortor, dignissim varius massa euismod vitae. In molestie sem sed nunc eleifend, sollicitudin posuere metus dapibus. In quis lacus mauris. Suspendisse facilisis, odio nec ullamcorper porta, nisl risus efficitur mi, ut pulvinar lectus turpis at massa. Aliquam erat volutpat. Maecenas et quam scelerisque, molestie ipsum vel, finibus tellus. Donec interdum fringilla massa, in bibendum libero congue at. Nulla imperdiet mollis maximus. Ut vehicula iaculis turpis, a volutpat mi eleifend vitae. Nunc placerat ante sed lectus iaculis, sit amet eleifend felis pharetra.\
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis viverra nec dolor et laoreet. Nullam euismod mi nisi. Aliquam tristique laoreet efficitur. Maecenas volutpat nibh quis tincidunt fringilla. Etiam suscipit elit tortor, dignissim varius massa euismod vitae. In molestie sem sed nunc eleifend, sollicitudin posuere metus dapibus. In quis lacus mauris. Suspendisse facilisis, odio nec ullamcorper porta, nisl risus efficitur mi, ut pulvinar lectus turpis at massa. Aliquam erat volutpat. Maecenas et quam scelerisque, molestie ipsum vel, finibus tellus. Donec interdum fringilla massa, in bibendum libero congue at. Nulla imperdiet mollis maximus. Ut vehicula iaculis turpis, a volutpat mi eleifend vitae. Nunc placerat ante sed lectus iaculis, sit amet eleifend felis pharetra.\
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis viverra nec dolor et laoreet. Nullam euismod mi nisi. Aliquam tristique laoreet efficitur. Maecenas volutpat nibh quis tincidunt fringilla. Etiam suscipit elit tortor, dignissim varius massa euismod vitae. In molestie sem sed nunc eleifend, sollicitudin posuere metus dapibus. In quis lacus mauris. Suspendisse facilisis, odio nec ullamcorper porta, nisl risus efficitur mi, ut pulvinar lectus turpis at massa. Aliquam erat volutpat. Maecenas et quam scelerisque, molestie ipsum vel, finibus tellus. Donec interdum fringilla massa, in bibendum libero congue at. Nulla imperdiet mollis maximus. Ut vehicula iaculis turpis, a volutpat mi eleifend vitae. Nunc placerat ante sed lectus iaculis, sit amet eleifend felis pharetra.\
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis viverra nec dolor et laoreet. Nullam euismod mi nisi. Aliquam tristique laoreet efficitur. Maecenas volutpat nibh quis tincidunt fringilla. Etiam suscipit elit tortor, dignissim varius massa euismod vitae. In molestie sem sed nunc eleifend, sollicitudin posuere metus dapibus. In quis lacus mauris. Suspendisse facilisis, odio nec ullamcorper porta, nisl risus efficitur mi, ut pulvinar lectus turpis at massa. Aliquam erat volutpat. Maecenas et quam scelerisque, molestie ipsum vel, finibus tellus. Donec interdum fringilla massa, in bibendum libero congue at. Nulla imperdiet mollis maximus. Ut vehicula iaculis turpis, a volutpat mi eleifend vitae. Nunc placerat ante sed lectus iaculis, sit amet eleifend felis pharetra.\
    '
    wordOcc = countOccurance(lorem)
    showOccurances = showOccurances(wordOcc)
