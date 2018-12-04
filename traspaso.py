from bs4 import BeautifulSoup
import re
import os

import sqlite3

stopWords = ['&#3','reuter','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

from datetime import datetime
startTime = datetime.now()

csv = open("basedatos.csv","a")


dbsql = sqlite3.connect('basedatos.db')
c = dbsql.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS noticias(id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, descripcion TEXT);''')


listado = []

def guardar(titulo,cuerpo):
    #csv.write(titulo+","+cuerpo+"\n")
    listado.append((titulo,cuerpo))





def extraer_titulo_body(texto):

    hi = texto.find("<title>") + 7
    hf = texto.find("</title>")

    titulo = texto[hi:hf]

    bi = texto.find("<body>") + 6
    bf = texto.find("</body>")

    body = texto[bi:bf]

    if hf == -1 and hf == -1 :
        return "",""

    if bf == -1:
        return titulo,""


    titulo = titulo.replace(",","---").replace("\n"," ")


    body = body.replace("("," ").replace(")"," ").replace(";"," ").replace("\n"," ")
    body = body.replace(",", " ").replace("<", " ").replace(">", " ").replace("\""," ").replace("."," ").replace("/"," ")
    #body = re.sub('[^A-Za-z ]+','',body)

    #body = re.sub('\d', '', body)

    filtered_words = []

    for word in body.split():
        if word not in stopWords and word.isalpha():
            filtered_words.append(word)

    filtered_words_titulo = []

    for word in titulo.split():
        if word not in stopWords and word.isalpha():
            filtered_words_titulo.append(word)



    body =" ".join(str(x) for x in filtered_words)
    titulo =" ".join(str(x) for x in filtered_words_titulo)

    return titulo,body




def analizar2(ruta):
    print (ruta)
    file = open(ruta, mode="r", encoding="ISO-8859-1").read().lower().replace("&lt;","<").replace("\n"," ")#.replace(","," ").replace("<"," ").replace(">"," ")
    #file = file.replace(";"," ").replace("&#3"," ")

    contador = 0
    flag = 0
    while True:
        try:
            texto = file[flag:]

            ti = texto.index("<reuters") +7
            tf = texto.index("</reuters>")

            flag =  flag + tf + 9

            titulo, body = extraer_titulo_body(texto[ti:tf])
            guardar(titulo,body)
            contador = contador + 1

            #print ("Titulo: "+titulo+"\nBody: "+body[:150]+"\n")
        except Exception as e:
            print ("EEROR - " +str(e))
            break
    print ("Este archivo tiene "+str(contador)+" articulos")
    print(datetime.now() - startTime)
    print("\n")








def listar():
    directio_actual = os.path.join(os.getcwd(),"archivos")
    for file in os.listdir(directio_actual):
        if file.endswith(".sgm"):
            archivo = os.path.join(directio_actual ,file)
            analizar2(archivo)




listar()

c.executemany('''INSERT OR IGNORE INTO noticias(titulo, descripcion) VALUES(?,?)''', listado)
dbsql.commit()
print(datetime.now() - startTime)