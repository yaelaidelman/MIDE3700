#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
import numpy as np
import math
import copy

class Allen:
# Atributos de la clase
    archivo_in= ""    # Nombre del archivo que tiene la lista de las tablas
#
# Tabla 1 para las clases de luminosidad I, III y V:
# col 1: tipo espectral
# col 2: magnitud absoluta
# col 3: temperatura efectiva
# col 4: correccion bolometrica
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
        self.archivo_in= "Input/Allen.in"
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
        print("Cargo Tablas de Allen \ Load Allen Tables\n")

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
                mv= float(columna[1])
                teff= float(columna[2])
                cb= float(columna[3])
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
                tabla1.append( [te, mv, teff, cb] )
                linea= f_tabla.readline()# leemos la siguiente linea del archivo
#
        f_tabla.close()
        return tabla1
#-------------------------------------------------------------------------------
    def Cargo_Tabla2(self, archivo):
        tabla2= []
        f_tabla= open(archivo, 'r') # Abro el archivo de lectura
        linea= f_tabla.readline()
        linea= f_tabla.readline()
        while linea != "":
                columna= linea.split("  ")
#
                te1= str(columna[0])
                logg= float(columna[1])
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
    def Calculo_teff(self, te, cl):
#
# Elijo la tabla en funcion de la clase de luminosidad
#
        if cl == "Ia" or cl == "Ib" or cl == "II":
            tabla= copy.copy( self.tabla1_I )
            teff= self.Interpolo1_teff(te, tabla)
        elif cl == "III":
            tabla= copy.copy( self.tabla1_III )
            teff= self.Interpolo1_teff(te, tabla)
        elif cl == "IV":
            tabla1= copy.copy( self.tabla1_III )
            tabla2= copy.copy( self.tabla1_V )
            teff= self.Interpolo2_teff(te, tabla1, tabla2)
        else:
            tabla= copy.copy( self.tabla1_III )
            teff= self.Interpolo1_teff(te, tabla)
#
        return teff
#-------------------------------------------------------------------------------
    def Interpolo1_teff(self, te, tabla):
#
# Al tipo espectral le asigno un numero entero
#
        x= te[0:1]
        if x == "O":
            ties= int(te[1:2])
        elif x == "B":
            ties= 10 + int(te[1:2])
        elif x == "A":
            ties= 20 + int(te[1:2])
        elif x == "F":
            ties= 30 + int(te[1:2])
        elif x == "G":
            ties= 40 + int(te[1:2])
        elif x == "K":
            ties= 50 + int(te[1:2])
        elif x == "M":
            ties= 50 + int(te[1:2])
#
        te1= tabla[0][0]
        n= len(tabla)# cantidad de filas de la tabla
        i= 0
#
        if ties < te1:
            te2= tabla[i+1][0]
            temp1= tabla[i][2]
            temp2= tabla[i+1][2]
            teff= temp2 - (te2 - ties)*(temp2 - temp1)/(te2 - te1)
            calculo= True
        elif te1 <= ties and ties < tabla[n][0]:
            calculo= False
            while not calculo:
                te2= tabla[i+1][0]
                if te1 <= ties and ties < te2:
                    temp1= tabla[i][2]
                    temp2= tabla[i+1][2]
                    teff= temp2 - (te2 - ties)*(temp2 - temp1)/(te2 - te1)
                    calculo= True
                else:
                    te1= te2
                    temp1= temp2
                    i += 1
        elif tabla[n][0] <= ties:
            te1= tabla[n-1][0]
            te2= tabla[n][0]
            temp1= tabla[n-1][2]
            temp2= tabla[n][2]
            teff= temp1 + (ties - te1)*(temp2 - temp1)/(te2 - te1)
#
        return teff
#-------------------------------------------------------------------------------
    def Interpolo2_teff(self, te, tabla1, tabla2):
#
        teff1= self.Interpolo1_teff(te, tabla1)
        teff2= self.Interpolo1_teff(te, tabla2)
#
        teff= teff1 + (teff2 - teff1)/2.
#
        return teff
#-------------------------------------------------------------------------------
