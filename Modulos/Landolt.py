#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
import numpy as np
import math
import copy
import Algebra

class Landolt:
# Atributos de la clase
    archivo_in= ""    # Nombre del archivo que tiene la lista de las tablas
#
# Tabla 1 para las clases de luminosidad I, III y V:
# col 1: tipo espectral
# col 2: temperatura efectiva
# col 3: magnitud absoluta
# col 4: magnitud bolometrica
#
    tabla1_I= []
    tabla1_III= []
    tabla1_V= []
#
# Tabla 2 para las clases de luminosidad I, III y V:
# col 1: tipo espectral
# col 2: log g
#
    tabla2_I= []
    tabla2_III= []
    tabla2_V= []
#-------------------------------------------------------------------------------
    def __init__(self):
        self.archivo_in= "Input/Landolt.in"
        self.tabla1_I= []
        self.tabla1_III= []
        self.tabla1_V= []
        self.tabla2_I= []
        self.tabla2_III= []
        self.tabla2_V= []
#
        self.Cargo_Tablas()
        return
#-------------------------------------------------------------------------------
    def Cargo_Tablas(self):
#
        print("Cargo Tablas de Landolt \ Load Landolt tables\n")
        tablas_in= self.Leo_Archivo()
#
        self.tabla1_I= self.Cargo_Tabla1(tablas_in[0])
        self.tabla1_III= self.Cargo_Tabla1(tablas_in[1])
        self.tabla1_V= self.Cargo_Tabla1(tablas_in[2])
#
        self.tabla2_I=  self.Cargo_Tabla2(tablas_in[3])
        self.tabla2_III= self.Cargo_Tabla2(tablas_in[4])
        self.tabla2_V= self.Cargo_Tabla2(tablas_in[5])
#
        return
#-------------------------------------------------------------------------------
    def Leo_Archivo(self):
#
        f_tabla= open(self.archivo_in, 'r') # Abro el archivo de lectura
        linea= f_tabla.readline()
        tablas_in= []
#
# Leemeos el archivo
        while linea != "": # Lee linea por linea hasta el final del archivo
# Como las columnas estan separadas por espacios guardamos las columnas
# en una lista
            columna= linea.split("  ")
            n= len( str(columna[0]) )
            col= str( columna[0] )[0:n-1]
            tablas_in.append( col )# Primera columna del archivo
            linea= f_tabla.readline()# leemos la siguiente linea del archivo
#
        f_tabla.close()
        return tablas_in
#-------------------------------------------------------------------------------
    def Cargo_Tabla1(self, archivo):
        tabla1= []
        f_tabla= open(archivo, 'r') # Abro el archivo de lectura
        linea= f_tabla.readline()
        linea= f_tabla.readline()
        while linea != "":
                columna= linea.split("  ")
#
                te1= str(columna[0])
                teff= float(columna[1])
                mv= float(columna[2])
                mbol= float(columna[3])
#
# Al tipo espectral le asigno un numero entero
#
                x= te1[0:1]
                if x == "O":
                    te= int(te1[1:2])
                elif x == "B":
                    te= 10 + int(te1[1:2])
                elif x == "A":
                    te= 20 + int(te1[1:2])
                elif x == "F":
                    te= 30 + int(te1[1:2])
                elif x == "G":
                    te= 40 + int(te1[1:2])
                elif x == "K":
                    te= 50 + int(te1[1:2])
                elif x == "M":
                    te= 60 + int(te1[1:2])
#
                tabla1.append( [te, teff, mv, mbol] )
                linea= f_tabla.readline()# leemos la siguiente linea del archivo
#
        f_tabla.close()
        return tabla1
#-------------------------------------------------------------------------------
    def Cargo_Tabla2(self, archivo):
        log_gsol= 4.43775# gsol= 2.74 x 10^4 cm/s^2
        tabla2= []
        f_tabla= open(archivo, 'r') # Abro el archivo de lectura
        linea= f_tabla.readline()
        linea= f_tabla.readline()
        while linea != "":
                columna= linea.split("  ")
