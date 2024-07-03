#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
import math
################################################################################
class Distancia():
    # Atributos
    ebv= float()
    mod_dis= float()
    dist= float()
    Rv= float()
    #
    err_ebv= float()
    err_mod_dis= float()
    err_dist= float()
    #
    lohice_ebv= bool()
    lohice_mod_dis= bool()
    lohice_dist= bool()
################################################################################
    def __init__(self):
        #
        self.ebv= float()
        self.mod_dis= float()
        self.dist= float()
        #
        self.err_ebv= float()
        self.err_mod_dis= float()
        self.err_dist= float()
        #
        self.lohice_ebv= bool()
        self.lohice_mod_dis= bool()
        self.lohice_dist= bool()
        #
        self.Rv= 3.1
        #
        return
################################################################################
    def Calculo_EBV(self, l_onda, phi, phio, err_phi, err_phio, lohice):
        #
        if lohice:
#            n= len(l_onda) - 1
            #
            if l_onda == 1: #[4000:4600]
                #
                a = 0.75
                b = -3.0e-4
                #
            elif l_onda == 2: #[4000:4800]
                #
                a = 0.68
                b = -1.9e-4
                #
            else:  #[4000:6700]
                #
                a = 0.54
                b = 3.1e-5
                #
            self.ebv= a * (phi - phio) + b
#
#     Propagamos el error
#
#     Escribo E(B-V) en forma matricial:
#
#     E(B-V) = a * (PHI - PHIo) - b
#
#     ===> E(B-V) = ( a  a ) (PHI - PHIo)^{t}
#
#     La matriz C de varianza-covarianza es igual a una matriz diagonal de 2x2 cuyos
#     elementos de la diagonal son (dPHI)^{2} y (dPHIo)^{2}
#
#     Luego, el error se puede calcular como
#
#     dE(B-V) = SQRT( (a  a) * C * (a  a)^{t} )
#
#             = a * SQRT ( (dPHI)^{2} + (dPHIo)^{2} )
#
            self.err_ebv= a * math.sqrt( err_phi*err_phi + err_phio*err_phio )
            self.lohice_ebv= True
        else:
            self.ebv= -9999.
            self.lohice_ebv= False
################################################################################
    def Calculo_Dist(self, m, mv, err_mv, lohice):
        #
        if lohice and self.lohice_ebv and self.ebv >= 0.:
            #
            self.mod_dis= m - mv - self.Rv * self.ebv
            a= (self.mod_dis + 5.)/5.
            self.dist= math.pow( 10., a )
            #
            #     Propago el error
            #
            e1= err_mv * err_mv
            e2= self.Rv * self.err_ebv
            e2= e2 * e2
            self.err_mod_dis= math.sqrt( e1 + e2 )
            #
            self.err_dist= self.dist * math.log(10.) * self.err_mod_dis / 5.
            #
            self.lohice_mod_dis= True
            self.lohice_dist= True
            #
        else:
            self.mod_dis= 9999999.
            self.dist= 9999999.
            self.lohice_mod_dis= False
            self.lohice_dist= False

################################################################################
    def Print_Dist(self, estrella):
        f= open("Dist.out", "a")
        f.write('{0:20}'.format(estrella.nombre))
        # Escribo Phi y su error
        f.write('  {0:4.2f} 0.01 '.format(estrella.BCD.Phi))
        # Escribo PHIo
        if estrella.lohice_phio:
            if not estrella.extra_phio:
                f.write('  {0:4.2f} {1:4.2f} '.format(estrella.phio, estrella.err_phio))
            else:
                f.write('  {0:4.2f} {1:4.2f}:'.format(estrella.phio, estrella.err_phio))
        else:
            f.write('  **** ****')
        # Escribo E(B-V)
        if self.lohice_ebv:
            f.write('  {0:5.2f} {1:4.2f} '.format(self.ebv, self.err_ebv))
        else:
            f.write('    **** **** ')
        # Escribo magnitud aparente
        if estrella.lohice_m:
            f.write('  {0:5.2f}'.format(estrella.m))
        else:
            f.write('  ****'.format(estrella.m))
        # Escribo Mv
        if estrella.lohice_mv:
            if not estrella.extra_mv:
                f.write('  {0:5.2f} {1:4.2f} '.format(estrella.mv, estrella.err_mv))
            else:
                f.write('  {0:5.2f} {1:4.2f}:'.format(estrella.mv, estrella.err_mv))
        else:
            f.write('   **** **** ')
        # Escribo el modulo de distancia        
        if self.lohice_mod_dis:
            f.write('  {0:5.2f} {1:4.2f} '.format(self.mod_dis, self.err_mod_dis))
        else:
            f.write('  ***** **** ')
        # Escribo la distancia        
        if self.lohice_dist:
            f.write('  {0:6.0f} {1:4.0f} '.format(self.dist, self.err_dist))
        else:
            f.write('  ****** **** ')
        f.write('\n')
        f.close()
        return
#-------------------------------------------------------------------------------
