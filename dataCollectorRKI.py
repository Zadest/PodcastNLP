from genericpath import exists
import requests as r
import os
from pathlib import Path # todo neuen folder wenn nicht exists: Path.mkdir(path,parents=True,exist_ok=True)


def dcrki(): 
    path = os.path.join('data','DASH')
    url = 'https://api.corona-zahlen.org'
    ghist = '/germany/history'
    vacc = '/vaccinations/history'
    curl = url + ghist + '/cases'
    iurl = url + '/incidence'
    durl = url + '/deaths'
    rurl = url + '/recovered'
    vurl = url + vacc

    cases = r.get(curl)
    incidence = r.get(iurl) # Vergleich
    deaths = r.get(durl) # Vergleich
    recovered = r.get(rurl)
    vaccinations = r.get(vurl) # Vergleich

    print(cases.content.decode('utf-8'))
    print(incidence.content.decode('utf-8'))
    print(deaths.content.decode('utf-8'))
    print(recovered.content.decode('utf-8'))
    print(vaccinations.content.decode('utf-8'))

    Path.mkdir(path,parents=True,exist_ok=True)
    with open(os.path.join(path,'cases_hist.json'),'w',encoding='utf-8') as f:
        f.write(cases.content.decode('utf-8'))
        print(cases.content.decode('utf-8'))
    with open(os.path.join(path,'incidence_hist.json'),'w',encoding='utf-8') as f:
        f.write(incidence.content.decode('utf-8'))
        print(incidence.content.decode('utf-8'))
    with open(os.path.join(path,'deaths_hist.json'),'w',encoding='utf-8') as f:
        f.write(deaths.content.decode('utf-8'))
        print(deaths.content.decode('utf-8'))
    with open(os.path.join(path,'recovered_hist.json'),'w',encoding='utf-8') as f:
        f.write(recovered.content.decode('utf-8'))
        print(recovered.content.decode('utf-8'))
    with open(os.path.join(path,'vaccinations_hist.json'),'w',encoding='utf-8') as f:
        f.write(vaccinations.content.decode('utf-8'))
        print(vaccinations.content.decode('utf-8'))

dcrki()