#
                te1= str(columna[0])
                logg= float( columna[1] ) + log_gsol# porque la tabla da log(g/gsol)
#
# Al tipo espectral le asigno un numero entero
#
                x= te1[0:1]
                if x == "O":
                    te= int(te1[1:2])
                elif x == "B":
                    te= 10 + int(te1[1:2])
                elif x == "A":
                    te= 20 + int(te1[1:2])
                elif x == "F":
                    te= 30 + int(te1[1:2])
                elif x == "G":
                    te= 40 + int(te1[1:2])
                elif x == "K":
                    te= 50 + int(te1[1:2])
                elif x == "M":
                    te= 60 + int(te1[1:2])
#
                tabla2.append( [te, logg] )
                linea= f_tabla.readline()# leemos la siguiente linea del archivo
#
        f_tabla.close()
        return tabla2
#-------------------------------------------------------------------------------
    def Calculo_teff(self, ties, cl):
#
# Elijo la tabla en funcion de la clase de luminosidad
#
        if cl == "Ia" or cl == "Ib" or cl == "II":
            tabla= self.Armo_tabla(self.tabla1_I, 1)
            calculo, teff, extrapolo= self.Interpolo1(ties, tabla)
        elif cl == "III":
            tabla= self.Armo_tabla(self.tabla1_III, 1)
            calculo, teff, extrapolo= self.Interpolo1(ties, tabla)
        elif cl == "IV":
            tabla1= self.Armo_tabla(self.tabla1_III, 1)
            tabla2= self.Armo_tabla(self.tabla1_V, 1)
            calculo, teff, extrapolo= self.Interpolo2(ties, tabla1, tabla2)
        else:
            tabla= self.Armo_tabla(self.tabla1_V, 1)
            calculo, teff, extrapolo= self.Interpolo1(ties, tabla)
#
        return calculo, teff, extrapolo
#-------------------------------------------------------------------------------
    def Calculo_logg(self, ties, cl):
#
# Elijo la tabla en funcion de la clase de luminosidad
#
        if cl == "Ia" or cl == "Ib" or cl == "II":
            tabla= copy.copy(self.tabla2_I)
            calculo, logg, extrapolo= self.Interpolo1(ties, tabla)
        elif cl == "III":
            tabla= copy.copy(self.tabla2_III)
            calculo, logg, extrapolo= self.Interpolo1(ties, tabla)
#
        # Esta tabla esta muy incompleta. Si la estrella esta entre B5 y G0 el valor es dudoso
            if 15 < ties and ties < 40:
                extrapolo= True
#
        elif cl == "IV":
            tabla1= copy.copy(self.tabla2_III)
            tabla2= copy.copy(self.tabla2_V)
            calculo, logg, extrapolo= self.Interpolo2(ties, tabla1, tabla2)
        else:
            tabla= copy.copy(self.tabla2_V)
            calculo, logg, extrapolo= self.Interpolo1(ties, tabla)
#
        return calculo, logg, extrapolo
#-------------------------------------------------------------------------------
    def Calculo_mv(self, ties, cl):
#
# Elijo la tabla en funcion de la clase de luminosidad
#
        if cl == "Ia" or cl == "Ib" or cl == "II":
            tabla= self.Armo_tabla(self.tabla1_I, 2)
            calculo, mv, extrapolo= self.Interpolo1(ties, tabla)
        elif cl == "III":
            tabla= self.Armo_tabla(self.tabla1_III, 2)
            calculo, mv, extrapolo= self.Interpolo1(ties, tabla)
        elif cl == "IV":
            tabla1= self.Armo_tabla(self.tabla1_III, 2)
            tabla2= self.Armo_tabla(self.tabla1_V, 2)
            calculo, mv, extrapolo= self.Interpolo2(ties, tabla1, tabla2)
        else:
            tabla= self.Armo_tabla(self.tabla1_V, 2)
            calculo, mv, extrapolo= self.Interpolo1(ties, tabla)
