import json
import re
import os

def dicttojson(index,path):
    file = os.path.join(path,str(index)+'.txt')
    i = 1
    dndr = {}
    with open(file,'r') as f: 
        # list = line.split('\n')
        list = f.read().split('\n')
        # print(list)
        for i in range(0,len(list)-1):
            if i%2:
                key = str(i//2)
                value = list[i:i+2]
                dndr.update({key:value})
        # print(dndr)
    # ndr_dict = json.loads(dndr)
    filename = str(index)
    with open(os.path.join(path,filename+".json"),"w") as f:
        json.dump(dndr,f,indent=4,ensure_ascii=False)
    
    # {'1': {
    #                     "1":["drosten","REDEANTEIL"],
    #                     "2":["",],
    #                     "3":[]
    #                     }
    # }

    # ndr_dict['erster']