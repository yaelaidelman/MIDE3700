#===============================================================================
import os, sys
import math
import matplotlib.pyplot as plt
from pylab import *
import Parametros_BCD
import Curvas
import Landolt
import Algebra
#######################################################################
#######################################################################
#############                FUNCION                     ##############
class Parametros:
    def __init__(self, bcd, cof, nom):
        self.BCD= bcd
        self.c_o_f= cof
        self.nombre= nom
        self.teff= int()
        self.te= str()
        self.ties= int()# numero natural asignado al tipo espectral
        self.cl= str()
        self.logg= float()
        self.mv= float()
        self.mbol= float()
        self.phio= float()
        self.m= float()
#
        self.err_teff= int()
        self.err_logg= float()
        self.err_mv= float()
        self.err_mbol= float()
        self.err_phio= float()
#
        self.extra_teff= False
        self.lohice_teff= False
        self.extra_te= False
        self.lohice_te= False
        self.extra_cl= False
        self.lohice_cl= False
        self.extra_logg= False
        self.lohice_logg= False
        self.extra_mv= False
        self.lohice_mv= False
        self.extra_mbol= False
        self.lohice_mbol= False
        self.extra_phio= False
        self.lohice_phio= False
        self.lohice_m= False
#-------------------------------------------------------------------------------
    def Calculo_teff(self, curvas, curvas_te_f, curvas_cl_f, landolt, n):
#
# n= 1 es para calcular la temperatura y construir el cuerpo negro
# n= 2 es la medida final de Teff para la estrella con su error
#
        if n == 1:
            if self.c_o_f == 'c':# para estrellas calientes
                # print(f"\n\n\n#################### para interpolar, estos parametros {self.BCD.D_est, self.BCD.lambda1}")
                  
                
                self.lohice_teff, temp, self.extra_teff= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)
#
            else:# para estrellas frias
                self.Calculo_te(curvas_te_f)
                self.Calculo_cl(curvas_cl_f)
                self.lohice_teff, temp, self.extra_teff= landolt.Calculo_teff(self.ties, self.cl)
#
            self.teff= Algebra.Redondeo_int_mas_cerca( temp )
#
        else:# n == 2
            if self.c_o_f == 'c':# para estrellas calientes
                self.lohice_teff, temp, self.extra_teff= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)
#
            else:# para estrellas frias
                self.lohice_teff, temp, self.extra_teff= landolt.Calculo_teff(self.ties, self.cl)
#
#
            self.teff= Algebra.Redondeo_int_mas_cerca( temp )
#
            if self.lohice_teff:
                if self.c_o_f == 'c':
                    err= curvas.Error(self.BCD.D_est, self.BCD.lambda1, self.teff)
                else:
                    err= landolt.Error(self.ties, self.cl, "teff", self.teff)

                self.err_teff= Algebra.Redondeo_int_mas_cerca( err )
#
        return
#-------------------------------------------------------------------------------
    def Calculo_te(self, curvas):
#
        self.lohice_te, ties, self.extra_te= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)
#
        n= Algebra.Redondeo_int_mas_cerca( ties )
#
# n= 10x + y
#
        y= n % 10# resto de n dividido 10 ==> da el subtipo espectral
        x= (n - y) / 10# da el tipo espectral
#
        if x == 0:# tipo espectral O
            self.te= "O"
        elif x == 1:# tipo espectral B
            self.te= "B"
        elif x == 2:# tipo espectral A
            self.te= "A"
        elif x == 3:# tipo espectral F
            self.te= "F"
        elif x == 4:# tipo espectral G
            self.te= "G"
        elif x == 5:# tipo espectral K
            self.te= "K"
        elif x == 6:# tipo espectral M
            self.te= "M"
#
        self.te= self.te + str(y)
        self.ties= x * 10 + y
#
        return
#-------------------------------------------------------------------------------
    def Calculo_cl(self, curvas):
#
        self.lohice_cl, cl, self.extra_cl= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)
#
        if cl <= 1.:# clase de luminosidad Ia
            self.cl= "Ia"
        elif 1. < cl and cl <= 2.:# clase de luminosidad Ib
            self.cl= "Ib"
        elif 2. < cl and cl <= 3.:# clase de luminosidad II
            self.cl= "II"
        elif 3. < cl and cl <= 4.:# clase de luminosidad III
            self.cl= "III"
        elif 4. < cl and cl <= 5.:# clase de luminosidad IV
            self.cl= "IV"
        elif 5. < cl and cl <= 6.:# clase de luminosidad V
            self.cl= "V"
        elif 6. < cl:# clase de luminosidad VI
            self.cl= "VI"
#
        return
#-------------------------------------------------------------------------------
    def Calculo_logg(self, curvas, landolt):
#
        if self.c_o_f == 'c':# para estrellas calientes
            self.lohice_logg, self.logg, self.extra_logg= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)
#
        else:# para estrellas frias
            self.lohice_logg, self.logg, self.extra_logg= landolt.Calculo_logg(self.ties, self.cl)