#
        return calculo, mv, extrapolo
#-------------------------------------------------------------------------------
    def Calculo_mbol(self, ties, cl):
#
# Elijo la tabla en funcion de la clase de luminosidad
#
        if cl == "Ia" or cl == "Ib" or cl == "II":
            tabla= self.Armo_tabla(self.tabla1_I, 3)
            calculo, mbol, extrapolo= self.Interpolo1(ties, tabla)
        elif cl == "III":
            tabla= self.Armo_tabla(self.tabla1_III, 3)
            calculo, mbol, extrapolo= self.Interpolo1(ties, tabla)
        elif cl == "IV":
            tabla1= self.Armo_tabla(self.tabla1_III, 3)
            tabla2= self.Armo_tabla(self.tabla1_V, 3)
            calculo, mbol, extrapolo= self.Interpolo2(ties, tabla1, tabla2)
        else:
            tabla= self.Armo_tabla(self.tabla1_V, 3)
            calculo, mbol, extrapolo= self.Interpolo1(ties, tabla)
#
        return calculo, mbol, extrapolo
#-------------------------------------------------------------------------------
    def Armo_tabla(self, tabla1, col):
        tabla= []
        for i in range( len(tabla1) ):
            tabla.append( [ tabla1[i][0], tabla1[i][col] ]  )
        return tabla
#-------------------------------------------------------------------------------
    def Interpolo1(self, ties, tabla):
#
        te1= tabla[0][0]
        n= len(tabla) - 1# ultima fila de la tabla
        i= 0
#
        if ties < te1:
            te2= tabla[i+1][0]
            y1= tabla[i][1]
            y2= tabla[i+1][1]
            y= y2 - (te2 - ties)*(y2 - y1)/(te2 - te1)
            calculo= True
            extrapolo= True
        elif te1 <= ties and ties < tabla[n][0]:
            calculo= False
            while not calculo:
                te2= tabla[i+1][0]
                if te1 <= ties and ties < te2:
                    y1= tabla[i][1]
                    y2= tabla[i+1][1]
                    y= y2 - (te2 - ties)*(y2 - y1)/(te2 - te1)
                    calculo= True
                    extrapolo= False
                else:
                    te1= te2
                    i += 1
        elif tabla[n][0] <= ties:
            te1= tabla[n-1][0]
            te2= tabla[n][0]
            y1= tabla[n-1][1]
            y2= tabla[n][1]
            y= y1 + (ties - te1)*(y2 - y1)/(te2 - te1)
            calculo= True
            extrapolo= True
        else:
            calculo= False
            extrapolo= False
#
        return calculo, y, extrapolo
#-------------------------------------------------------------------------------
    def Interpolo2(self, ties, tabla1, tabla2):
#
        calculo1, y1, extrapolo1= self.Interpolo1(ties, tabla1)
        calculo2, y2, extrapolo2= self.Interpolo1(ties, tabla2)
#
        if calculo1 and calculo2:
            y= y1 + (y2 - y1)/2.
            calculo= True
            if extrapolo1 or extrapolo2:
                extrapolo= True
            else:
                extrapolo= False
        else:
            calculo= False
            extrapolo= False
#
        return calculo, y, extrapolo
#-------------------------------------------------------------------------------
    def Error(self, ties, cl, Mag, val):
#
# El error es de un subtipo espectral y de una clase de luminosidad
#
        err_te= 1
#
        ties1= ties + err_te
        ties2= ties - err_te
