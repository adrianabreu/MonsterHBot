# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import requests
import re
import json
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.

f = open('/home/ubuntu/workspace/token.id', 'r')
TOKEN=f.read()
#TOKEN =  # Nuestro tokken del bot (el que @BotFather nos dió).
 
bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
 
def listener(messages):
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text': # Sólo saldrá en el log los mensajes tipo texto
            if cid > 0:
                mensaje = str(m.chat.first_name) + " [" + str(cid) + "]: " + m.text
            else:
                mensaje = str(m.from_user.first_name) + "[" + str(cid) + "]: " + m.text 
            f = open('log.txt', 'a')
            f.write(mensaje + "\n")
            f.close()
            print mensaje
            
bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
#############################################
#Funciones
def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

def format_string(string):
    a = string.split('\n')
    b = []
    result = ''
    print a
    for i in a:
        b.append(i.split(' ')[0])
    bigger=''
    for j in b:
        if len(j) > len(bigger):
            bigger = j
    for i in range(len(bigger)):
        result +='_'
        
    result += a[0]
    
    return result
    
@bot.message_handler(commands=['debilidades']) # Indicamos que lo siguiente va a controlar el comando '/roto2'.
def command_debilidades(m): # Definimos una función que resuelva lo que necesitemos.
    url = "http://kiranico.com/es/mh4u/monstruo/"
    #print str(m.text).split(' ')[1]
    ##Parse string
    a = len(str(m.text).split(' '))
    if a == 3:
       b = str(m.text).split(' ')
       for i in b:
           i=i.lower()
       del b[0]
       print b
       c = ('-').join(b)
       url += c
       req = requests.get(url)
       statusCode = req.status_code
    elif a == 2:
       url += str(m.text).split(' ')[1].lower()
       req = requests.get(url)
       statusCode = req.status_code
    else:
        statusCode=500
    #url += len(str(m.text).split(' ')[1]
    #url += str(m.text).split(' ')[1]
    # Realizamos la petición a la web
    
    
    # Comprobamos que la petición nos devuelve un Status Code = 200
    
    if statusCode == 200:
    
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
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
                result = "Fire | Ice | Thunder | Water | Dragon \n"
                for i in parts:
                    result += (i["local_name"] + " " + i["pivot"]["res_fire"] + " " + i["pivot"]["res_ice"] + " " + i["pivot"]["res_thunder"] + " " + i["pivot"]["res_water"] + " " + i["pivot"]["res_dragon"])
                    result += "\n"
        result = format_string(result)  
        #print "Items"
        #parts = j["monster"]["items"]
        #for i in parts:
        #    print i["local_name"] + "  Rango " + i["pivot"]["rank"]["local_name"] + " " + i["pivot"]["monsteritemmethod"]["local_name"] + " " + i["pivot"]["percentage"] + "%"
        #result = hp + ('\n') + fire + ('\n') + water + ('\n') + thunder + ('\n') + ice + ('\n') + dragon 
    else:
        print "Status Code %d" %statusCode
        result = "No he encontrado a ese monstruo :C"
    
    cid = m.chat.id
    bot.send_message(cid, result)
    
@bot.message_handler(commands=['recompensa']) # Indicamos que lo siguiente va a controlar el comando '/miramacho'
def command_recompensa(m): # Definimos una función que resuleva lo que necesitemos.
    url = "http://kiranico.com/es/mh4u/monstruo/"
    #print str(m.text).split(' ')[1]
    ##Parse string
    a = len(str(m.text).split(' '))
    if a == 3:
       b = str(m.text).split(' ')
       for i in b:
           i=i.lower()
       del b[0]
       print b
       c = ('-').join(b)
       url += c
       req = requests.get(url)
       statusCode = req.status_code
    elif a == 2:
       url += str(m.text).split(' ')[1].lower()
       req = requests.get(url)
       statusCode = req.status_code
    else:
        statusCode=500
    #url += len(str(m.text).split(' ')[1]
    #url += str(m.text).split(' ')[1]
    # Realizamos la petición a la web
    
    
    # Comprobamos que la petición nos devuelve un Status Code = 200
    
    if statusCode == 200:
    
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
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
                result = "RANGO BAJO\n"
                result2 = "RANGO ALTO\n"
                result3 = "RANGO G\n"
                parts = j["monster"]["items"]
                firstime = True
                jold=''
                for i in parts:
                    jnew = i["pivot"]["monsteritemmethod"]["local_name"]

                    if (i["pivot"]["rank"]["local_name"] == "Bajo"):
                        if (jnew != jold and not(firstime)):
                            result += "==================================================\n"
                        result += (i["local_name"] + " " + i["pivot"]["monsteritemmethod"]["local_name"] + " " + i["pivot"]["percentage"] + "%")
                        result += "\n"

                    elif (i["pivot"]["rank"]["local_name"] == "Alto"):
                        if (jnew != jold and not(firstime)):
                            result2 += "==================================================\n"
                        result2 += (i["local_name"]+ " " + i["pivot"]["monsteritemmethod"]["local_name"] + " " + i["pivot"]["percentage"] + "%")
                        result2 += "\n"
                    else:
                        if (jnew != jold and not(firstime)):
                            result3 += "==================================================\n"
                        result3 += (i["local_name"] + " " + i["pivot"]["monsteritemmethod"]["local_name"] + " " + i["pivot"]["percentage"] + "%")
                        result3 += "\n"
                    firstime=False
                    jold = i["pivot"]["monsteritemmethod"]["local_name"]
    else:
        print "Status Code %d" %statusCode
        result = "No he encontrado a ese monstruo :C"
    cid = m.chat.id
    bot.send_message(cid, result)
    bot.send_message(cid, result2)
    bot.send_message(cid, result3)
#############################################
#Peticiones
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.