import os
import json

PATH = os.path.join("data","REFINED","ndr")
COMBINEDPATH = os.path.join("data","COMBINED","ndr")

meta = []
with open(os.path.join(PATH,"meta.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)
meta.reverse()

# temp = os.listdir(PATH)
# files = []
# for filename in temp:
#     if filename.split(".")[-1] == "json":
#         files.append(filename)
# files = files[0:-1]

for i in range(len(meta)):
    newMeta = {"id":meta[i]['id'],"source":meta[i]['link'],"title":meta[i]['title']}
    if "date" in meta[i]:
        newMeta['date'] = meta[i]['date']
    else:
        newMeta['date'] = {"year":-1,"month":-1,"day":-1,"time":"00:00"}
    content = {}
    
    correspondingTextJSON = os.path.join(PATH,meta[i]['link'].split('/')[-1].split('.')[0][-3:]+'.json')
    
    
    with open(correspondingTextJSON,"r",encoding="utf-8") as f:
        content = json.load(f)
    speakers = []
    for entity in content.values():
        if entity[0] == "Info" or entity[0] == "Head":
            entity[0] = "None"
            continue
        speakers.append(entity[0])
    speakers = list(set(speakers))
    newMeta["speakers"] = speakers

    correspondingHeadlineJSON = os.path.join(PATH,'h'+meta[i]['link'].split('/')[-1].split('.')[0][-3:]+'.json')
    headlines = []
    with open(correspondingHeadlineJSON,"r",encoding="utf-8") as f:
        headlines = json.load(f)
        headlines = list(headlines.values())

    with open(os.path.join(COMBINEDPATH,str(newMeta['id'])+".json"),"w",encoding="utf-8") as f:
        returnDict = {"metadata":newMeta,"content":content,"headlines":headlines}
        print(returnDict)
        json.dump(returnDict,f,indent=4,ensure_ascii=False)
