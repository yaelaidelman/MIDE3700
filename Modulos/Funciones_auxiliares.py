from matplotlib.pyplot import gca, draw
import math
import matplotlib.pyplot as plt
import os

#https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle
def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1]);

def entre_puntos(xy, p1, p2):
    """ Dado un punto xy, determina si este punto se encuentra entre 2 puntos p1 y p2"""
    return (p1[0] <= xy[0] <= p2[0] or p2[0] <= xy[0] <= p1[0]) and (p1[1] <= xy[1] <= p2[1] or p2[1] <= xy[1] <= p1[1])

def point_in_triangle(pt, v1, v2, v3):
    d1 = (0,0)
    d2 = (0,0)
    d3 = (0,0)
    has_neg = False
    has_pos = False

    d1 = sign(pt, v1, v2);
    d2 = sign(pt, v2, v3);
    d3 = sign(pt, v3, v1);

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0);
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0);

    return not (has_neg and has_pos)

def Redondeo_int_mas_cerca(x):
    """
    Redondea un número al entero más cercano.
    """
    y= ( x - round(x) ) * 10
    if x >= 0.:
        if y < 5.:
            x_int= int( round(x) )
        else:
            x_int= int( round(x) + 1 )
    else:
        if abs(y) < 5.:
            x_int= int( round(x) )
        else:
            x_int= int( round(x) - 1 )        
    return x_int

# Fuente: https://stackoverflow.com/a/52617883/2116607
def redondear(n: float, decimals: int = 0) -> float:
    expoN = n * 10 ** decimals
    if abs(expoN) - abs(math.floor(expoN)) < 0.5:
        return math.floor(expoN) / 10 ** decimals
    return math.ceil(expoN) / 10 ** decimals

def calcular_min_punto(xy, curva):
    min_distance = float("inf")
    min_point = (0, 0)

    for punto in curva:
       
        x2 = punto[0]
        y2 = punto[1]

        distance = distancia_euclidea_v2(xy[0], x2, xy[1], y2)

        if distance < min_distance: 
            min_point = (x2, y2)
            min_distance = distance

    return min_point

def producto_cruzado(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) 

def calcular_min_distance(xy, curva):
    min_distance = float("inf")
    min_point = (0, 0)

    for punto in curva:
        x2 = punto[0]
        y2 = punto[1]

        distance = distancia_euclidea_v2(xy[0], x2, xy[1], y2)

        if distance < min_distance: 
            min_point = (x2, y2)
            min_punto_real = punto
            min_distance = distance

    # output = open("/home/valen/PPS/MIDE3700/tests/resultados_interpolación/resultados.txt", "a")
    # output.write(f"# {xy[0]} {xy[1]} {min_point[0]} {min_point[1]}\n")
    # output.write(f"{min_distance}\n")
    # output.close()

    # # print("El punto más cercano esta en la posición: ",min_point[0], min_point[1])
    # plt.scatter(x = min_punto_real[0], y = min_punto_real[1], c = "pink", marker = "o", s = 50)
    # plt.show()
    # plt.draw()
    # print(f"Punto minimo: {min_point}, que es {min_punto_real}, distance {min_distance}")
    
    return min_distance

