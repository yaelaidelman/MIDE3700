#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
import numpy as np
import Algebra
import numpy as np
import multiprocessing

from Modulos import Landolt
from Funciones_auxiliares import distancia_euclidea, distancia_euclidea_v2,entre_puntos,producto_cruzado
from Funciones_auxiliares import get_puntos_curva_completa, get_puntos_curva
from Funciones_auxiliares import minimo_punto_busqueda_binaria, buscar_medio, fijar_rango,  calcular_min_punto, calcular_minima_distancia_a_curva
from Archivos.diccionarios import curvas_mas_cercanas, curves, curvas_de_extrapolacion, curvas_externas

class Curvas:
    # Atributos de la clase
    archivo_in= ""    # Nombre del archivo que tiene la lista de curvas
    cte_curvas= []    # Guarda el valor constante de cada curva
    x0= float()       # Inicio del eje x
    xn= float()       # Fin del eje x
    y0= float()       # Inicio del eje y
    yn= float()       # Fin del eje y
    kx= int()         # Escaleo del eje x
    ky= int()         # Escaleo del eje y
    nc= int()         # Cantidad de curvas de nivel
    matriz= [[],[]]   # Matriz que guarda las curvas de nivel

    #---------------------------------------------------------------------------
    def __init__(self, magnitud):
        self.archivo_in= "Input/Curva" + magnitud + ".in"
        self.cte_curvas= []
        self.matriz= [[],[]]
        self.titulo = ""

        self.cargo_curvas_rellenas(magnitud)
        return
    #---------------------------------------------------------------------------
    def cargo_curvas_rellenas(self, magnitud):

        print("Cargo curvas de ", magnitud," \ Load ", magnitud, " curves\n")

        if magnitud == "Teff":

            self.nc= 13
            #Curva inferior nueva
            self.cte_curvas.append( 9250. )

            self.cte_curvas.append( 9500. )
            self.cte_curvas.append( 10000. )
            self.cte_curvas.append( 11000. )
            self.cte_curvas.append( 12500. )
            self.cte_curvas.append( 15000. )
            self.cte_curvas.append( 17500. )
            self.cte_curvas.append( 20000. )
            self.cte_curvas.append( 22500. )
            self.cte_curvas.append( 25000. )
            self.cte_curvas.append( 30000. )
            self.cte_curvas.append( 35000. )

            #Curva superior nueva
            self.cte_curvas.append( 37500. )

            self.x0= 0.
            self.xn= 0.55
            self.y0= -15.
            self.yn= 86.
            self.kx= 100
            self.ky= 10

        elif magnitud == "TE_c":

            self.nc= 14

            # A cada tipo espectral le asignamos le asignamos un numero entero:
            # O0 => 0
            # B0 => 10
            # A0 => 20
            
            #Curva inferior nueva
            self.cte_curvas.append(  5.5 )# => tipo espectral O5

            self.cte_curvas.append(  6. )# => tipo espectral O6
            self.cte_curvas.append(  8. )# => tipo espectral O8
            self.cte_curvas.append( 10. )# => tipo espectral B0
            self.cte_curvas.append( 11. )# => tipo espectral B1
            self.cte_curvas.append( 12. )# => tipo espectral B2
            self.cte_curvas.append( 13. )# => tipo espectral B3
            self.cte_curvas.append( 15. )# => tipo espectral B5
            self.cte_curvas.append( 17. )# => tipo espectral B7
            self.cte_curvas.append( 19. )# => tipo espectral B9
            self.cte_curvas.append( 20. )# => tipo espectral A0
            self.cte_curvas.append( 22. )# => tipo espectral A2
            self.cte_curvas.append( 23. )# => tipo espectral A3

            self.cte_curvas.append( 25. )# => tipo espectral A5

            #Curva superior nueva
            # self.cte_curvas.append(  23.5 )# => tipo espectral A3.5

            self.x0= 0.
            self.xn= 0.730
            self.y0= -15.
            self.yn= 86.
            # self.kx= 10000
            self.kx= 100
            self.ky= 10

        elif magnitud == "TE_f":

            self.nc= 11

            # A cada tipo espectral le asignamos le asignamos un numero entero:
            # A0 => 20
            # F0 => 30
            # G0 => 40

            
            #MODIFICO WARNING AVISO ACA YAEL
            # self.cte_curvas.append( 37. )# => tipo espectral A7 

            self.cte_curvas.append( 24.)# => Area de extrapolación

            self.cte_curvas.append( 25. )# => tipo espectral A5
            self.cte_curvas.append( 27. )# => tipo espectral A7
            self.cte_curvas.append( 30. )# => tipo espectral F0
            self.cte_curvas.append( 32. )# => tipo espectral F2
            self.cte_curvas.append( 34. )# => tipo espectral F4
            self.cte_curvas.append( 36. )# => tipo espectral F6
            self.cte_curvas.append( 37. )# => tipo espectral F7
            self.cte_curvas.append( 38. )# => tipo espectral F8
            self.cte_curvas.append( 40. )# => tipo espectral G0

            self.cte_curvas.append( 41. )# => Area de extrapolación


            self.x0= 0.
            self.xn= 0.730
            self.y0= -15.
            self.yn= 86.
            self.kx= 100
            self.ky= 10

        elif magnitud == "CL_c":

            self.nc= 7

            # A cada clase de luminosidad le asignamos le asignamos un numero entero:
            # Ia => 0
            # Ib => 1
            # II => 2
            # III => 3
            # IV => 4
            # V => 5
            # VI => 6

            self.cte_curvas.append( 0. )
            self.cte_curvas.append( 1. )
            self.cte_curvas.append( 2. )
            self.cte_curvas.append( 3. )
            self.cte_curvas.append( 4. )
            self.cte_curvas.append( 5. )
            self.cte_curvas.append( 6. )

            self.x0= 0.
            self.xn= 0.70
            self.y0= -5.
            self.yn= 80.
            self.kx= 100
            self.ky= 10

        elif magnitud == "CL_f":

            self.nc= 5

            # A cada clase de luminosidad le asignamos le asignamos un numero entero:
            # Ia => 0
            # Ib => 1
            # II => 2
            # III => 3
            # IV => 4
            # V => 5
            # VI => 6

            self.cte_curvas.append( 1. )
            self.cte_curvas.append( 2. )
            self.cte_curvas.append( 3. )
            self.cte_curvas.append( 4. )
            self.cte_curvas.append( 5. )

            self.x0= 0.
            self.xn= 0.70
            self.y0= -5.
            self.yn= 80.
            self.kx= 100
            self.ky= 10
        
        elif magnitud == "Logg":

            self.nc= 12

            self.cte_curvas.append( 2.7 )
            self.cte_curvas.append( 2.8 )
            self.cte_curvas.append( 3.0 )
            self.cte_curvas.append( 3.2 )
            self.cte_curvas.append( 3.4 )
            self.cte_curvas.append( 3.6 )
            self.cte_curvas.append( 3.8 )
            self.cte_curvas.append( 4.0 )
            self.cte_curvas.append( 4.1)
            self.cte_curvas.append( 4.2 )
            self.cte_curvas.append( 4.3 )
            self.cte_curvas.append( 4.35)

            self.x0= 0.
            self.xn= 0.73
            self.y0= -15.
            self.yn= 86.
            self.kx= 100
            self.ky= 10

            # print(self.cte_curvas)

        elif magnitud == "Mv":

            self.nc= 11

            self.cte_curvas.append(-6.25 )
            for i in range( -6, 0):
                self.cte_curvas.append( float(i) )
                
            self.cte_curvas.append( -0.5 )
            self.cte_curvas.append( 0.0 )
            self.cte_curvas.append( 0.5 )
            self.cte_curvas.append( 0.75 )

            # print(self.cte_curvas)

            self.x0= 0.
            self.xn= 0.73
            self.y0= -15.
            self.yn= 84.
            self.kx= 100
            self.ky= 10

        elif magnitud == "Mbol":

            self.nc= 18

            self.cte_curvas.append( -8.25 )
            self.cte_curvas.append( -8.0 )
            for i in range( 2, self.nc-1):
                self.cte_curvas.append( self.cte_curvas[i-1] + 0.5 )
            self.cte_curvas.append( -0.25)

            self.x0= 0.
            self.xn= 0.73
            self.y0= -15.
            self.yn= 86.
            self.kx= 100
            self.ky= 10

            # print(self.cte_curvas)
        
        elif magnitud == "PHIo_c":

            self.nc= 14

            self.cte_curvas.append( 0.655 ) #Curva inferior

            self.cte_curvas.append( 0.66 )
            self.cte_curvas.append( 0.67 )
            self.cte_curvas.append( 0.68 )
            self.cte_curvas.append( 0.69 )

            self.cte_curvas.append( 0.70 )
            self.cte_curvas.append( 0.72 )
            self.cte_curvas.append( 0.76 )
            self.cte_curvas.append( 0.80 )

            self.cte_curvas.append( 0.86 )
            self.cte_curvas.append( 0.93 )
            self.cte_curvas.append( 1.05 )
            self.cte_curvas.append( 1.12 )

            self.cte_curvas.append( 1.24) #Curva superior

            # self.cte_curvas.append( 1.27 ) Eliminar, este debe ser el valor viejo
            # self.cte_curvas.append( 1.35 ) 

            self.x0= 0.
            self.xn= 0.730
            self.y0= -8.
            self.yn= 86.
            self.kx= 100
            self.ky= 10

        elif magnitud == "PHIo_f":

            self.nc= 11
            
            self.cte_curvas.append( 1.16 ) #Curva inferior de extrapolación
            self.cte_curvas.append( 1.27 )
            self.cte_curvas.append( 1.45 )
            self.cte_curvas.append( 1.62 )
            self.cte_curvas.append( 1.77 )
            self.cte_curvas.append( 1.97 )
            self.cte_curvas.append( 2.14 )
            self.cte_curvas.append( 2.27 )
            self.cte_curvas.append( 2.40 )
            self.cte_curvas.append( 2.65 )
            self.cte_curvas.append( 2.77 )#Curva inferior de extrapolación

            self.x0= 0.
            self.xn= 0.7330
            self.y0= -15.
            self.yn= 86.
            self.kx= 100
            self.ky= 10

        curvas_in= self.Leo_Archivo()
        # self.Matriz_Curvas(curvas_in) Versión anterior, donde se cargan las curvas de a una y se convierten en matriz
        self.Matriz_Curvas_Rellenas(curvas_in)
        return
    #---------------------------------------------------------------------------
    def Leo_Archivo(self):
        with open(self.archivo_in, 'r') as f_curva:
            return [linea.split()[0] for linea in f_curva if linea.strip()]
    
    def nombrar_archivo(self, curvas_in):
        """
        Dada la ruta de una archivo le devuelve el nombre
        si es que tiene una carpeta en el medio el nombre sera  
        la 2da carpeta.

        Args:
            curvas_in (list): lista de directorios

        Returns:
            sting : nombre del archivo
            
        """
        titulo = ""
        parseo_ruta = curvas_in[0].split("/")
        if len(parseo_ruta) == 3:
            titulo = parseo_ruta[1]
        else:
            titulo = parseo_ruta[1]+"-"+parseo_ruta[2]     
            
        return titulo
        
    #---------------------------------------------------------------------------
    def Matriz_Curvas_Rellenas(self, curvas_in):
        """
        Version: 2.0
        Carga las matrices alamacenadas en archivos .npy, que contienen valores mapeados
        """  
        self.titulo = self.nombrar_archivo(curvas_in)
        self.matriz = np.load("./Matrices/"+self.titulo+".npy", allow_pickle=True)
    
        return self.matriz
    #---------------------------------------------------------------------------
    def Parametrizar(self, x, y):
        """     
        xx e yy son redimencionados para acceder a la matriz
        devuelve en i1, i2 las dimensiones de la matriz en el eje x
        devuelve en j1, j2 las dimensiones de la matriz en el eje y
        """
        
        if self.x0 >= 0.:
            i1= Algebra.Redondeo_int_mas_cerca( self.x0 * float(self.kx) )
            i2= Algebra.Redondeo_int_mas_cerca( self.xn * float(self.kx) )
            xx= x * float(self.kx)
        else:
            i1= 0
            i2= Algebra.Redondeo_int_mas_cerca( (self.xn + abs(self.x0)) * float(self.kx) )
            xx= (x + abs(self.x0)) * float(self.kx)

        # Parametrizamos el eje y y la coordenada y del punto

        if self.y0 >= 0.:
            j1= Algebra.Redondeo_int_mas_cerca( self.y0 * float(self.ky) )
            j2= Algebra.Redondeo_int_mas_cerca( self.yn * float(self.ky) )
            yy= y * float(self.ky)
        else:
            j1= 0
            j2= Algebra.Redondeo_int_mas_cerca( (self.yn + abs(self.y0)) * float(self.ky) )
            yy= (y + abs(self.y0)) * float(self.ky)
            
        return i1, i2, xx, j1, j2, yy
    #---------------------------------------------------------------------------    
    def calcular_punto_minimo(self, xy, curva_discreta, curva_completa):
        """
        Dado un punto xy y una curva, devuelve el punto de la curva que está más cerca de xy
        """    
        medio, index_curve = buscar_medio(xy, curva_discreta)

        inicio, fin = fijar_rango(medio, curva_completa)
        
        punto = calcular_min_punto(xy, curva_completa[inicio:fin])
        if self.titulo == "Logg":
            punto = calcular_min_punto(xy, curva_completa[0:len(curva_completa)-1])

        return punto, index_curve
    #---------------------------------------------------------------------------
    def minimas_distancias_con_validación(self, xy, curvas_in, curva1, curva2):
        """
        Esta función, dado:
        xy: un par con coordenadas x e y en el plano
        curvas_in: la lista de archivos que contienen las curvas almacenadas en conjuntos de puntos x,y
        curva1 y curva2, contienen el valor constante que representa la curva, una curva en el planto es un conjunto de puntos x,y -> z, donde z es el valor constante
        
        Devuelve la distancia que hay de x,y a cada una de las curvas y si realmente el punto esta entre esas curvas

        Existe el caso en el que el punto parece estar entre las curvas, pero realmente cae afuera de las curvas.
        """

        punto_1 = minimo_punto_busqueda_binaria(xy, curvas_in, curva1, self.cte_curvas)
        punto_2 = minimo_punto_busqueda_binaria(xy, curvas_in, curva2, self.cte_curvas)

        dentro_de_curvas = entre_puntos(xy, punto_1, punto_2)

        if dentro_de_curvas:
            dist1 = distancia_euclidea_v2(xy[0], punto_1[0], xy[1], punto_1[1])
            dist2 = distancia_euclidea_v2(xy[0], punto_2[0], xy[1], punto_2[1])
        else:   
            dist1 = 99999.0
            dist2 = 99999.0
                
        return dist1, dist2, dentro_de_curvas
    #---------------------------------------------------------------------------
    def definir_origen(self, curvas_in, curvas_cercanas, medio):
        #Busca en la curva del medio, un punto que este a una distanica x, para poder utilizarlo como origen, para calcular producto cruzado
        curva_discreta = get_puntos_curva(curvas_in, curvas_cercanas[1], self.cte_curvas)

        #Setea el punto de origen como referencia para calcular el producto cruzado
        try:
            punto_origen = curva_discreta[medio-1]
        except:
            punto_origen = curva_discreta[medio+1]
        
        return punto_origen  
    #-------------------------------------------------------------------------------    
    def buscar_entre_curvas(self, x, y , curvas_cercanas, curvas_in):
        """
        Curvas cercanas vienen ordenadas de menor a mayor
        Devuelve los 3 puntos más cercanos, al punto, cada uno corresponde a una curva, el diccionario tiene el siguiente formato

        La clave es la ubicación del punto, puede ser inicio, medio o fin
        El valor es el valor de la curva, y el punto más cercano a x, y
        """
        dic = {}

        #Creo las claves de los diccionarios
        for curva, ubicacion in zip(curvas_cercanas, ["inicio", "medio", "fin"]):
            dic[ubicacion] = [curva]

        #Lleno el diccionario
        for curva, ubicacion in zip(curvas_cercanas, ["inicio", "medio", "fin"]):
            curva_completa = get_puntos_curva_completa(curvas_in, curva, self.cte_curvas)
            curva_discreta = get_puntos_curva(curvas_in, curva, self.cte_curvas)

            if ubicacion == "medio":
                punto, medio = self.calcular_punto_minimo((x,y), curva_discreta, curva_completa)
            else:
                punto, _ =self.calcular_punto_minimo((x,y), curva_discreta, curva_completa)
            
            dic[ubicacion].append(punto)

        punto_origen = self.definir_origen(curvas_in, curvas_cercanas, medio)

        dic["origen"] = (punto_origen[0], punto_origen[1])

        return dic
