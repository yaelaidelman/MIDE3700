#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
import numpy as np
import math
import scipy.optimize as optimization

class Polinomio:
# Atributos de la clase
    grado= int()
    coef= []
#
#   $P(x)= a_{n} x^{n} + a_{n-1} x^{n-1} + \dots + a_{1} x + a_{0}$
#-------------------------------------------------------------------------------
    def _init_(self):# Genero el polinomio
        self.grado= int()
        self.coef= []
#-------------------------------------------------------------------------------
    
    def print_polynomial(self):
        print("\n\n####--- Polinomio ---####\n\n")
        print(f' -Grado: {self.grado} \n -Coeficiente: {self.coef}\n\n')
    
    def minimos_cuadrados(self, x, y, n):
        # x e y son los puntos a ajustar
        # n es el grado del polinomio
        
#
#  Programa que ajusta un polinomio de grado n por minimos cuadrados
#
#     Sea P(x) = a_0 + a_1 x + ... + a_n x^{n} el polinomio que queremos ajustar
#     y S = sum_{i=0}^{m} {P(x_i) - y_i}^{2} el error del ajuste.
#     Como queremos el ajuste que tenga el minimo error, las derivadas parciales
#     de S con respecto a los coeficientes del polinomio deben ser cero.
#     De este modo armamos n+1 ecuaciones de la forma
#
#     a_0 sum_{i=0}^{m}{x_i^{k}} + a_1 sum_{i=0}^{m}{x_i^{k+1}} + ... +
#     +  a_n sum_{i=0}^{m}{x_i^{k+n}} =  sum_{i=0}^{m}{y_i * x_i^{k}}
#
#     con k = 0, 1, ... , n
#
        ajuste= False
        self.grado= n + 1
        self.coef= np.arange(self.grado).reshape(self.grado)
        self.coef= np.zeros((self.grado))
                
        if len(x) > self.grado:
            A= np.zeros((self.grado, self.grado))
            b= np.zeros((self.grado))
            for k in range(self.grado):
                for j in range(self.grado):
                    for i in x:
                        A[k,j] += math.pow(i, k+j)
                for i in range(len(x)):
                        b[k] += y[i] * math.pow(x[i], k)
#
            sol= np.linalg.solve(A,b)

            for i in range(len(sol)):
                self.coef[i]= sol[n-i]
        
            ajuste= True
#        else:
#            print ("Agregue ", n-len(x)+2, " puntos")
#
        return ajuste
#------------------------------------------------------------------------------
    def Evaluo_pol(self, pol, x0):
        suma= 0.
        n= pol.grado
        for i in range(0,n+1):
            suma += pol.coef[i] * (math.pow(x0, n-i))
        return suma
#-------------------------------------------------------------------------------
    def Print_pol(self, pol):
        n= pol.grado
        y= '%s' %pol.coef[0] + ' * x**' + '%s' %n + ' '
        
        """
        for i in range(1,n):
            if pol.coef[i] < 0.:
                y += '%s' %pol.coef[i] + ' * x**' + '%s' %(n-i) + ' '
            else:
                y += '+' + '%s' %pol.coef[i] + ' * x**' + '%s' %(n-i) + ' '
        
        if pol.coef[n-1] < 0.:
            y += '%s' %pol.coef[n]
        else:
            y += '+' + '%s' %pol.coef[n]
        """
        for i,c in enumerate(pol.coef[1:-1]):
            i= i+1
            if c < 0.:
                y += '%s' %c + ' * x**' + '%s' %(n-i) + ' '
            else:
                y += '+' + '%s' %c + ' * x**' + '%s' %(n-i) + ' '
        
        if n > 1:
            if pol.coef[-1] < 0.:
                y += '%s' %pol.coef[-1]
            else:
                y += '+' + '%s' %pol.coef[-1]

        return y
