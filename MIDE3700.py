#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
#                             octubre 2014
# PRUEBA 8: Calcula D, D*, d, lambda_1 y Phi.
#           Guarda informacion de los ajustes en un archivo
#           Guarda grafico de espectro con ajustes
#           Imprime resultados en archivo de salida
#           Calcula la temperatura efectiva de la estrella
#           Normaliza el espectro de la estrella
#           Calcula D en el espectro normalizado
#           Calcula los parametros fundamentales
#           Calcula el exceso de color y la distancia
#
######################################################################
import math
import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append('./Modulos')

from Modulos import Archivos_in_out
from Modulos import Espectro
from Modulos import Inter_Grafica
from Modulos import Polinomios
from Modulos import Algebra
from Modulos import Parametros_BCD
from Modulos import Parametros_FUN
from Modulos import Normalizo_espectro
from Modulos.Curvas import cargar_curvas_multiproceso
#import Allen
from Modulos import Distancia

#######################################################################
#######################################################################
#############            PRINCIPAL PROGRAM              ##############
# Leo el archivo de entrada
lista_estrellas, m, lohice_m= Archivos_in_out.Leo_estrellas_in()
#
# Archivos de salida
# Out files
Archivos_in_out.Genero_BCD_out()
Archivos_in_out.Genero_ParFun_out()
Archivos_in_out.Genero_Dist_out()
#-------------------------------------------------------------------------------

curvas_dict, landolt = cargar_curvas_multiproceso()

curvas_teff = curvas_dict["Teff"]
curvas_te_c = curvas_dict["TE_c"]
curvas_te_f = curvas_dict["TE_f"]
curvas_cl_c = curvas_dict["CL_c"]
curvas_cl_f = curvas_dict["CL_f"]
curvas_logg = curvas_dict["Logg"]
curvas_mv = curvas_dict["Mv"]
curvas_mbol = curvas_dict["Mbol"]
curvas_phio_c = curvas_dict["PHIo_c"]
curvas_phio_f = curvas_dict["PHIo_f"]

#obsoleto?
"""
curvas_teff= Curvas.Curvas("Teff")
curvas_te_c= Curvas.Curvas("TE_c")
curvas_te_f= Curvas.Curvas("TE_f")
curvas_cl_c= Curvas.Curvas("CL_c")
curvas_cl_f= Curvas.Curvas("CL_f")
curvas_logg= Curvas.Curvas("Logg")
curvas_mv= Curvas.Curvas("Mv")
curvas_mbol= Curvas.Curvas("Mbol")
curvas_phio_c= Curvas.Curvas("PHIo_c")
curvas_phio_f= Curvas.Curvas("PHIo_f")
#allen= Allen.Allen()
landolt= Landolt.Landolt()
"""

#-------------------------------------------------------------------------------
i= -1
for nom_est in lista_estrellas:
    i= i + 1# es un contador para poder identificar la magnitud aparente de la estrella
    #
    # Genero el espectro
    #
    espectro= Espectro.Espectro(nom_est)
    espectro.Leo_archivo()
    
#
# Ajuste del continuo de Paschen
# Fitting Paschen continuum
#
    
    espectro.Ajuste_Paschen()
#
# Ajuste del continuo de Balmer
# Fitting Balmer continuum
#
    espectro.Ajuste_Balmer()
#
# Ajuste de la envolvente inferior de las lineas de Balmer
# Fitting bottom envelope of Balmer lines
#
    espectro.Ajuste_Balmer_inf()
#
# Ajuste de la envolvente superior de las lineas de Balmer
# Fitting upper envelope of Balmer lines
#
    espectro.Ajuste_Balmer_sup()
#
# Calculamos la altura del salto de Balmer
# D* es la distancia entre el continuo de Paschen y la envolvente inferior
# d es la distancia entre el continuo de Paschen y el continuo de Balmer
# D es el salto total: D= D* + d
#
# Calculate the height of the Balmer jump
# D * is the distance between the Paschen continuum and the lower envelope
# d is the distance between Paschen's continuum and Balmer's continuum
# D is the total jump: D= D* + d
#

    BCD= Parametros_BCD.Parametros(espectro, False)
    
    BCD.Calculo_D()
#
# Calculamos la posicion media del salto de Balmer
# Calculate the mean position of the Balmer jump
#
    lambda_ok_1= BCD.Calculo_lambda1()
#
# Calculamos el gradiente de color observado
# Calculate the observed color gradient 
#
    BCD.Calculo_Phi(espectro.l_onda)
#
# Guardamos el espectro con los ajustes
# Save the spectrum with the settings
#
    c_o_f= espectro.Guardo_ajuste(BCD, 1)
#===============================================================================
# NORMALIZO EL ESPECTRO
# Spectrum normalization
#
    if lambda_ok_1:
#
        estrella_1= Parametros_FUN.Parametros(BCD, c_o_f, espectro.nombre)
#
# Calculo la temperatura efectiva
# Calculate the effective temperature
#
        estrella_1.Calculo_teff(curvas_teff, curvas_te_f, curvas_cl_f, landolt, 1)