#-------------------------------------------------------------------------------    
    def elegir_curvas(self, dic, punto):
        #El valor de los diccionarios es una lista donde el primer valor es el valor de la curva:
        # 
        origen = dic.pop("origen")
        curve1 = (dic["medio"][0], dic["medio"][1])

        medio = dic.pop("medio")[1]

        for k, v in dic.items():
            if producto_cruzado(origen, medio, v[1]) >= 0:
                punto_der = v
            else:
                punto_izq = v
            
        if producto_cruzado(origen, medio, punto) >= 0:
            curve2 = (punto_der[0], punto_der[1])
        elif(producto_cruzado(origen, medio ,punto) < 0):
            curve2 = (punto_izq[0] , punto_izq[1])
        
        #Retorna los valores: valor de la curva, punto más cercano a x, y de esa curva
        return curve1, curve2
#-------------------------------------------------------------------------------
    def obtener_curvas_cercanas(self, curva):
        #Este diccionario devuelve para un valor de la curva, cuáles son las curvas próximas
        

        curvas_cercanas = sorted(curvas_mas_cercanas[self.titulo][str(curva)])

        return curvas_cercanas
#-------------------------------------------------------------------------------
    def interpolo_sobre_punto(self, x, y, curva):
        """
        Si el punto cae sobre un punto de la curva en la matriz, no se puede determinar de que lado
        de la curva esta el punto, por lo que se hace es obtener las 3 curvas, el punto más cercano de
        cada una y luego un producto cruzado para determinar de que lado esta el punto
        
        La clave 99999.0 ya no es necesaria, en la matriz ya no se encuentre este valor.
        
        """
        curvas_cercanas = self.obtener_curvas_cercanas(curva)
        
        curvas_in = self.Leo_Archivo()

        #Si el largo es 2 quiere decir que cayo en alguna las curvas más externas.
        if len(curvas_cercanas) == 3:
            
            dic = self.buscar_entre_curvas(x, y, curvas_cercanas, curvas_in)
            curve_punto1, curve_punto2 = self.elegir_curvas(dic, (x,y))

            curva1 = curve_punto1[0]
            curva2 = curve_punto2[0]
            punto1 = curve_punto1[1]
            punto2 = curve_punto2[1]

            distancia_1 = distancia_euclidea(x, punto1[0], y , punto1[1])
            distancia_2 = distancia_euclidea(x, punto2[0], y , punto2[1])

        else:
            #Tengo las dos curvas más cercanas que son dos solamente,  por lo que se debe calcular cuales son los puntos
            #Más cercanos de cada curva 
            curva1 = curvas_cercanas[0]
            curva2 = curvas_cercanas[1] 

            distancia_1, distancia_2, dentro_de_curvas = self.minimas_distancias_con_validación((x, y), curvas_in, curva1, curva2)
    
            #Determino si el punto no esta realmente fuera de las curvas
            if not dentro_de_curvas:
                print(f"Calculo fallido para curva {self.titulo}, punto fuera de las curvas")
                print(f"Calcule fail for curve {self.titulo}, point out of the curves")
                return 99999.0
                          
        #Calculo la nueva magnitud:
        distancia_entre_curvas = distancia_1 + distancia_2
        magnitud_nueva = curva1 - distancia_1 * (curva1 - curva2) / distancia_entre_curvas
                                        
        return magnitud_nueva
