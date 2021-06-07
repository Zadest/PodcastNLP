import json
import re
import os

def dicttojson(file):
    f = ''
    i = 1
    for line in txt:
        key= line.strip()
    # d_ndr.update({key})
        print(i,key)
        i=i+1


    
    # cleanText = delimiters
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