def maximizar_pantalla():
    mng = plt.get_current_fig_manager()
    file = "./Configuraciones/resolucion.txt"
    tupla_resultante = (1000, 1000)
    
    try:
        with open(file, 'r') as file:
            contenido = file.read()
            valores = contenido.strip().split(',')
            
            # Asegurarse de que haya exactamente dos valores
            if len(valores) != 2:
                raise ValueError("El archivo debe contener dos valores separados por coma.")
            
            # Convertir los valores a enteros
            tupla_resultante = tuple(map(int, valores))

    except FileNotFoundError:
        print(f"Error: El archivo '{file}' no se encontró.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    mng.resize(tupla_resultante[0], tupla_resultante[1])
    return

def distancia_euclidea_v2(x1, x2, y1, y2):
    di = ((x1*100 - x2*100) ** 2)
    dj = ((y1 - y2) ** 2)
    
    return math.sqrt( di + dj )

    d1 = math.sqrt((x1 - x2) ** 2)

    d2 = math.sqrt((y1 - y2) ** 2)
    print(x1, y1, x2, y2)
    print(f"d1: {d1}")
    print(f"d2: {d2}")

    dist = (d1) + (d2)
    print(dist)
    return dist
    
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def distancia_euclidea(x1, x2, y1, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

def normalize(x, min_val, max_val):
        return (x - min_val) / (max_val - min_val)
    
def desnormalize(x_normalized, min_val, max_val):
    return x_normalized * (max_val - min_val) + min_val

def encontrar_punto_mas_cercano_normalizado(x_norm, y_norm, x_spectro_norm, y_spectro_norm):
    """
    Encuentra el punto más cercano en el espectro a las coordenadas (x_clicked, y_clicked).

    :param x_spectrum: Lista de coordenadas x del espectro Normalizado entre 0 y 1
    :param y_spectrum: Lista de coordenadas y del espectro Normalizado entre 0 y 1
    :param x_clicked: Coordenada x del clic.
    :param y_clicked: Coordenada y del clic.
    :param max_x_spectrum: Es el máximo valor del espectro en x
    :param max_y_spectrum: Es el máximo valor del espectro en y
    :return: Coordenadas x e y del espectro al punto más cercano
    """
    min_distance = float("inf")
    x = 0
    y = 0
    closest_spectrum_index = None

    for i in range(len(x_spectro_norm)):
        
        #Multiplico por 10000 a los valores de X para poder calcular las distancias euclideanas de X.
        
        distance = distancia_euclidea(x_spectro_norm[i]*10000, x_norm*10000, y_spectro_norm[i], y_norm)
        if distance < min_distance:
            min_distance = distance
            closest_spectrum_index = i
            x = x_spectro_norm[i]
            y = y_spectro_norm[i]
            
    return x, y

def encontrar_punto_mas_cercano( x_norm, y_norm, x_spectro_norm, y_spectro_norm):
    """
    Encuentra el punto más cercano en el espectro a las coordenadas (x_clicked, y_clicked).

    :param x_spectrum: Lista de coordenadas x del espectro Normalizado entre 0 y 1
    :param y_spectrum: Lista de coordenadas y del espectro Normalizado entre 0 y 1
    :param x_clicked: Coordenada x del clic.
    :param y_clicked: Coordenada y del clic.
    :param max_x_spectrum: Es el máximo valor del espectro en x
    :param max_y_spectrum: Es el máximo valor del espectro en y
    :return: Coordenadas x e y del espectro al punto más cercano
    """
    min_distance = float("inf")
    x = 0
    y = 0
    closest_spectrum_index = None

    for i in range(len(x_spectro_norm)):
        
        #Los valores del eje x se multiplican por 10000 para trabajar con valores en una escala aproximada
        
        distance = distancia_euclidea(x_spectro_norm[i], x_norm, y_spectro_norm[i], y_norm)
        if distance < min_distance:
            min_distance = distance
            closest_spectrum_index = i
            x = x_spectro_norm[i]
            y = y_spectro_norm[i]
            
    #Combierto x e y que estaban normalizados a su verdadera escala
    #x = x_spectro_norm[closest_spectrum_index] 
    #y = y_spectro_norm[closest_spectrum_index] 
        
    return x, y

def calcular_indice_del_punto_mas_cercano_normalizado(clic_x, clic_y, coor_x, coor_y):
    # Inicializa la distancia mínima como infinito y el índice del punto más cercano como -1
    distancia_minima = float('inf')
    indice_mas_cercano = -1
    
    # Itera a través de las coordenadas x e y para encontrar el punto más cercano
    for i in range(len(coor_x)):
        
        #Multiplico por 10000 para tratar con valores con una escala aproximada
        distancia = math.sqrt((clic_x*10000 - coor_x[i]*10000) ** 2 + (clic_y - coor_y[i]) ** 2)
        if distancia < distancia_minima:
            distancia_minima = distancia
            indice_mas_cercano = i
    
    # Devuelve el índice del punto más cercano
    return indice_mas_cercano



def calcular_indice_del_punto_mas_cercano(clic_x, clic_y, coor_x, coor_y):
    # Inicializa la distancia mínima como infinito y el índice del punto más cercano como -1
    distancia_minima = float('inf')
    indice_mas_cercano = -1
    
    # Itera a través de las coordenadas x e y para encontrar el punto más cercano
    for i in range(len(coor_x)):
        distancia = math.sqrt((clic_x - coor_x[i]) ** 2 + (clic_y - coor_y[i]) ** 2)
        if distancia < distancia_minima:
            distancia_minima = distancia
            indice_mas_cercano = i
    
    # Devuelve el índice del punto más cercano
    return indice_mas_cercano

#Mover a nuevo archivo
def leer_curva(file):
    """
        Dada la dirección de un archivo, lo lee y devuelve sus filas en una lista de tuplas
    """
    with open(file, 'r') as f_curva:
                
        next(f_curva)  # Saltar la primera línea

        lista_puntos = []

        for linea in f_curva:
            xy = tuple(map(float, linea.split()))
            lista_puntos.append((xy))

    return lista_puntos

def get_puntos_curva_completa(curvas_in, curva, constantes):
    """
        Dada una constante, devuelve una lista de pares x, y con los puntos que representan la curva 
    """
    lista_puntos = []
    index_file = -1

    for i in range(len(constantes)):
        if ( constantes[i] == curva ):
            index_file = i
            break
        
    lista_puntos = leer_curva(curvas_in[index_file])
        
    return lista_puntos

def get_puntos_curva(curvas_in, curva, constantes):
        """
        Dada una constante, devuelve una lista de pares x, y con los puntos que representan una
        aproximación de la curva.
        """

        lista_puntos = []
        index_file = -1

        for i in range(len(constantes)):
            if ( constantes[i] == curva ):
                index_file = i
                break

        lista_puntos = leer_curva(curvas_in[index_file].replace("Curvas/", "./Curvas_Muestreadas/"))
        
        return lista_puntos

def elegir_derecha(xy, p1, p2):
        """
        Dado un punto (x, y), devuelve True si p1, esta más cerca que p2 a (x, y)
        """

        x1 = xy[0]
        y1 = xy[1]
        x2 = p1[0]
        y2 = p1[1]

        distancia_p1 = distancia_euclidea_v2(x1, x2, y1, y2)

        x2 = p2[0]
        y2 = p2[1]

        distancia_p2 = distancia_euclidea_v2(x1, x2, y1, y2)

        return distancia_p1 < distancia_p2

#Mover a nuevo archivo
def buscar_medio(xy, c1, curvas_in = None, curva1 = None, curva2 = None):
        """
        Dada unas coordenadas x e y, retorna el indice de la curva que más se acerca al punto
        """
        #Busco en los archivos las 2 curvas, con las coordenadas x e y de cada punto 

        #Mientras no encuentre la distancia minima, buscar

        index_curva = int(len(c1)/2)
        largo_segmento = int(len(c1)/2)
        umbral_busqueda = int((len(c1)/100) * 10)
        
        punto_actual = c1[index_curva]
        punto_der = c1[index_curva-1]
        
        mover_derecha = elegir_derecha(xy, punto_actual, punto_der)

        #Mientras el tamaño del segmento no sea lo suficientemente pequeño sigo buscando
        #Pequeño será el 5% del total de los puntos en la curva
        while (largo_segmento > umbral_busqueda):

            largo_segmento /= 2
            #Buscar a derecha
            if mover_derecha:
                index_curva = int(index_curva + largo_segmento)

                punto_actual = c1[index_curva]
                punto_der = c1[index_curva-1]

            #Buscar a la izquierda
            else:
                index_curva = int(index_curva - largo_segmento)

                punto_actual = c1[index_curva]
                punto_der = c1[index_curva-1]

            mover_derecha = elegir_derecha(xy, punto_actual, punto_der)

        #Punto_actual en la posición 2, contiene el indice del de este punto en el archivo.
        medio = int( punto_actual[2] )

        return medio, index_curva

def fijar_rango(medio, curva_completa):
        """
        Calculo el inicio y el fin del rango de búsqueda
        El inicio esta una decima parte de la totalidad de los puntos de la curvas
        De forma parecida para el fin.
        """
        punto_0 = curva_completa[0]
        punto_ultimo = curva_completa[-1]
        distancia_ini_fin = distancia_euclidea_v2(punto_0[0], punto_ultimo[0], punto_0[1], punto_ultimo[1])

        largo = len(curva_completa)

        inicio  = medio - int( (len( curva_completa ) / 10) )
        
        if inicio < 0:
            inicio = 0
        else:
            punto_inicio = curva_completa[inicio]
            punto_medio = curva_completa[medio]
            
            distancia_ini_medio = distancia_euclidea_v2(punto_inicio[0], punto_medio[0], punto_inicio[1], punto_medio[1])

            while ( distancia_ini_medio < distancia_ini_fin/20) and inicio > 0:
                inicio -= int( (len( curva_completa ) / 20) )
                punto_inicio = curva_completa[inicio] if inicio > 0 else curva_completa[0]

                distancia_ini_medio = distancia_euclidea_v2(punto_inicio[0], punto_medio[0], punto_inicio[1], punto_medio[1])
            
            inicio = inicio if inicio > 0 else 0

        fin = medio + int( (largo / 10) )

        if fin > largo:
            fin = largo-1
        else:
            punto_fin = curva_completa[fin]
            punto_medio = curva_completa[medio]
            distancia_fin_medio = distancia_euclidea(punto_fin[0], punto_medio[0], punto_fin[1], punto_medio[1])
            
            # print(f"Distancia fin medio: {distancia_fin_medio}, distancia_ini_fin: {distancia_ini_fin}")
            while ( distancia_fin_medio < distancia_ini_fin/20 ) and fin < largo:
                # print(f"Distancia fin medio: {distancia_fin_medio}, distancia_ini_fin: {distancia_ini_fin}")
                fin += int( largo / 20) 

                punto_fin = curva_completa[largo-1] if fin > largo else curva_completa[fin]
                distancia_fin_medio = distancia_euclidea(punto_fin[0], punto_medio[0], punto_fin[1], punto_medio[1])
            
            fin = fin if fin < largo else largo-1

        # print(f"Retorna {inicio} y {fin}, largo: {largo}")
        return inicio, fin

 #Mover a Funciones_auxiliares
def calcular_origen(xy, curva_discreta):
        """
        Dado un punto xy y una curva, devuelve el punto de la curva que está más cerca de xy
        """
        min_distance = 99999.0
    
        punto = calcular_min_punto(xy, curva_discreta)
        
        return punto

def minimo_punto_busqueda_binaria( xy = (1, 1), curvas_in = "", curva = 0, cte_curvas= []):
        """
        Dado un punto xy y una curva, devuelve el punto de la curva que está más cerca de xy
        utilizando un algoritmo de busqueda binaria, con respecto a la distancia de los puntos a xy
        por último se calcula la distancia con los puntos alrededor de este punto encontrado

        Args:
            xy (tuple): Coordenadas x, y del punto
            curvas_in (string): Ruta de los archivos que contienen las curvas
            curva (float): Valor de la curva
        """
        curva_suavisada = get_puntos_curva(curvas_in, curva, cte_curvas)

        curva_completa = get_puntos_curva_completa(curvas_in, curva, cte_curvas)

        medio, _ = buscar_medio(xy, curva_suavisada, curvas_in)

        inicio, fin = fijar_rango(medio, curva_completa)

        punto = calcular_min_punto(xy, curva_completa[inicio:fin])
        
        return punto
  
def calcular_minima_distancia_a_curva(xy, curvas_in, curva, cte_curvas):
        """
        Dado un punto xy y una curva, devuelve la distancia al punto más cercano de la curva
        Args:
            xy (tuple): Coordenadas x, y del punto
            curvas_in (string): Ruta de los archivos que contienen las curvas
            curva (float): Valor de la curva

        Returns:
            float: Distancia al punto más cercano de la curva
        """
        punto = minimo_punto_busqueda_binaria(xy, curvas_in, curva, cte_curvas)
        dist = distancia_euclidea_v2(xy[0], punto[0], xy[1], punto[1])

        return dist
