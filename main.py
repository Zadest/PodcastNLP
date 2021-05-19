#! /usr/bin/env python3
# -*- coding: utf8 -*-

import os
import matplotlib.pyplot as plt
import nltk

from decorators import timer

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


@timer
def countOccurance(text):
    if type(text) == str:
       text = text.split(' ')
       text = text.split('.')
       text = text.split(',')
    wordOccurances = {}
    ps = PorterStemmer()
    for token in text:
        rootWord = ps.stem(token)
        print(rootWord)
        if rootWord in wordOccurances:
            wordOccurances[rootWord] += 1
            continue
        wordOccurances[rootWord] = 1
    return wordOccurances

@timer
def showOccurances(wordOccurances):
    wordOccurancesSorted = dict(sorted(wordOccurances.items(), key=lambda item: item[1], reverse=True))
    plt.bar(wordOccurancesSorted.keys(),wordOccurancesSorted.values())
    plt.xticks(rotation=90)
    plt.show()

@timer
def test():
    print("Hallo!")

@timer
def loadData():
    with open('data/wikisent2.txt','r') as f:
        text = ' '.join(f.readlines())
    return text

if __name__ == "__main__":
    print("Hello!")
    
    englishBlindText = 'The pope (Latin: papa, from Greek: πάππας, romanized: pappas,[2] "father"),[3] also known as the supreme pontiff (Pontifex maximus) or the Roman pontiff (Romanus Pontifex), is the bishop of Rome, head of the worldwide Catholic Church and head of state or sovereign of the Vatican City State.[4] According to Catholics, the primacy of the bishop of Rome is largely derived from his role as the apostolic successor to Saint Peter, to whom primacy was conferred by Jesus, giving him the Keys of Heaven and the powers of "binding and loosing", naming him as the "rock" upon which the church would be built. The current pope is Francis, who was elected on 13 March 2013.[5]\
While his office is called the papacy, the jurisdiction of the episcopal see is called the Holy See.[6] It is the Holy See that is the sovereign entity by international law headquartered in the distinctively independent Vatican City State, a city-state enclaved within Rome, established by the Lateran Treaty in 1929 between Italy and the Holy See to ensure its temporal and spiritual independence. The Holy See is recognized by its adherence at various levels to international organization and by means of its diplomatic relations and political accords with many independent states.\
According to Catholic tradition, the apostolic see[7] of Rome was founded by Saint Peter and Saint Paul in the 1st century. The papacy is one of the most enduring institutions in the world and has had a prominent part in world history.[8] In ancient times the popes helped spread Christianity, and intervened to find resolutions in various doctrinal disputes.[9] In the Middle Ages, they played a role of secular importance in Western Europe, often acting as arbitrators between Christian monarchs.[10][11][12] Currently, in addition to the expansion of the Christian faith and doctrine, the popes are involved in ecumenism and interfaith dialogue, charitable work, and the defense of human rights.[13][14]\
In some periods of history, the papacy, which originally had no temporal powers, accrued wide secular powers rivaling those of temporal rulers. However, in recent centuries the temporal authority of the papacy has declined and the office is now almost exclusively focused on religious matters.[9] By contrast, papal claims of spiritual authority have been increasingly firmly expressed over time, culminating in 1870 with the proclamation of the dogma of papal infallibility for rare occasions when the pope speaks ex cathedra—literally "from the chair (of Saint Peter)"—to issue a formal definition of faith or morals.[9] Still, the pope is considered one of the world\'s most powerful people because of his extensive diplomatic, cultural, and spiritual influence on 1.3 billion Catholics and beyond,[15][16][17] and because he heads the world\'s largest non-government provider of education and health care,[18] with a vast network of charities.\
'

    lorem='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ornare fermentum venenatis. Cras rutrum turpis et aliquam tincidunt. Donec sollicitudin nulla non nisi sollicitudin, nec tempor dui interdum. Quisque orci massa, aliquet a tortor quis, fringilla feugiat libero. Praesent placerat est sed ante aliquet, et mollis eros viverra. Nulla facilisi. Aliquam placerat euismod magna, at lacinia metus laoreet sed.\
    Nam a ligula efficitur diam rhoncus rutrum. Proin ultrices fringilla nibh, nec efficitur nulla iaculis nec. Vestibulum nec ipsum molestie, condimentum turpis at, lacinia tortor. Nam tempor euismod sem sit amet rutrum. Praesent congue sed enim vitae molestie. Aenean nec tortor sit amet elit viverra tincidunt. Nam a tempus metus.\
    Suspendisse ac nulla hendrerit, dictum nisl ut, dapibus odio. Sed vel nibh eget metus finibus varius ut ut augue. Cras finibus dictum massa vitae eleifend. Duis a mauris ullamcorper, finibus augue ac, pellentesque magna. Nullam fermentum ligula dignissim nisi dapibus pellentesque. Nulla condimentum lacus sed facilisis faucibus. In hac habitasse platea dictumst. Nulla condimentum nibh ut tempus vulputate. Pellentesque lacinia, felis vitae ullamcorper finibus, mi tortor elementum ex, vitae cursus nisl lectus et nisi. Aliquam a eleifend purus. Cras quis diam lacus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Maecenas eu dictum massa, at suscipit velit. Aenean non nisi hendrerit, tempus est vel, auctor nunc. Integer feugiat elementum interdum. Aliquam tristique finibus eleifend.\
    Nullam vitae mauris pellentesque, pellentesque magna nec, varius mi. Nulla vel nisi eu nulla feugiat vulputate. Maecenas nec elit ex. Sed consectetur ornare mi et tempor. Sed congue ipsum a elit finibus efficitur. Proin lorem diam, pellentesque eget enim et, porta placerat diam. Vivamus imperdiet dapibus nunc, nec malesuada nisl ultrices vel. Nulla consequat felis mauris, et rutrum nulla ullamcorper id. Vestibulum eu lectus quis quam ullamcorper vehicula non vitae libero. Donec a pretium nunc, eget scelerisque justo. Quisque euismod faucibus tortor ac lobortis. Suspendisse dapibus neque in urna laoreet dapibus.\
    Pellentesque dictum felis pellentesque cursus eleifend. Suspendisse ut elit at lorem tempus cursus fermentum sit amet felis. Aenean accumsan semper nisi eu finibus. Proin aliquam, nisl ac luctus molestie, velit quam pharetra eros, et hendrerit magna purus ac libero. Donec elit metus, finibus sit amet nisi in, rutrum pharetra ipsum. Quisque vel malesuada neque, eu tempus sem. Pellentesque iaculis lectus ac mauris lacinia, sed rutrum erat tristique. Vestibulum condimentum, magna eget feugiat gravida, neque ex ornare lacus, sed pretium augue arcu at enim. Integer molestie viverra enim in placerat. Aenean purus nisi, efficitur a risus accumsan, dapibus mollis urna.'
    
    #text = loadData()
    print(len(lorem))
    wordOcc = countOccurance(lorem)
    showOccurances = showOccurances(wordOcc)
    print(wordOcc)
