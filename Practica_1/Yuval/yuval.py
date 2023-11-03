import pandas as pd
import csv
import hashlib
import time

def cargarCSV(ficherito):
    textoCargado = []
    with open(ficherito, newline='') as csvfile:
        texto = csv.reader(csvfile, delimiter=';')

        for row in texto:
            textoCargado.append(row)
    
    return textoCargado

def convertToBin(numero, tam):
    binario = bin(numero)[2:]
    binario = binario.zfill(tam)
    binario = binario.ljust(32, "0")
    binarioFinal = bin(int(binario,2))[2:].zfill(len(binario))
    return binario

def cargarTexto(csvTexto, binIt):
    texto = " "
    it = 0
    for x in binIt:
        #print(x)
        texto = texto + csvTexto[it][int(x)]
        it=it+1 
    return texto

def generarTextosIlicitos(ilicitoCSV, tam, num):
    textNum = pow(2,num)
    ilicitoDic = {}
    for i in range(0,textNum):
        binIt = convertToBin(i, num)
        textoIlicito = cargarTexto(ilicitoCSV, binIt)
        #print(textoLicito)
        #print(" ")
        huella = hash_variable_length(textoIlicito, tam)
        #print(huella)
        #print(" ")
        ilicitoDic[huella] = binIt
    
    return ilicitoDic


def hash_variable_length(data, length_digit):
    # Utiliza SHA-256 para calcular el hash de los datos
    md5_hash = hashlib.md5(data.encode()).hexdigest()

    # Trunca el hash al número de bytes especificado
    truncated_hash = md5_hash[:length_digit]

    return truncated_hash

def comparar(licitoCSV, ilicitoCSV, tam, num):
    startTime = time.perf_counter()
    #Si num mayor de 25 funcion recursiva
    listaIlicitos = generarTextosIlicitos (ilicitoCSV, tam, num)
    print("Textos Ilicitos Generados: " + str(num))
    dicNum = len(listaIlicitos)
    cantidad = 0
    textNum = pow(2,num)
    resultados = [0,0,0,0.0]
    tiempo = 0.0
    for x in range(0,textNum): #recorre textos licitos
        binDic = convertToBin(x, num)
        textoLicito = cargarTexto(licitoCSV, binDic)
        huella = hash_variable_length(textoLicito,tam)
        del textoLicito
        if huella in listaIlicitos:
            endTime = time.perf_counter()
            tiempo = endTime-startTime
            resultados=[num, binDic, listaIlicitos[huella],tiempo]
            print("Hay coincidencia: Licito: " + binDic + " e Ilicito: " + listaIlicitos[huella] + " con hash: " + huella + " en tiempo: " + str(tiempo))
            break
    del listaIlicitos
    return resultados

def doMedia(resultados, div):
    suma = 0.0
    for x in range(0, div):
        suma = suma + resultados[x][3]
    media = suma/div
    return media

def main(): 
    num = 20
    resultadosList=[]
    tituloLicito = "licito.csv" 
    licitoCSV = cargarCSV(tituloLicito)

    for x in range(6,13):
        resultados = []
        print("Pruebas para Hash: " + str(x))

        resultadosList.append(['-------- Resultados para Hash: ' + str(x*4) + ' --------'])
        resultadosList.append(["Tamanio Texto", "Licito", "Ilicito", "Tiempo"])

        for y in range(1,16):
            print("Texto " + str(y)) 
            tituloIlicito = "ilicito" + str(y) + ".csv" 
            ilicitoCSV = cargarCSV(tituloIlicito)
            encontrado = False
            num = x*2
            while not encontrado and num < 33:
                resultado = comparar(licitoCSV,ilicitoCSV,x,num)
                if resultado[3] != 0.0:
                    resultados.append(resultado)
                    #print(resultado)
                    resultadosList.append(resultado)
                    encontrado = True
                num = num + 1
            del ilicitoCSV
        mediacinco = doMedia(resultados, 5)
        media = doMedia(resultados, len(resultados))

        print("La media es: " + str(media))
        
        resultadosList.append(["La media para 5 es de: " + str(mediacinco)])
        resultadosList.append(["La media total es de: " + str(media)])
        resultadosList.append(" ")
        outputYuval = 'outputPrueba.csv'
        with open(outputYuval, 'w', newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerows(resultadosList)

main()

