# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import requests
import re
import json
from telegram import Updater
from operator import itemgetter

'''
def listener(messages):
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            if cid > 0:
                mensaje = str(m.chat.first_name) + " [" + str(cid) + "]: " + m.text
            else:
                mensaje = str(m.from_user.first_name) + "[" + str(cid) + "]: " + m.text 
            f = open('log.txt', 'a')
            f.write(mensaje + "\n")
            f.close()
            print mensaje
'''            
#############################################
#Funciones 
    
def findallweakness (j):
    parts = j["monster"]["monsterbodyparts"]
    result = "Fire | Ice | Thunder | Water | Dragon \n"
    for i in parts:
        result += (i["local_name"] + " " + i["pivot"]["res_fire"] + " " + i["pivot"]["res_ice"] + " " + i["pivot"]["res_thunder"] + " " + i["pivot"]["res_water"] + " " + i["pivot"]["res_dragon"])
        result += "\n"    
    return result

def findhighweakness (j):

    parts = j["monster"]["monsterbodyparts"]
    result = ""
    a={'Fire':0,'Ice':0,'Thunder':0,'Water':0,'Dragon':0}
    usedparts=[]
    
    for i in parts:
        if (int(i["pivot"]["monsterbodypart_id"])) not in usedparts:
            a['Fire']+=int(i["pivot"]["res_fire"])
            a['Ice']+=int(i["pivot"]["res_ice"])
            a['Thunder']+=int(i["pivot"]["res_thunder"])
            a['Water']+=int(i["pivot"]["res_water"])
            a['Dragon']+=int(i["pivot"]["res_dragon"])
            usedparts.append(int(i["pivot"]["monsterbodypart_id"]))
    sortdict = sorted(a.items(), key=itemgetter(1),reverse=True)

    for w in sortdict:
        result += (str(w).split('\'')[1] + ' (' + str(w).split('\'')[2].split(' ')[1] + ' \n' )
    
    result += '\n'
    
    return result
    
    
def debilidades(bot, update): # Definimos una función que resuelva lo que necesitemos.
    m = update.message
    url = "http://kiranico.com/es/mh4u/monstruo/"
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


    
    if statusCode == 200:

        html = BeautifulSoup(req.text, "lxml")

        script = html.find_all('script',{'class':''})
    
        for i,entradas in enumerate(script):
            if i == 5:
                #print entradas
                values = re.findall(r'var.*?=\s*(.*?);', str(entradas), re.DOTALL | re.MULTILINE)
                j = json.loads(values[0])
                
                #Until md is not implemented we will conform with 
                result = findhighweakness(j)

    else:
        print "Status Code %d" %statusCode
        if statusCode == 502 or statusCode == 404:
            result= "Se ha caido la web"
        else:
            result = "No he encontrado a ese monstruo :C"
    
    cid = m.chat.id
    bot.sendMessage(cid, result)
    
def recompensa(bot, update): # Definimos una función que resuelva lo que necesitemos.
    m = update.message
    url = "http://kiranico.com/es/mh4u/monstruo/"

    ## Buscamos al monstruo 
    
    a = len(str(m.text).split(' '))
    b = str(m.text).split(' ')
    rango = b[-1].lower()
    print b
    print rango
    if  rango == 'alto' or rango == 'bajo' or rango == 'g':
        del b[-1]
    
    if len(b) == 3:
       for i in b:
           i=i.lower()
       del b[0]
       print b
       c = ('-').join(b)
       url += c
       req = requests.get(url)
       statusCode = req.status_code
       print url
    elif len(b) == 2:
       url += str(m.text).split(' ')[1].lower()
       req = requests.get(url)
       statusCode = req.status_code
       print url
    else:
        statusCode=500
    #url += len(str(m.text).split(' ')[1]
    #url += str(m.text).split(' ')[1]
    # Realizamos la petición a la web
    
    
    # Comprobamos que la petición nos devuelve un Status Code = 200, es decir, pagina ok
    result=''
    result2=''
    result3=''
    if statusCode == 200:
    
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "lxml")
    
        # Buscamos todos los tags de script en la pagina de kiranico
        script = html.find_all('script',{'class':''})
    
    
        #El numero 5 tiene el contenido en json
        for i,entradas in enumerate(script):
            if i == 5:
                #Extraemos con esta regexp la variable json y la parseamos
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

        cid = m.chat.id
        if rango == 'bajo':
            bot.sendMessage(cid, result)
        elif rango == 'alto':
            bot.sendMessage(cid, result2)
        elif rango == 'g':
            bot.sendMessage(cid, result3)
        else:
            if(result2=='' and result3==''):
                bot.sendMessage(cid, result)
            else:
                bot.sendMessage(cid, result)
                bot.sendMessage(cid, result2)
                bot.sendMessage(cid, result3)
    else:
        print "Status Code %d" %statusCode
        result = "No he encontrado a ese monstruo :C"
        cid = m.chat.id
        bot.sendMessage(cid, result)
#############################################
def main():
    f = open('/home/ubuntu/workspace/token.id', 'r')
    TOKEN=f.read()
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("debilidades", debilidades)
    dp.addTelegramCommandHandler("recompensa", recompensa)

    # Start the Bot
    updater.start_polling(timeout=5)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()