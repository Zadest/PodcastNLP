import json
import re
import os

def dicttojson(file):
    i = 1
    dndr = {}
    speaker = []
    text = []
    for line in open(file):
        list = line.split(':')
        print(list)
        # speaker = speaker.append(list[0])
        # text = text.append(list[1])
        # print(speaker,text)
        i=i+1
        # dndr.update(list)
        # print(dndr)
    
    # ndr_dict = json.loads(cleanText)
    
    # {'1': {
    #                     "1":["drosten","REDEANTEIL"],
    #                     "2":["",],
    #                     "3":[]
    #                     }
    # }

    # ndr_dict['erster']
    # filename = 'lol'
    # with open(filename+".json","w") as f:
    #     json.dump(ndr_dict,f)