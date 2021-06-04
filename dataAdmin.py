from dataCollector import data_collector
import pdftotext
import pdftotext_mdr 
import json
import os
from pathlib import Path

def safe_text_to_json(text:dict,folder:str,filename:str):
    path = os.path.join(os.path.join("data","refined"),folder)
    Path.mkdir(path,parents=True,exist_ok=True)
    with open(filename+".json", "w") as f:
        json.dump(text,f)



if __name__ == "__main__":
    data_collector()

    pdftotext.performRegEx()
    pdftotext_mdr.performRegEx()


