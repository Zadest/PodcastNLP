import requests as r
import os

url = 'https://api.corona-zahlen.org/germany/history'
curl = url + '/cases'
iurl = url + '/incidence'
durl = url + '/deaths'
rurl = url + '/recovered'

cases = r.get(curl)
incidence = r.get(iurl)
deaths = r.get(durl)
recovered = r.get(rurl)

print(cases)