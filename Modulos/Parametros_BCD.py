#===============================================================================
import os, sys
import math
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import Polinomios
import Algebra
#######################################################################
#######################################################################
#############                FUNCION                     ##############
class Parametros:
    D_total= float
    D_est= float
    d= float
    BD2= bool
    lambda1= float
    Phi= float
#
    paschen= Polinomios.Polinomio()
    balmer= Polinomios.Polinomio()
    balmer_inf= Polinomios.Polinomio()
    xH_inf= []
    balmer_sup= Polinomios.Polinomio()
#
    archivo_out= ""
    nor= bool # Para saber si el espectro esta normalizado
#-------------------------------------------------------------------------------
    def __init__(self, espectro, nor):
#
        self.archivo_out= espectro.archivo_out
        self.nor= nor
#
        if nor:
            self.paschen= espectro.paschen
            self.balmer= espectro.balmer
            self.balmer_inf= espectro.balmer_inf
        else:
            self.paschen= espectro.paschen
            self.balmer= espectro.balmer
            self.balmer_inf= espectro.balmer_inf
            self.xH_inf= espectro.xH_inf
            self.balmer_sup= espectro.balmer_sup
#-------------------------------------------------------------------------------
    def Calculo_D(self):
#
        f_est= open(self.archivo_out, "a") # Archivo de salida
        f_est.write( '\n' )
        f_est.write( 'CALCULO D= D* + d\n' )
        f_est.write( 'CALCULATE D= D* + d\n' )
        f_est.write( '--------------------------------\n' )
        f_est.write( '\n' )
#
        #Muestra los datos del coefciente a evaluar
        # self.balmer_inf.print_polynomial()
        
        if self.nor:
            yp= self.paschen.Evaluo_pol(self.paschen, 1./3700.)
            yb= self.balmer.Evaluo_pol(self.balmer, 1./3700.)
            ybi= self.balmer_inf.Evaluo_pol(self.balmer_inf, 1./3700.)
        else:
            yp= self.paschen.Evaluo_pol(self.paschen, 3700.)
            yb= self.balmer.Evaluo_pol(self.balmer, 3700.)
            ybi= self.balmer_inf.Evaluo_pol(self.balmer_inf, 3700.)
#
        self.D_est= yp - ybi
        self.d= ybi - yb
        self.D_total= self.D_est + self.d
#
        f_est.write( 'D= ' + '%1.2f' % self.D_total + '\n')
        
        # print('D* = {} = {} - {}\n\n     d = {} = {} - {}\n\n      D_total = {} = {} + {}'.format(
        #     self.D_est, yp, ybi,
        #     self.d, ybi, yb,
        #     self.D_total, self.D_est, self.d
        # ))
#
# El error de medicion es 0.02
#
        if abs(self.D_total - self.D_est) <= 0.02:# no existe un segundo salto
            self.d= 0.
            self.D_total= self.D_est
            self.BD2= False
#
            f_est.write( 'La estrella no presenta un segundo salto\n' )
            f_est.write( 'The star does not present a second jump\n' )
#
        else:
            self.BD2= True
#
            f_est.write( 'D*= ' + '%1.2f' % self.D_est + '\n')
            f_est.write( 'd= ' + '%1.2f' % self.d + '\n')
#
        f_est.close()
        return
#-------------------------------------------------------------------------------
    def Calculo_lambda1(self):
#
        f_est= open(self.archivo_out, "a") # Archivo de salida
        f_est.write( '\n' )
        f_est.write( 'CALCULO LAMBDA_1\n' )
        f_est.write( 'CALCULATE LAMBDA_1\n' )
        f_est.write( '--------------------------------\n' )
        f_est.write( '\n' )
#
# Calculo la coordenada x del punto de interseccion entre la envolvente
# superior de las lineas de balmer y una recta paralela al continuo de
# Paschen que pasa por el punto (3700., D/2)
#
# La recta paralela al continuo de Paschen es igual a:
#
        Pp= Polinomios.Polinomio()
        Pp.grado= 1
        Pp.coef= [0., 0.]
        Pp.coef[0]= self.paschen.coef[0]
#
        ybi= self.balmer_inf.Evaluo_pol(self.balmer_inf, 3700.)
        Pp.coef[1] =  ybi + self.D_est/2.0 - self.paschen.coef[0] * 3700.
#
# El punto de interseccion sera
#
        x1, x2, sol= Algebra.Interseccion(Pp, self.balmer_sup)
#
        if sol:
            if x2 >= x1:
                if x1 > 3700.:
                    x0= x1
                else:
                    x0= x2
            else:
                if x2 > 3700.:
                    x0= x2
                else:
                    x0= x1
#
#     El valor de LAMBDA_1 lo vamos a calcular en el plano Log(F) Vs. cm.
#     La conversion de angstroms a centimetros hay que hacerla de la siguiente
#     forma: cuando imprimo en papel el espectro Log(F) Vs. Lambda tenemos que
#     200 Ang equivalen a 3.2 cm (mediendo con una regla sobre el papel).
#     Entonces lo que hace el programa es pasar de Ang a cm haciendo un cambio
#     de escala.
#
#     Entonces si tomamos el cero de la escala en cm en 3700 Angs, tenemos una
#     transformacion lineal de la forma 
#
#     X[cm] = a * X[Angs] + b
#
#     que pasa por los puntos
#
#     (3700,0) y (3900,3.2)
#
#     de este modo encontramos que
#
#     a = 2./125.     y        b = -296./5.
#     
#     entonces
#
#     lambda_cm = (2./125.) * lambda_A - (296./5.)
#
#     En este plano tenemos que calcular la distancia de las lineas de Balmer
#     a la recta Lambda = 3700.
#     A estas distancias las llamaremos x_cm(i).
#
#     Las longitudes de onda en reposo son
#
            w= []
            w.append( 3750.154 )    #H_kappa
            w.append( 3770.632 )    #H_iota
            w.append( 3797.900 )    #H_theta
            w.append( 3835.386 )    #H_gamma
            w.append( 3889.051 )    #H_delta
            w.append( 3970.074 )    #H_epsilon
