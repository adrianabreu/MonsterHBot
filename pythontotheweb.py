# -*- coding: utf-8 -*-
import urllib2,unicodedata
from bs4 import BeautifulSoup
 
#método de análisis de una dirección web
def analisisDescarga(archivo,conexion):
    html = conexion.read()
    soup = BeautifulSoup(html)
    #obtenemos una lista de String con la condición de atributos class con valores details y price
    links = soup.find_all(True, {'class':['details','price']})
    #la lista alterna valores de nombre de producto y precio
    #   creamos una bandera para diferenciar si es valor o producto
    precio = False
    for tag in links:
        print("--")
        for linea in tag:
            linea = linea.strip();
            #adaptamos unicode a utf-8
            normalizado=unicodedata.normalize('NFKD', linea).encode('ascii','ignore')
 
            if len(normalizado)>1:
                if precio:
                    print('precio: '+normalizado)
                    precio= not precio
                    archivo.write(normalizado+'\n')
                else:
                    print('producto: '+normalizado)
                    precio = not precio
                    archivo.write(normalizado+'\t')
#este método se conectará con la web y establece un timeout que obliga a reintentar el fallo
def preparar(archivo,web,x):
    try:
        print(web)
        conector = urllib2.urlopen(web,timeout=10)#timeout de 10 segundos
        analisisDescarga(archivo,conector)
    except:
        print("Tiempo de espera agotado, volviendo a intentar")
        preparar(archivo,web,x)
 
#Programa principal
print('Comienza el programa')
archivo=open('productoPrecio.csv','w')
#El CSV separa las columnas por medio de tabuladores
for x in range(0,177):
    #Ruta de la página web
    url = 'http://www.dia.es/compra-online/productos/c/WEB.000.000.00000?q=%3Aname-asc&page='+str(x)+'&disp=grid'
    preparar(archivo,url,x)
 
archivo.close()
print('Fin del programa')