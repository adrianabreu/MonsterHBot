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


TOKEN = '172228506:AAFYIgQcOv06RuDfYDacE1PuB5M1_WFZphA' # Nuestro tokken del bot (el que @BotFather nos dió).
 
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
@bot.message_handler(commands=['debilidades']) # Indicamos que lo siguiente va a controlar el comando '/roto2'.
def command_debilidades(m): # Definimos una función que resuelva lo que necesitemos.
    url = "http://kiranico.com/es/mh4u/monstruo/"
    #print str(m.text).split(' ')[1]
    url += str(m.text).split(' ')[1]
    # Realizamos la petición a la web
    req = requests.get(url)
    
    # Comprobamos que la petición nos devuelve un Status Code = 200
    statusCode = req.status_code
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
                j=0
                for x in str(values).split(","):
                    if x.find("res_fire") != -1 and j < 20:
                        fire += x.split(':')[1].split('\"')[1]
                        fire += " "
                        j+=1
                    if x.find("res_thunder") != -1 and j < 20:
                        thunder += x.split(':')[1].split('\"')[1]
                        thunder += " "
                        j+=1
                    if x.find("res_water") != -1 and j < 20:
                        water += x.split(':')[1].split('\"')[1]
                        water += " "
                        j+=1
                    if x.find("res_ice") != -1 and j < 20:
                        ice += x.split(':')[1].split('\"')[1]
                        ice += " "
                        j+=1
                    if x.find("res_dragon") != -1 and j < 20:
                        dragon += x.split(':')[1].split('\"')[1]
                        dragon += " "
                        j+=1
                
        hp = "HP " + str(values).split(',')[1].split(':')[1]
        print hp
        print fire
        print thunder
        print water
        print ice
        print dragon
        result = hp + ('\n') + fire + ('\n') + water + ('\n') + thunder + ('\n') + ice + ('\n') + dragon 
    else:
        print "Status Code %d" %statusCode
        result = "No he encontrado a ese monstruo :C"
    cid = m.chat.id
    bot.send_message(cid, result)
    
@bot.message_handler(commands=['recompensa']) # Indicamos que lo siguiente va a controlar el comando '/miramacho'
def command_recompensa(m): # Definimos una función que resuleva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    bot.send_message( cid, 'Aun no esta, paciencia') # Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.
#############################################
#Peticiones
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.