#
#     Contruyo el vector x_cm
#
            aux= np.zeros( (len(self.xH_inf)) )
            ind= []
            for i in range( len(self.xH_inf) ):
                aux[i]= self.xH_inf[i]
            for i in w:
                ind.append( np.argmin( np.absolute(aux - i) ) )
            x_cm= []
            for i in ind:
                x_cm.append( (2.0/125.0) * self.xH_inf[i] - (296.0/5.0) )
#
#     x0 es la distancia entre lambda=3700 y la interseccion entre la envolvente
#     superior de las lineas de Balmer con la recta paralela al continuo de 
#     Paschen pero que pasa por el punto (3700, yB+D/2).
#     x0 tambien se mide en centimetros
#
            x0_cm= (2.0/125.0) * x0 - (296.0/5.0)
#
#     Luego, con los valores de x0_cm, x_cm(i) hacemos correlacionar
#     las longitudes en centimetros de las lineas con sus las longitudes
#     de onda en reposo en angstroms.
#
#     Ajustamos una recta por minimos cuadrados para encontrar la correlacion
#
            cw= Polinomios.Polinomio()
            ajuste= cw.minimos_cuadrados(x_cm, w, 1)
            if ajuste:
                self.lambda1 = cw.coef[0] * x0_cm + cw.coef[1] - 3700.0
                f_est.write( 'lambda_1= ' + '%3i' % self.lambda1 + '\n')
                if self.lambda1 > 0.:
                    lambda_ok= True
                else:
                    lambda_ok= False
            else:
                print( '######  ERROR  #######')
                print( 'NO SE PUEDE CALCULAR $\lambda_{1}$')
                print( 'CANNOT CALCULATE $\lambda_{1}$')
                f_est.write( '######  ERROR  #######' )
                f_est.write( 'NO SE PUEDE CALCULAR $\lambda_{1}$' )
                f_est.write( 'CANNOT CALCULATE $\lambda_{1}$' )
                lambda_ok= False
                self.lambda1= -999.
#
        else:
            print( '######  ERROR  #######')
            print( 'LA ENVOLVENTE SUPERIOR Y LA PARALELA AL CONTINUO DE PASCHEN NO SE INTERSECAN')
            print( 'THE UPPER ENVELOPE AND THE PARALLEL TO THE PASCHEN CONTINUOUS DO NOT INTERSECT' )
            print( 'NO SE PUEDE CALCULAR $\lambda_{1}$')
            print( 'CANNOT CALCULATE $\lambda_{1}$')
            print( '######################')
            f_est.write( '######  ERROR  #######' )
            f_est.write( 'LA ENVOLVENTE SUPERIOR Y LA PARALELA AL CONTINUO DE PASCHEN NO SE INTERSECAN' )
            f_est.write( 'THE UPPER ENVELOPE AND THE PARALLEL TO THE PASCHEN CONTINUOUS DO NOT INTERSECT' )
            f_est.write( 'NO SE PUEDE CALCULAR $\lambda_{1}$' )
            f_est.write( 'CANNOT CALCULATE $\lambda_{1}$' )
            f_est.write( '######################' )
            lambda_ok= False
            self.lambda1= -999.
#
        f_est.close()
        return lambda_ok
#-------------------------------------------------------------------------------
    def Calculo_Phi(self, l):
#
        f_est= open(self.archivo_out, "a") # Archivo de salida
        f_est.write( '\n' )
        f_est.write( 'CALCULO EL GRADIENTE DE COLOR\n' )
        f_est.write( 'CALCULATE THE COLOR GRADIENT\n' )
        f_est.write( '--------------------------------\n' )
        f_est.write( '\n' )
#
        L1= 4000.
        l_max= max(l)
        if 4700. < l_max:
            if 4900. < l_max:
                if 6800. < l_max:
                    L2= 6700.
                else:
                    L2= 4800.
            else:
                L2= 4600.
        else:
            L2= 4600.
#
        ln_L1= math.log(L1)
        ln_L2= math.log(L2)
        ln_F1= self.paschen.Evaluo_pol(self.paschen, L1) * math.log(10.)
        ln_F2= self.paschen.Evaluo_pol(self.paschen, L2) * math.log(10.)
#
        num= 5. * (ln_L2 - ln_L1) + ln_F2 - ln_F1
        den= ( (1./L1) - (1./L2) ) * 10.**4 # paso a micrones
#
        self.Phi= num / den
        f_est.write( 'Phi= ' + '%1.2f' % self.Phi + '\n')
        f_est.close()
        return
#-------------------------------------------------------------------------------
    def Print_BCD(self, nombre, c_o_f, espec):
        f= open("BCD.out", "a")
        f.write('{0:20}'.format(nombre))
        if self.D_est >= 0.:
            f.write('  {0:4.2f}'.format(self.D_total))
            f.write('  {0:4.2f}'.format(self.D_est))
        else:
            f.write('  ****')
            f.write('  ****')
        f.write('   {0:5.2f}'.format(self.d))
        if self.lambda1 >= 0.:
            f.write('    {0:3d}'.format(int(self.lambda1)))
        else:
            f.write('    ***')
        f.write('   {0:4.2f}'.format(self.Phi))
        f.write('   {0:1s}'.format(c_o_f))
        f.write('     {0:1d}'.format(espec))
        f.write('\n')
        f.close()
        return
#-------------------------------------------------------------------------------