#-------------------------------------------------------------------------------       
    def buscar_curvas(self, x, y):
        
        x = Algebra.Redondeo_int_mas_cerca(x)
        y = Algebra.Redondeo_int_mas_cerca(y)

        valor_en_matriz = str(self.matriz[x][y])
                
        curvas_in = self.Leo_Archivo()
        
        dict_curvas = curves[self.titulo]
        entre_curvas = dict_curvas[valor_en_matriz]
                    
        return entre_curvas
#-------------------------------------------------------------------------------
    def query_matriz(self, x, y):
        xx = Algebra.Redondeo_int_mas_cerca(x)
        yy = Algebra.Redondeo_int_mas_cerca(y)

        return self.matriz[xx][yy]
#-------------------------------------------------------------------------------    
    def calcular_magnitud(self, x, y, celda):
        """
        x e y flotantes, los redondea para indexar la matriz
        Consulta la celda de la matriz con las curvas, y devuelve el valor en esa celda
        """
        curva1, curva2 = map(float, celda.split(" "))
        curvas_in = self.Leo_Archivo()
# 
        distancia_1 = calcular_minima_distancia_a_curva((x, y), curvas_in, curva1, self.cte_curvas)
        distancia_2 = calcular_minima_distancia_a_curva((x, y), curvas_in, curva2, self.cte_curvas)

        distancia_entre_curvas = distancia_1 + distancia_2
            
        magnitud_nueva = curva1 - distancia_1 * (curva1 - curva2) / distancia_entre_curvas
                                
        return magnitud_nueva
