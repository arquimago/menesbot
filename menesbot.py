#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

ultimo = "https://tmblr.co/ZoQwWu2LUhN2S"

def start(bot, update):      
    bot.sendMessage(chat_id=update.message.chat_id, text="Este é o bot dos menes")


start_handler = CommandHandler('start', start)                   
dispatcher.add_handler(start_handler)                                                              

def getmene(bot, update):      
    messages = client.posts('sitedosmenes')
    texto = messages["posts"][0]["summary"]
    imagem = messages["posts"][0]["photos"][0]["original_size"]["url"]
    bot.send_photo(chat_id=update.message.chat_id, photo=imagem, caption=texto)

getmene_handler = CommandHandler('getmene', getmene)                   
dispatcher.add_handler(getmene_handler)

def mande(bot, update, args):
    nome=update.message.from_user.username
    postagem = ' '.join(args)
    if nome=="Arquimago":
        print("olá meu mestre")
        messages = client.posts('sitedosmenes')
        texto = messages["posts"][postagem]["summary"]
        imagem = messages["posts"][postagem]["photos"][0]["original_size"]["url"]
        bot.send_photo(chat_id="@canaldosmenes",photo=imagem,caption=texto)
        bot.sendMessage(chat_id=update.message.chat_id, text= "novo mene enviado")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text = "usuario não autorizado!")
        texto = nome + " tentou usar o bot indevidamente"
        print(texto)
		
mande_handler = CommandHandler('mande', mande)                   
dispatcher.add_handler(mande_handler)

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
    hora = time.strftime("%c")
    if ultimo == messages["posts"][0]["short_url"]:
        print("%s teste executado e não teve atualização" % hora)
    else:
        ultimo = messages["posts"][0]["short_url"]                                                                                 
        texto = messages["posts"][0]["summary"]                                                                                    
        imagem = messages["posts"][0]["photos"][0]["original_size"]["url"]                                                         
        bot.send_photo(chat_id="@canaldosmenes",photo=imagem,caption=texto)                                                        
        print("%s Canal tem novo mene!" % hora)

job_minute = Job(confere_menes, 60.0)
j.put(job_minute, next_t=0.0)

updater.start_polling()