#
# Genero el cuerpo negro correpondiete a la temperatura teff_bb calculada
# Creation of the black body corresponds to the calculated teff_bb temperature
#          
        espectro_nor= Normalizo_espectro.Normalizo_espectro(estrella_1.teff, espectro)
        
        espectro_nor.Normalizo()
        
#
# Ajusto el continuo de Paschen
# Fitting Paschen continuum
#
        espectro_nor.Ajuste_Paschen()
#
# Ajusto el continuo de Balmen
# Fitting Balmer continuum
#
        espectro_nor.Ajuste_Balmer()
#
# Ajusto la envolvente inferior de las lineas de Balmer
# Fitting bottom envelope of Balmer lines
#

            
        espectro_nor.Ajuste_Balmer_inf()
#
# Calculamos la altura del salto de Balmer
# D* es la distancia entre el continuo de Paschen y la envolvente inferior
# d es la distancia entre el continuo de Paschen y el continuo de Balmer
# D es el salto total: D= D* + d
#
# Calculate the height of the Balmer jump
# D * is the distance between the Paschen continuum and the lower envelope
# d is the distance between Paschen's continuum and Balmer's continuum
# D is the total jump: D= D* + d
#
        BCD_nor= Parametros_BCD.Parametros(espectro_nor, True)
        BCD_nor.Calculo_D()
#
# Guardamos los valores mejorados del salto de Balmer
# Saved the improved values of the Balmer jump
#
        BCD.D_total= BCD_nor.D_total
        BCD.D_est= BCD_nor.D_est
        BCD.d= BCD_nor.d
        BCD.BD2= BCD_nor.BD2
#
# Guardamos el espectro normalizado con los ajustes
# Save the normalized spectrum with the settings
#
        espectro_nor.Guardo_ajuste_2(BCD_nor)
#
# Mejoramos la posicion media del salto de Balmer
# Improve the average position of the Balmer jump 
#
        lambda_ok= BCD.Calculo_lambda1()
#
# Guardamos el espectro con los ajustes finales
# Save the spectrum with the final adjustments
#
        espectro.Guardo_ajuste(BCD, 3)
#
#===============================================================================
# CALCULAMOS LOS PARAMETROS FUNDAMENTALES
# Calculate the fundamental parameters
#
        # if lambda_ok:
        if True:
#
            estrella= Parametros_FUN.Parametros(BCD, c_o_f, espectro.nombre)
            estrella.m= m[i]
            estrella.lohice_m= lohice_m[i]
#
# Calculo el tipo espectral, clase de luminosidad y el gradiente de color intrinseco
# Spectral type, luminosity class and intrinsic color gradient
#
            if estrella.c_o_f == 'c':
                estrella.Calculo_te(curvas_te_c)
                estrella.Calculo_cl(curvas_cl_c)
                estrella.Calculo_phio(curvas_phio_c)
            else:
                estrella.Calculo_te(curvas_te_f)
                estrella.Calculo_cl(curvas_cl_f)
                estrella.Calculo_phio(curvas_phio_f)
#
# Calculo la temperatura efectiva
# Efective temperature
#
            estrella.Calculo_teff(curvas_teff, curvas_te_f, curvas_cl_f, landolt, 2)
#
# Calculo el logaritmo de la gravedad superficial
# Logarithm of surface gravity 
#
            estrella.Calculo_logg(curvas_logg, landolt)
#
# Calculo la magnitud visual absoluta
# Absolute visual magnitude
#
            estrella.Calculo_mv(curvas_mv, landolt)
#
# Calculo la magnitud bolometrica
# Bolometric magnitude
#
            estrella.Calculo_mbol(curvas_mbol, landolt)
#-------------------------------------------------------------------------------
# Calculo el exceso de color E(B-V)
# Color excess E(B-V)
#
            est_dis= Distancia.Distancia()
            est_dis.Calculo_EBV(espectro.l_onda, estrella.BCD.Phi, estrella.phio, 0.01, estrella.err_phio, estrella.lohice_phio)
#
# Calculo el modulo de distancia
# Distance modulus
#
            est_dis.Calculo_Dist(estrella.m, estrella.mv, estrella.err_mv, estrella.lohice_mv)
#
#-------------------------------------------------------------------------------
        else:
            print('No se puede calcular lambda_1')
            print('Cannot calculate lambda_1')
#
#-------------------------------------------------------------------------------
    else:
        print('No se puede calcular lambda_1')
        print('Cannot calculate lambda_1')
#-------------------------------------------------------------------------------
# Escribimos los valores de D, lambda_1 y Phi en un archivo
# Write D, lambda_1 and Phi values in a file
#
    BCD.Print_BCD(espectro.nombre, c_o_f, espectro.espec)
#
# Escribimos los parametros fundamentales en un archivo
# Write the fundamental parameters in a file
#
    estrella.Print_ParFun()
#
# Escribimos los parametros de la distancia
# Write the distance parameters in a file
#
    est_dis.Print_Dist(estrella)
################################################################################