#-------------------------------------------------------------------------------    
    def evaluo_extrapolar(self, celda):
        """
        Evalua si el punto esta fuera de las curvas, si es así, indico que se esta extrapolando
        """

        #Sobre estas curvas no tiene sentido extrapolar
        if self.titulo in ["Landolt", "CL-Calientes", "CL-Frias"]:
            return False
        
        
        
        valores = curvas_de_extrapolacion[self.titulo].values()
        claves = curvas_externas[self.titulo]
        
        for v in valores:
            if celda == f"{v[0]} {v[1]}":
                #El punto esta en un area de extrapolación
                return True
        
        celda = str(celda)
        for k in claves:
            if celda == k:
                #El punto esta sobre una de las curvas externas (que tienen valore float64)
                return True

        #Si su valor no cae sobre curvas externas ni las 2 areas externas, se debe interpolar.
        return False
 #-------------------------------------------------------------------------------   
    def Interpolo(self, x, y):
        """
        Calcula la magnitud de un punto (x,y) en la matriz de curvas de nivel.

        Args:
            x (float): Coordenada x del punto a calcular
            y (float): Coordenada y del punto a calcular

        Returns:
            bool: True si el calculo fue exitoso, False si no
            float: Magnitud calculada
            bool: True si el valor fue extrapolado, False si no
        """
        #Si cae dentro de las curvas exteriores es True
        extrapolo=False
        
        magnitud_nueva = 99999.
        i1, i2, xx, j1, j2, yy = self.Parametrizar(x, y)

        if (i1 <= xx <= i2) and (j1 <= yy <= j2):             
            
            celda = self.query_matriz(xx,yy)
            # Casos posibles:
            # Es None None, entonces cae fuera del area de las curvas
            # Es un solo valor, entonces cae sobre una curva
            # Es un string con dos valores, entonces cae entre dos curvas
            # Es un string con dos valores y estos valores son de extrapolación

            if celda != "None None":
                
                #Esta variable sirve para indicar en el archivo de salida si es que el valor fue extrapolado o no
                extrapolo = self.evaluo_extrapolar(celda)
                if extrapolo:
                    print("El valor calculado será resultado de una extrapolación")
                
                #El valor cae sobre la curva
                if type(celda) == np.float64:
                    
                    #Resolver utilizando producto cruzado para determinar de que lado de la curva se encuentra el punto.
                    magnitud_nueva = self.interpolo_sobre_punto(x, y, celda)

                #Cae entre 2 curvas
                else:
                    magnitud_nueva = self.calcular_magnitud(x, y, celda)
            
            if magnitud_nueva > 99990.:
                lohice=False
                extrapolo=False
                print(f"Calculo fallido para curva {self.titulo}, punto fuera de las curvas")
                print(f"Calcule fail for curve {self.titulo}, point out of the curves")
            else:
                lohice=True
                
            return  lohice, magnitud_nueva, extrapolo
                
        print(f"Calculo fallido para curva {self.titulo}, punto fuera de las curvas")
        print(f"Calcule fail for curve {self.titulo}, point out of the curves")
        extrapolo= False
        lohice= False
        magnitud_nueva = 99999.

        return lohice, magnitud_nueva, extrapolo