#
        if cl == "Ia" or "Ib":
            if Mag == "teff":
                calculo, val1, extrapolo= self.Calculo_teff(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_teff(ties2, cl)
            elif Mag == "logg":
                calculo, val1, extrapolo= self.Calculo_logg(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_logg(ties2, cl)
            elif Mag == "mv":
                calculo, val1, extrapolo= self.Calculo_mv(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_mv(ties2, cl)
            elif Mag == "mbol":
                calculo, val1, extrapolo= self.Calculo_mbol(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_mbol(ties2, cl)
#
            err1= abs(val - val1)
            err2= abs(val - val2)
#
            error= (err1 + err2) / 2.
#
        elif cl == "II":
            cl1= "Ib"
            cl2= "III"
            if Mag == "teff":
                calculo, val1, extrapolo= self.Calculo_teff(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_teff(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_teff(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_teff(ties2, cl2)
            elif Mag == "logg":
                calculo, val1, extrapolo= self.Calculo_logg(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_logg(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_logg(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_logg(ties2, cl2)
            elif Mag == "mv":
                calculo, val1, extrapolo= self.Calculo_mv(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_mv(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_mv(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_mv(ties2, cl2)
            elif Mag == "mbol":
                calculo, val1, extrapolo= self.Calculo_mbol(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_mbol(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_mbol(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_mbol(ties2, cl2)
#
            err1= abs(val - val1)
            err2= abs(val - val2)
            err3= abs(val - val3)
            err4= abs(val - val4)
#
            error= (err1 + err2 + err3 + err4) / 4.
#
        elif cl == "III":
            cl1= "II"
            cl2= "IV"
            if Mag == "teff":
                calculo, val1, extrapolo= self.Calculo_teff(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_teff(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_teff(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_teff(ties2, cl2)
            elif Mag == "logg":
                calculo, val1, extrapolo= self.Calculo_logg(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_logg(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_logg(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_logg(ties2, cl2)
            elif Mag == "mv":
                calculo, val1, extrapolo= self.Calculo_mv(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_mv(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_mv(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_mv(ties2, cl2)
            elif Mag == "mbol":
                calculo, val1, extrapolo= self.Calculo_mbol(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_mbol(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_mbol(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_mbol(ties2, cl2)
#
            err1= abs(val - val1)
            err2= abs(val - val2)
            err3= abs(val - val3)
            err4= abs(val - val4)
#
            error= (err1 + err2 + err3 + err4) / 4.
#
        elif cl == "IV":
            cl1= "III"
            cl2= "V"
            if Mag == "teff":
                calculo, val1, extrapolo= self.Calculo_teff(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_teff(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_teff(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_teff(ties2, cl2)
            elif Mag == "logg":
                calculo, val1, extrapolo= self.Calculo_logg(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_logg(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_logg(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_logg(ties2, cl2)
            elif Mag == "mv":
                calculo, val1, extrapolo= self.Calculo_mv(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_mv(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_mv(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_mv(ties2, cl2)
            elif Mag == "mbol":
                calculo, val1, extrapolo= self.Calculo_mbol(ties1, cl1)
                calculo, val2, extrapolo= self.Calculo_mbol(ties2, cl1)
                calculo, val3, extrapolo= self.Calculo_mbol(ties1, cl2)
                calculo, val4, extrapolo= self.Calculo_mbol(ties2, cl2)
#
            err1= abs(val - val1)
            err2= abs(val - val2)
            err3= abs(val - val3)
            err4= abs(val - val4)
#
            error= (err1 + err2 + err3 + err4) / 4.
#
        elif cl == "V":
            if Mag == "teff":
                calculo, val1, extrapolo= self.Calculo_teff(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_teff(ties2, cl)
            elif Mag == "logg":
                calculo, val1, extrapolo= self.Calculo_logg(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_logg(ties2, cl)
            elif Mag == "mv":
                calculo, val1, extrapolo= self.Calculo_mv(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_mv(ties2, cl)
            elif Mag == "mbol":
                calculo, val1, extrapolo= self.Calculo_mbol(ties1, cl)
                calculo, val2, extrapolo= self.Calculo_mbol(ties2, cl)
#
            err1= abs(val - val1)
            err2= abs(val - val2)
#
            error= (err1 + err2) / 2.
#
        return error
#-----------------------------------------------------------------------------------------