#
        if self.lohice_logg:
            if self.c_o_f == 'c':
                self.err_logg= curvas.Error(self.BCD.D_est, self.BCD.lambda1, self.logg)
            else:
                self.err_logg= landolt.Error(self.ties, self.cl, "logg", self.logg)
#
        return
#-------------------------------------------------------------------------------
    def Calculo_mv(self, curvas, landolt):
#
        if self.c_o_f == 'c':# para estrellas calientes
            self.lohice_mv, self.mv, self.extra_mv= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)
#
        else:# para estrellas frias
            self.lohice_mv, self.mv, self.extra_mv= landolt.Calculo_mv(self.ties, self.cl)
#
        if self.lohice_mv:
            if self.c_o_f == 'c':
                self.err_mv= curvas.Error(self.BCD.D_est, self.BCD.lambda1, self.mv)
            else:
                self.err_mv= landolt.Error(self.ties, self.cl, "mv", self.mv)
        
        return
#-------------------------------------------------------------------------------
    def Calculo_mbol(self, curvas, landolt):
#
        if self.c_o_f == 'c':# para estrellas calientes
            self.lohice_mbol, self.mbol, self.extra_mbol= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)
#
        else:# para estrellas frias
            self.lohice_mbol, self.mbol, self.extra_mbol= landolt.Calculo_mbol(self.ties, self.cl)
#
        if self.lohice_mbol:
            if self.c_o_f == 'c':
                self.err_mbol= curvas.Error(self.BCD.D_est, self.BCD.lambda1, self.mbol)
            else:
                self.err_mbol= landolt.Error(self.ties, self.cl, "mbol", self.mbol)
#
        return
#-------------------------------------------------------------------------------
    def Calculo_phio(self, curvas):
#
        self.lohice_phio, self.phio, self.extra_phio= curvas.Interpolo(self.BCD.D_est, self.BCD.lambda1)

        if self.lohice_phio:
            self.err_phio= curvas.Error(self.BCD.D_est, self.BCD.lambda1, self.phio)
#
        return
#-------------------------------------------------------------------------------
    def Print_ParFun(self):
        f= open("ParFun.out", "a")
        f.write('{0:20}'.format(self.nombre))
#
# Escribo D y lambda_1
#
        if self.BCD.D_est >= 0.:
            f.write('  {0:4.2f}'.format(self.BCD.D_est))
        else:
            f.write('  ****')
#
        if self.BCD.lambda1 >= 0.:
            f.write('  {0:3.0f}'.format(self.BCD.lambda1))
        else:
            f.write('  ***')
#
# Escribo el tipo espectral
#
        if self.lohice_te:
            if not self.extra_te:
                f.write('     {0:2s} '.format(self.te))
            else:
                f.write('     {0:2s}:'.format(self.te))
        else:
            f.write('     ** ')
#
# Escribo la clase de luminosidad
#
        if self.lohice_cl:
            if not self.extra_cl:
                f.write(' {0:>3s} '.format(self.cl))
            else:
                f.write(' {0:>3s}:'.format(self.cl))
        else:
            f.write(' *** ')
#
# Escribo Teff
#
        if self.lohice_teff:
            if not self.extra_teff:
                f.write('  {0:5d} {1:5d} '.format(self.teff, self.err_teff))
            else:
                f.write('  {0:5d} {1:5d}:'.format(self.teff, self.err_teff))
        else:
            f.write('  ***** ***** ')
#
# Escribo Logg
#
        if self.lohice_logg:
            if not self.extra_logg:
                f.write('  {0:4.2f} {1:4.2f} '.format(self.logg, self.err_logg))
            else:
                f.write('  {0:4.2f} {1:4.2f}:'.format(self.logg, self.err_logg))
        else:
            f.write('  **** **** ')
#
# Escribo Mv
#
        if self.lohice_mv:
            if not self.extra_mv:
                f.write('  {0:5.2f} {1:4.2f} '.format(self.mv, self.err_mv))
            else:
                f.write('  {0:5.2f} {1:4.2f}:'.format(self.mv, self.err_mv))
        else:
            f.write('  ***** **** ')
#
# Escribo Mbol
#
        if self.lohice_mbol:
            if not self.extra_mbol:
                f.write('  {0:5.2f} {1:4.2f} '.format(self.mbol, self.err_mbol))
            else:
                f.write('  {0:5.2f} {1:4.2f}:'.format(self.mbol, self.err_mbol))
        else:
            f.write('  ***** **** ')
#
# Escribo PHIo
#
        if self.lohice_phio:
            if not self.extra_phio:
                f.write('  {0:4.2f} {1:4.2f} '.format(self.phio, self.err_phio))
            else:
                f.write('  {0:4.2f} {1:4.2f}:'.format(self.phio, self.err_phio))
        else:
            f.write('  **** **** ')
#
        f.write('\n')
        f.close()
        return
#-------------------------------------------------------------------------------