#-------------------------------------------------------------------------------
    def Error(self, D, L, M):
#
# El error de medicion en D es 0.02
# El error de medicion en lambda_1 es 2
#
        err_D= 0.02
        #err_L= 10.
        err_L= 2.
#
        D1= D + err_D
        D2= D - err_D
#
        L1= L + err_L
        L2= L - err_L
#
# Calculo el valor de la magnitud con los nuevos valores D1, D2, L1 y L2
#
        lohice1, m1, extra1= self.Interpolo(D1, L1)
        lohice2, m2, extra2= self.Interpolo(D1, L2)
        lohice3, m3, extra3= self.Interpolo(D2, L1)
        lohice4, m4, extra4= self.Interpolo(D2, L2)

#
# Ahora promediamos los valores de los errores
#
        n= 0
#
        if lohice1:
            err1= abs(M - m1)
            n= n + 1
        else:
            err1 = 0.0
#
        if lohice2:
            err2= abs(M - m2)
            n= n + 1
        else:
            err2= 0.0
#
        if lohice3:
            err3= abs(M - m3)
            n= n + 1
        else:
            err3= 0.0
#
        if lohice4:
            err4= abs(M - m4)
            n= n + 1
        else:
            err4= 0.0
#
        error= (err1 + err2 + err3 + err4) / float(n)

