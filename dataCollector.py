#! /usr/bin/env python3.9
# -*- coding : utf8 -*-

import os
import requests

result = requests.get("https://www.mdr.de/nachrichten/podcast/kekule-corona/kekule-corona-kompass-einhundertneunundsiebzig-100-downloadFile.pdf")

with open("data/kekule/179.pdf","wb") as f:
    f.write(result.content)


