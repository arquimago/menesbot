#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import oauth2
import urllib.parse
import pytumblr
import html
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
	texto = html.unescape(texto)
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

def git(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="O código deste bot se encontra em http://github.com/arquimago/menesbot")

git_handler = CommandHandler('git', git)
dispatcher.add_handler(git_handler)

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
		novo_mene = time.strftime("%c") + " Atualizado sem novos menes\n"
		arqLog = open('atividades.log','a')
		arqLog.write(novo_mene)
		arqLog.close()
	else:
		#Guarda o indice da ultima enviada
		indice = 20
		for i in range(0,20):
			if ultimo == messages["posts"][i]["short_url"]:
				indice = i
				break
		indice-=1
		#guarda o ultimo mene enviado
		ultimo = messages["posts"][0]["short_url"]
		arqUltimo = open('ultimo.txt','w')
		arqUltimo.write(ultimo)
		arqUltimo.close()
		arqUltimos = open('ultimos.txt', 'w')
		#Prepara arquivo de ultimos 20 menes
		for i in range(0,20):
			texto = messages["posts"][i]["caption"]
			texto = re.sub('<[^<]+?>', '', texto)
			texto += '\n'
			texto += messages["posts"][i]["photos"][0]["original_size"]["url"]
			texto += '\n'
			texto = html.unescape(texto)
			arqUltimos.write(texto)
		arqUltimos.close()
		arqUltimos = open('ultimos.txt','r')
		ultimos = arqUltimos.readlines()
		for i in range(0,len(ultimos)):
			ultimos[i] = ultimos[i].strip('\n')
		arqUltimos.close()
		#Arquivo ajustado
		
		#Posta menes faltantes
		for i in range(indice,-1,-1):
			texto = messages["posts"][i]["caption"]
			texto = re.sub('<[^<]+?>', '', texto)
			texto = html.unescape(texto)
			imagem = messages["posts"][i]["photos"][0]["original_size"]["url"]
			if len(texto) < 200:
				bot.send_photo(chat_id="@canaldosmenes",photo=imagem,caption=texto)
			else:
				bot.send_photo(chat_id="@canaldosmenes",photo=imagem)
				bot.sendMessage(chat_id="@canaldosmenes",text=texto)
		novo_mene = time.strftime("%c") + " Canal tem" + str(indice+1)+ " novo(s) mene(s)\n"
		arqLog = open('atividades.log','a')
		arqLog.write(novo_mene)
		arqLog.close()
		
j.run_repeating(confere_menes, 120.0, first=0)

updater.start_polling()