#
        return error
#-----------------------------------------------------------------------------------------
def cargar_curvas(nombre, curvas_dict):
        curvas = Curvas(nombre)
        curvas_dict[nombre] = curvas
#-------------------------------------------------------------------------------       
def cargar_curvas_multiproceso():
    """
    Carga las curvas en paralelo

    Returns:
        dict: Diccionario con las curvas cargadas
        Landolt: Curva de Landolt que se carga diferente
    """
    # Cargo curvas
    # Load curves
    
    # Crear una lista de nombres de curvas
    nombres_curvas = ["Teff", "TE_c", "TE_f", "CL_c", "CL_f", "Logg", "Mv", "Mbol", "PHIo_c", "PHIo_f"]

    # Crear un diccionario para almacenar las curvas
    manager = multiprocessing.Manager()
    curvas_dict = manager.dict()

    # Crear una lista de procesos
    processes = []


    # Crear un proceso para cargar cada curva
    for nombre in nombres_curvas:
        process = multiprocessing.Process(target=cargar_curvas, args=(nombre, curvas_dict))
        processes.append(process)
        process.start()

    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()

    # Accede a las curvas cargadas por su nombre
    
    # Crear el objeto Landolt
    landolt = Landolt.Landolt()
    
    return curvas_dict, landolt