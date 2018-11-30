from bs4 import BeautifulSoup
import re
import os

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


csv = open("basedatos.csv","a")


def guardar(titulo,cuerpo):
    csv.write(titulo+","+cuerpo+"\n")







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


    body = body.replace("reuter"," ").replace("("," ").replace(")"," ").replace(";"," ").replace("&#3"," ").replace("\n"," ")
    body = body.replace(",", " ").replace("<", " ").replace(">", " ").replace("\""," ").replace("."," ").replace("/"," ")
    #body = re.sub('[^A-Za-z ]+','',body)

    filtered_words = [word for word in body.split(" ") if word not in stopwords.words('english') and  word.isalpha()]

    filtered_words_titulo = [word for word in titulo.split(" ") if word not in stopwords.words('english') and word.isalpha()]

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








def listar():
    directio_actual = os.getcwd()
    for file in os.listdir(directio_actual ):
        if file.endswith("0.sgm"):
            archivo = os.path.join(directio_actual ,file)
            analizar2(archivo)
            break






listar()