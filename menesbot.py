#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import oauth2
import urllib.parse
import pytumblr
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram.ext import Job

arqTokens = open('menesbot.token','r')
token = arqTokens.readlines()

for i in range(0,4):
    token[i] = token[i].strip('\n')

arqTokens.close()

updater = Updater(token=token[0])
dispatcher = updater.dispatcher                                    

client = pytumblr.TumblrRestClient(
  token[1],
  token[2],
  token[3],
  token[4]
)
                                    
j = updater.job_queue


arqUltimo = open('ultimo.txt','r')
ultimo = arqUltimo.read()
arqUltimo.close()
arqUltimos = open('ultimos.txt','w')
messages = client.posts('sitedosmenes')
for i in range(0,20):
    texto = messages["posts"][i]["caption"]
    texto = re.sub('<[^<]+?>', '', texto)
    texto = re.sub('[\r\n]', ' ', texto)
    texto += '\n'
    texto += messages["posts"][i]["photos"][0]["original_size"]["url"]
    texto += '\n'
    arqUltimos.write(texto)
arqUltimos.close()
arqUltimos = open('ultimos.txt','r')
ultimos = arqUltimos.readlines()
for i in range(0,len(ultimos)):
    ultimos[i] = ultimos[i].strip('\n')
arqUltimos.close()

def start(bot, update):      
    bot.sendMessage(chat_id=update.message.chat_id, text="Este é o bot dos menes, criado por @Arquimago para distribuir os menes automaticamente pelo @CanalDosMenes")


start_handler = CommandHandler('start', start)                   
dispatcher.add_handler(start_handler)                                                              

def getmene(bot, update):      
    global ultimos
    texto = ultimos[0]
    imagem = ultimos[1]
    if len(texto) < 200:
        bot.send_photo(chat_id=update.message.chat_id, photo=imagem, caption=texto)
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo=imagem)
        bot.sendMessage(chat_id=update.message.chat_id, text=texto)

getmene_handler = CommandHandler('getmene', getmene)                   
dispatcher.add_handler(getmene_handler)

def getultimo(bot,update):
    nome=update.message.from_user.username
    global ultimo
    if nome=="Arquimago":
        messages = client.posts('sitedosmenes')
        texto = "o atual no servidor é "+ultimo+" e o atual no site é "+ messages["posts"][0]["short_url"]
        bot.sendMessage(chat_id=update.message.chat_id, text = texto)

getultimo_handler = CommandHandler('getultimo', getultimo)
dispatcher.add_handler(getultimo_handler)

def confere_menes(bot, job):
    messages = client.posts('sitedosmenes')
    global ultimo
    global ultimos
    hora = time.strftime("%c")
    if ultimo == messages["posts"][0]["short_url"]:
        print("%s teste executado e não teve atualização" % hora)
    else:
        ultimo = messages["posts"][0]["short_url"]
        arqUltimo = open('ultimo.txt','w')
        arqUltimo.write(ultimo)
        arqUltimo.close()
        arqUltimos = open('ultimos.txt', 'w')
        for i in range(0,20):
            texto = messages["posts"][i]["caption"]
            texto = re.sub('<[^<]+?>', '', texto)
            texto += '\n'
            texto += messages["posts"][i]["photos"][0]["original_size"]["url"]
            texto += '\n'
            arqUltimos.write(texto)
        arqUltimos.close()
        arqUltimos = open('ultimos.txt','r')
        ultimos = arqUltimos.readlines()
        for i in range(0,len(ultimos)):
            ultimos[i] = ultimos[i].strip('\n')
        arqUltimos.close()
        texto = messages["posts"][0]["caption"]                                                                              
        texto = re.sub('<[^<]+?>', '', texto)
        imagem = messages["posts"][0]["photos"][0]["original_size"]["url"]                                                         
        if len(texto) < 200:
            bot.send_photo(chat_id="@canaldosmenes",photo=imagem,caption=texto)
        else:
            bot.send_photo(chat_id="@canaldosmenes",photo=imagem)
            bot.sendMessage(chat_id="@canaldosmenes",text=texto)
        print("%s Canal tem novo mene!" % hora)

job_confere_menes = Job(confere_menes, 60.0)
j.put(job_confere_menes, next_t=0.0)

updater.start_polling()