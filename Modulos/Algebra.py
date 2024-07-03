import math
import numpy as np
import Espectro
import Polinomios
#######################################################################
#######################################################################
#############                FUNCION                     ##############
def Busco_minimos(x, y):
#
    # Hace una busqueda de maximos y minimos en intervalo dado
    # en este caso buscamos en el intervalo [3700, 4150]
#
    xi= 3700.
    xf= 4150.
#
    x_min= []
    y_min= []
#
    for i in range(len(x)):
        if xi <= x[i] and x[i] <= xf:
            a1= (y[i - 1] - y[i]) / (x[i - 1] - x[i])
            a2= (y[i] - y[i + 1]) / (x[i] - x[i + 1])
            if a1*a2 < 0.:
                if a1 < 0.: # es un minimo
                    x_min.append ( x[i] )
                    y_min.append ( y[i] )
    return x_min, y_min
#===============================================================================
def Busco_maximos(x, y):
#
    # Hace una busqueda de maximos y minimos en intervalo dado
    # en este caso buscamos en el intervalo [3700, 3850]
#
    xi= 3700.
    xf= 3850.
#
    x_max= []
    y_max= []
#
    for i in range(len(x)):
        if xi <= x[i] and x[i] <= xf:
            a1= (y[i - 1] - y[i]) / (x[i - 1] - x[i])
            a2= (y[i] - y[i + 1]) / (x[i] - x[i + 1])
            if a1*a2 < 0.:
                if a1 > 0.: # es un maximo
                    x_max.append ( x[i] )
                    y_max.append ( y[i] )
    return x_max, y_max
#===============================================================================
def Busco_lineas_balmer(x_min, y_min):
#
# Posicion teorica de las lineas de Balmer
    H= [3713., 3723., 3735., 3751., 3771., 3799., 3837., 3890., 3971., 4103.]
#
# Buscamos los minimos mas cercanos a las lineas
#
    x_H= []
    y_H= []
#
    i= 1
    i1= 0
    i2= len(x_min)
#
    for j in range(len(H)):
        hay_min= False
        dist1= abs(x_min[i-1] - H[j])
        dist2= abs(x_min[i] - H[j])
        while i1 < i and i < i2 and not hay_min:
            dist3= abs(x_min[i+1] - H[j])
            if dist1 < dist2 and dist2 < dist3:
                x_H.append( x_min[i-1] )
                y_H.append( math.log(y_min[i-1],10) )
                i1= i
                hay_min= True
            elif dist2 < dist1 and dist2 < dist3:
                x_H.append( x_min[i] )
                y_H.append( math.log(y_min[i],10) )
                i1= i + 1
                hay_min= True
            else:
                i += 1
                dist1= dist2
                dist2= dist3
        i= i1 + 1
        
#
    return x_H, y_H
#===============================================================================
def Interseccion(recta, parabola):
#
# recta         y1= a1 x + b1
# parabola      y2= a2 x^2 + b2 x + c2
#
# para encontrar la interseccion hay que resolver la ecuacion cuadratica
#
#             a2 x^2 + (b2 - a1) x + (c2 - b1) = 0
#
    a= parabola.coef[0]
    b= parabola.coef[1] - recta.coef[0]
    c= parabola.coef[2] - recta.coef[1]
#
    D= b**2 - 4. * a * c
#
    if D < 0.: # no tiene solucion en reales
        sol= False
        x1= 0.
        x2= 0.
    elif D == 0.:
        x1= -b / (2. * a)
        x2= x1
        sol= True
    else:
        x1= (-b + math.sqrt(D)) / (2. * a)
        x2= (-b - math.sqrt(D)) / (2. * a)
        sol= True
#
    return x1, x2, sol
#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------
def Busco_elemento(v, x):
#
# Dado un vector v y un elemento x, busco el elemento v(i) mas cercano a x
# y devuelve la posicion i y v(i)
#
    key= True
    n= len(v) - 1
    dist_min= abs( v[0] - x )
#
    k= 0
    for i in v:
        dist= abs( i - x )
        if dist <= dist_min:
            dist_min= dist
            pos= k
        k += 1
#
    return pos, v[pos]
#-------------------------------------------------------------------------------
