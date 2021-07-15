import requests as r
import matplotlib.pyplot as plt
import json
from datetime import datetime


URL = "https://api.corona-zahlen.org/germany/history/"

result = r.get(URL+"cases")
#print(json.loads(result.content)["data"][0])
cases = [data["cases"] for data in json.loads(result.content)["data"]]
dates = [data["date"] for data in json.loads(result.content)["data"]]
datesTicks = dates[::7]
datesTicks.append(dates[-1])


fig, axs = plt.subplots(1,2,figsize=(24,6),sharex='col', sharey='none')

result = r.get(URL+"deaths")

deaths = [data["deaths"] for data in json.loads(result.content)["data"]]
dates = [data["date"] for data in json.loads(result.content)["data"]]

plt.xticks(list(range(len(dates))[::7]).append(len(dates)),datesTicks,rotation=90)
#fig.autofmt_xdate()
axs[0].plot(cases,color="orange",label="Cases")
axs[0].set_title("cases")

axs[1].plot(deaths,label="Deaths")
axs[1].set_title("deaths")

plt.show()