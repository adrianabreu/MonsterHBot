# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import json

url = "http://kiranico.com/es/mh4u/monstruo/kirin"

# Realizamos la petición a la web
req = requests.get(url)

# Comprobamos que la petición nos devuelve un Status Code = 200
statusCode = req.status_code
if statusCode == 200:

    html = BeautifulSoup(req.text)

    # Obtenemos todos los divs donde estan las entradas
    script = html.find_all('script',{'class':''})

    # Recorremos todas las entradas para extraer el título, autor y fecha
    fire="Resistencia fuego: "
    water="Resistencia agua: "
    thunder="Resistencia trueno: "
    ice="Resistencia hielo: "
    dragon="Resistencia dragon: "
    for i,entradas in enumerate(script):
        if i == 5:
            #print entradas
            values = re.findall(r'var.*?=\s*(.*?);', str(entradas), re.DOTALL | re.MULTILINE)
            j = json.loads(values[0])
            parts = j["monster"]["monsterbodyparts"]
            print "Fire | Ice | Thunder | Water | Dragon"
            for i in parts:
                print i["local_name"] + " " + i["pivot"]["res_fire"] + " " + i["pivot"]["res_ice"] + " " + i["pivot"]["res_thunder"] + " " + i["pivot"]["res_water"] + " " + i["pivot"]["res_dragon"]
            
            print "Items"
            parts = j["monster"]["items"]
            for i in parts:
                print i["local_name"] + "  Rango " + i["pivot"]["rank"]["local_name"] + " " + i["pivot"]["monsteritemmethod"]["local_name"] + " " + i["pivot"]["percentage"] + "%"
else:
    print "Status Code %d" %statusCode
    result = "No he encontrado a ese monstruo :C"