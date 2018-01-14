import json
import time
from datetime import datetime
import pymongo
from pymongo import MongoClient
import hashlib

#CONEXÃO COM O BANCO
cliente = MongoClient('localhost', 27017)
db = cliente.teste
collection = db.Encurtador

url_p = 'http://shortener/u/'
dt = str(datetime.now())

tempo = time.clock()
tempof = time.clock() - tempo

#FUNÇÃO QUE GERA UM ALIAS ALEATORIO AUTOMATICAMENTE A PARTIR DE UM CÓDIGO HASH
def random_key(dt):

    h = hashlib.sha1()
    h.update(bytes(dt, encoding='ascii'))
    aux = str(h.hexdigest())
    return aux[6:13]

print('============BEM-VINDO AO ENCURTADOR DE URL ==============')

ret = int(input('Deseja acessar o ShortenURL ou RetrieveURL? (1 - ShortenURL // 0 - RetrieveURL\n)'))

if ret == 1:

    dec = int(input('Deseja customizar a URL? (1 - Sim // 0 - Não)\n '))
    url = str(input('Digite a URL desejada.\n'))


    if dec == 1:
        c_alias = str(input('Digite o Alias desejado.'))
        encode = url_p + c_alias

        # VERIFICA SE O ALIAS DIGITADO JÁ EXISTE NO BANCO
        verifica = bool(collection.find_one({"alias": {'$in': [c_alias]}}))

        while verifica == True:
            print('Alias: %s \nERR_CODE: 001\nDescription: CUSTOM ALIAS ALREADY EXIST\n', c_alias)
            c_alias = str(input('Digite outro CUSTOM ALIAS.\n'))
            verifica = bool(collection.find_one({'alias': {'$in': [c_alias]}}))
            encode = url_p + c_alias
    else:
        c_alias = random_key(dt)
        encode = url_p + c_alias

    # INSERINDO NO BANCO DE DADOS
    collection.insert_one({"url": url,
                           "alias": c_alias,
                           "encode": encode,
                           "Tempo": tempof})
    # EXIBINDO RESULTADO DA INSERÇÃO.
    print('URL Original: %s \nURL Encurtada: %s \nTempo de Operação: %f' % (url, str(encode), tempof))

else:
    url = str(input('Digite a URL a ser acessada.'))
    # VERIFICA SE O ALIAS DIGITADO JÁ EXISTE NO BANCO
    verifica = bool(collection.find_one({"url": {'$in': [url]}}))
    if verifica == False:
        print('ERR_CODE: 002\n Description: SHORTENED URL NOT FOUND')
    else:
        for b in collection.find({"url":url}):
            print(b)