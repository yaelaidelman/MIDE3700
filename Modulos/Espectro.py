#!/usr/local/bin/python
#===============================================================================
# Funcion que grafica el espectro de una estrella.
# El archivo debe ser ASCII de dos columnas:
# longitud de onda Versus flujo
#===============================================================================
import os, sys
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from pylab import *
from PIL import Image
import Polinomios
import Algebra
import Inter_Grafica
#import Despliega_ventana
import copy
from Modulos.Funciones_auxiliares import maximizar_pantalla
from Modulos.Punto import Punto


#######################################################################
#######################################################################
#############                CLASE                       ##############
class Espectro:
# Atributos: Nombre, longitud de onda y flujo
    nombre= ""
    archivo_out= ""
    l_onda= []
    flujo= []
    log_flujo = []
    espec= int()
    paschen= Polinomios.Polinomio()
    balmer= Polinomios.Polinomio()
    balmer_inf= Polinomios.Polinomio()
    balmer_sup= Polinomios.Polinomio()
    xP= []  #  puntos x del ajuste de Pashen
    xB= []
    xB_inf= []
    xH_inf= []
    yH_inf= []
    xH_sup= []
    yH_sup= []
    
    
#-------------------------------------------------------------------------------
    def __init__(self, nombre):# Genero el espectro
#
        # Manejo los datos del gráfico
        self.axes = None
        self.figure = None
        
# Inicializo los valores
        self.l_onda= []
        self.flujo= []
        self.log_flujo = []
        self.espec= int()
        self.paschen= Polinomios.Polinomio()
        self.balmer= Polinomios.Polinomio()
        self.balmer_inf= Polinomios.Polinomio()
        self.balmer_sup= Polinomios.Polinomio()
        self.paschen.grado= 1
        self.balmer.grado= 1
        self.balmer_inf.grado= 2
        self.balmer_sup.grado= 2
        self.xP= []
        self.xB= []
        self.xB_inf= []
        self.xH_inf= []
        self.yH_inf= []
        self.xH_sup= []
        self.yH_sup= []
        
        # Initialize a list to store the button instances
        self.lines = []
        self.line_buttons = []
        
        # Initialize a list to store the button instances
        self.parables = []
        self.parable_buttons = []
#
        n= len(nombre)
        if nombre[n-1:n] == '\n':
            self.nombre= nombre[0:n-1]
        else:
            self.nombre= nombre[0:n]
        self.archivo_out= "Ajustes/" + self.nombre + ".out"
#
        return
#-----------------------------------------------------------------------------------------
    def Leo_archivo(self):
#
# archivo es de la forma Estrellas/nombre.dat
        archivo= 'Estrellas/' + self.nombre + '.dat'
#        n= len(archivo) # cantidad de caracteres
#        self.nombre= archivo[10:n-4] # los ultimos 4 caracteres son '.dat'
#
        file_in= open(archivo, 'r') # Abro el archivo de lectura
        linea= file_in.readline()
#
    # Leemeos el archivo
        while linea != "": # Lee linea por linea hasta el final del archivo
# Como las columnas estan separadas por espacios guardamos las columnas
# en una lista
            columna= linea.split("  ")
            self.l_onda.append( float(columna[0]) )# Primera columna del archivo
            self.flujo.append( float(columna[1]) )# Segunda columna del archivo
            linea= file_in.readline()# leemos la siguiente linea del archivo
#
        file_in.close()
        n= len( self.l_onda ) - 1
        if self.l_onda[n] <= 4800.:
            self.espec= 1
        elif 4800. < self.l_onda[n] and self.l_onda[n] <= 6700.:
            self.espec= 2
        else:
            self.espec= 3
        return
        
#-------------------------------------------------------------------------------
    def Grafico_espec(self, n, puntos = None):
#
        # n= 1  Grafico el espectro
        # n= 2  Grafico el espectro y Paschen
        # n= 3  Grafico el espectro, Paschen, Balmer y Balmer inf
        # n= 4  Grafico el espectro, Paschen, Balmer, Balmer inf y Balmer sup
#
        self.log_flujo= []
        for i in self.flujo:
            self.log_flujo.append( math.log(i,10) )
            
    # Graficamos el espectro
    
    # Utiliza los atributos axes y figure
        self.axes.set_xlabel('$\lambda$ [$\AA$]')
        self.axes.set_ylabel('$\log (F_{\lambda})$')
        self.axes.axvline(x=3700., color='k')
        self.axes.plot(self.l_onda, self.log_flujo, 'b-')

#
# Grafico los ajustes realizados hasta el momento
        if n >= 2:
            yp= poly1d(self.paschen.coef); yp
            xp= []
            for i in self.l_onda:
                if i > 3700.:
                    xp.append( i )
            self.axes.plot(xp, polyval(yp, xp), 'g-')  # Grafico Paschen
#
            if n >= 3:
                yb= poly1d(self.balmer.coef); yb
                xb = [i for i in self.l_onda if i < 3700.]
        
                # Utilizo self.axes en lugar de plt
                self.axes.plot(xb, polyval(yb, xb), 'g-')  # Grafico Balmer
        
                if n == 3:
                    # Plotear los puntos y almacenarlos en la lista
                    for x, y in zip(self.xH_inf, self.yH_inf):
                        punto, = self.axes.plot(x, y, 'ro')
                        new_point = punto                        
                        puntos.append(Punto(x, y, new_point))

                    # Utilizo self.axes.set_title en lugar de plt.title
                    self.axes.set_title(self.nombre + '\n' + 'Ajuste la envolvente inferior\n' + 'Fit the bottom envelope of Balmer lines')

                if n == 4:# Grafico Balmer superior
                    
                    ybi= poly1d(self.balmer_inf.coef); ybi
                    xv= -self.balmer_inf.coef[1] / (2. * self.balmer_inf.coef[0])
                    xbi= []
                    if xv > 3755.:
                        for i in self.l_onda:
                            if 3700. <= i and i <= min(3850.,xv):
                                xbi.append( i )
                    else:
                        for i in self.l_onda:
                            if 3700. <= i and i <= 3800.:
                                xbi.append( i )
                                
                    self.axes.plot(xbi, polyval(ybi, xbi), 'g-')
                    
                    #Dibujo los puntos
                    for x, y in zip(self.xH_sup, self.yH_sup):
                        punto, = self.axes.plot(x, y, 'ro')
                        new_point = punto
                        puntos.append(Punto(x, y, new_point))
                                        
                    self.axes.set_title(self.nombre + '\n' + 'Ajuste la envolvente superior\n' + 'Fit the upper envelope of Balmer lines')                    
            else:
                self.axes.set_title(self.nombre + '\n' + 'Ajuste el continuo de Balmer\n' + 'Fit the Balmer continuum')
        else:
            self.axes.set_title(self.nombre + '\n' + 'Ajuste el continuo de Paschen\n' + 'Fit the Paschen continuum')

        plt.show()

#-------------------------------------------------------------------------------
    def Guardo_ajuste(self, BCD, n):
#
# Recta paralela al continuo de Paschen
#
        Pp= Polinomios.Polinomio()
        Pp.grado= 1
        Pp.coef= [0., 0.]
        Pp.coef[0]= self.paschen.coef[0]
#
        ybi= self.balmer_inf.Evaluo_pol(self.balmer_inf, 3700.)
        Pp.coef[1] =  ybi + BCD.D_est/2.0 - self.paschen.coef[0] * 3700.
#
# Genero los polinomios
#
        yp= poly1d(self.paschen.coef); yp
        yb= poly1d(self.balmer.coef); yb
        ybi= poly1d(self.balmer_inf.coef); ybi
        ybs= poly1d(self.balmer_sup.coef); ybs
        ypp= poly1d(Pp.coef); ypp
#
        xp= []
        xb= []
        xbi= []
        xbs= []
#
# La envolvente superior la voy a graficar hasta el x minimo entre la interseccion entre la recta del continuo de Paschen y la parabola de la envolvente superior, y el maximo de la envolvente superior.
#
        x1, x2, sol= Algebra.Interseccion(self.paschen, self.balmer_sup)
        xv= -self.balmer_sup.coef[1] / (2. * self.balmer_sup.coef[0])
        if sol:
            if self.balmer_sup.coef[0] < 0.:
                if x2 >= x1:
                    if x1 > 3755.:
                        min_bs= x1
                    elif xv > 3755.:
                        min_bs= min(3850.,xv)
                    elif x2 > 3755.:
                        min_bs= min(3850.,x2)
                    else:
                        min_bs= 3850.
                else:
                    if x2 > 3755.:
                        min_bs= x2
                    elif xv > 3755.:
                        min_bs= min(3850.,xv)
                    elif x1 > 3755.:
                        min_bs= min(3850.,x1)
                    else:
                        min_bs= 3850.
            else:
                if x2 >= x1:
                    min_bs= min(3850.,x2)
                else:
                    min_bs= min(3850.,x1)
        else:
            if xv > 3755.:
                min_bs= xv
            else:
                min_bs= 3850.
#
# Graficamos la envolvente inferior
#
        xv= -self.balmer_inf.coef[1] / (2. * self.balmer_inf.coef[0])
        if xv > 3755.:
            min_bi= min(3850.,xv)
        else:
            min_bi= 3850.
#
        for i in self.l_onda:
            if i >= 3700.:
                xp.append( i )
                if i <= min_bi:
                    xbi.append( i )
                if i <= min_bs:
                    xbs.append( i )
            else:
                xb.append( i )
#
        log_flujo= []
        for i in self.flujo:
            log_flujo.append( math.log(i,10) )
#
    # Graficamos el espectro
#
        plt.title(self.nombre)
#
        if BCD.D_est > 0.:
            plt.figtext(0.75, 0.85, 'D= %1.2f'%(BCD.D_total))
        else:
            plt.figtext(0.75, 0.85, 'D= ***')
#
        if BCD.lambda1 > 0.:
            plt.figtext(0.75, 0.80, '$\lambda_{1}$= %3i'%(BCD.lambda1))
        else:
            plt.figtext(0.75, 0.80, '$\lambda_{1}$= ***')
#
        if BCD.BD2:
            if BCD.D_est > 0.:
                plt.figtext(0.75, 0.75, 'D*= %1.2f'%(BCD.D_est))
            else:
                plt.figtext(0.75, 0.75, 'D*= ***')
            plt.figtext(0.75, 0.70, 'd= %1.2f'%(BCD.d))
            if n == 3:
                plt.figtext(0.75, 0.65, '$\Phi$= %1.2f'%(BCD.Phi))
        elif n == 3:
            plt.figtext(0.75, 0.75, '$\Phi$= %1.2f'%(BCD.Phi))
#
        if n == 1:
            f_ajuste= 'Ajustes/' + self.nombre + '.1' + '.png'# Nombre del archivo
        else:
            f_ajuste= 'Ajustes/' + self.nombre + '.3' + '.png'# Nombre del archivo
#
        # input("Imprimiendo...")
        plt.xlabel('$\lambda$ [$\AA$]')
        plt.ylabel('$\log (F_{\lambda})$')
        plt.plot(self.l_onda, log_flujo, 'b-')
        plt.plot(xp, polyval(yp,xp), 'g-')
        plt.plot(xp, polyval(ypp,xp), 'g--')
        plt.plot(xb, polyval(yb,xb), 'g-')
        plt.plot(xbi, polyval(ybi,xbi), 'g-')
        plt.plot(xbs, polyval(ybs,xbs), 'g-')
        plt.axvline(x=3700., color='k')
        plt.savefig(f_ajuste)
        plt.clf()
        # input("Fin de impresion...")
#
        if n == 1:
#
# Abro el archivo donde gurde el ajuste
#
            # f_png= Image.open(f_ajuste).show()
#
# Despliego la ventana
#
            #c_o_f= Despliega_ventana.Despliega_ventana()
            texto= input('La estrella es mas fria que A2? \n Is the star colder than a spectral type A2? (Yes/No): [no] ') or "n"
            #if texto == 'Si' or texto == 'si':
            if texto.lower()[0] == 'y':
                c_o_f= 'f'
            #elif texto == 'No' or texto == 'no':
            elif texto.lower()[0] == 'n':
                c_o_f= 'c'            
#
# Cierro la ventana desplegada del ajuste
#
            return c_o_f
        else:
            return
#-------------------------------------------------------------------------------
    def Ajuste_Paschen(self):
#
        
        f_est= open(self.archivo_out, "w") # Archivo de salida
        f_est.write( '\n' )
        f_est.write( 'AJUSTE DEL CONTINUO DE PASCHEN\n' )
        f_est.write( 'FIT OF THE PASCHEN CONTINUUM\n' )
        f_est.write( '------------------------------\n' )
        f_est.write( '\n' )
        f_est.close()
        self.figure, self.axes= plt.subplots()
#

        ajuste= Inter_Grafica.Inter_Grafica(self.archivo_out, False, self)
        ajuste.clean_puntos()
        maximizar_pantalla()
        
        self.figure.canvas.mpl_connect('button_press_event', ajuste.click)
        self.figure.canvas.mpl_connect('key_press_event', ajuste.handler_of_key_rect)
        
        self.Grafico_espec(1)
        
        if ajuste.get_cant_lines() > 0:
            self.graficar_ajuste_pashen_activa(ajuste.p)
            self.parable_buttons = []
        else:
            raise Exception("No se graficaron lineas")
#
        return
#-------------------------------------------------------------------------------
    def  Ajuste_Balmer(self):
#
        
        f_est= open(self.archivo_out, "a") # Archivo de salida
        f_est.write( '\n' )
        f_est.write( 'AJUSTE DEL CONTINUO DE BALMER\n' )
        f_est.write( 'FIT OF THE BALMER CONTINUUM\n' )
        f_est.write( '------------------------------\n' )
        f_est.write( '\n' )
        f_est.close()
        
        #Configuración para Widgets
        self.line_buttons = []
        
        self.figure, self.axes= plt.subplots()
#
        ajuste= Inter_Grafica.Inter_Grafica(self.archivo_out, False, self)
        ajuste.clean_puntos()
        
        maximizar_pantalla()
        
        self.figure.canvas.mpl_connect('button_press_event', ajuste.click)
        self.figure.canvas.mpl_connect('key_press_event', ajuste.handler_of_key_rect)
        
        self.Grafico_espec(2)
        
        if ajuste.get_cant_lines() > 0:
            self.graficar_ajuste_balmer_activa(ajuste.p)
            self.parable_buttons = []
        else:
            raise Exception("No se graficaron lineas")
        
        self.graficar_ajuste_balmer_activa(ajuste.p)

#
        return
#-------------------------------------------------------------------------------
    def Ajuste_Balmer_inf(self):
#
        f_est= open(self.archivo_out, "a") # Archivo de salida
        f_est.write( '\n' )
        f_est.write( 'AJUSTE DE LA ENVOLVENTE INFERIOR\n' )
        f_est.write( 'FIT OF THE BOTTOM ENVELOPE\n' )
        f_est.write( '------------------------------\n' )
        f_est.write( '\n' )
        f_est.close()

        self.figure, self.axes= plt.subplots()
#
        ajuste= Inter_Grafica.Inter_Grafica(self.archivo_out, False, self)
        ajuste.clean_puntos()
        
        maximizar_pantalla()
#
        x_min, y_min= Algebra.Busco_minimos(self.l_onda, self.flujo)
        self.xH_inf, self.yH_inf= Algebra.Busco_lineas_balmer(x_min, y_min)
##
        
        ajuste.xdatalist= copy.copy(self.xH_inf)
        ajuste.ydatalist= copy.copy(self.yH_inf)
##

        self.figure.canvas.mpl_connect('button_press_event', ajuste.click)
        self.figure.canvas.mpl_connect('key_press_event', ajuste.handler_of_key_parable)

        self.Grafico_espec(3, ajuste.points)
                
        self.graficar_balmer_inferior_activa(ajuste.p)
        
        self.clean_parables()
                
        
#
        return
#-------------------------------------------------------------------------------

    def clean_parables(self):
        self.parables = []
        return
    
    def Ajuste_Balmer_sup(self):
#
        f_est= open(self.archivo_out, "a") # Archivo de salida
        f_est.write( '\n' )
        f_est.write( 'AJUSTE DE LA ENVOLVENTE SUPERIOR\n' )
        f_est.write( 'FIT OF THE UPPER ENVELOPE\n' )
        f_est.write( '--------------------------------\n' )
        f_est.write( '\n' )
        f_est.close()
#
        self.parable_buttons = []

        self.figure, self.axes= plt.subplots()
#
        
        ajuste= Inter_Grafica.Inter_Grafica(self.archivo_out, False, self)
                
        ajuste.clean_puntos()
        
        maximizar_pantalla()
        x_max, y_max= Algebra.Busco_maximos(self.l_onda, self.flujo)
#
# Cargo los datos calculados
#
        ajuste.xdatalist= x_max
        self.xH_sup= x_max
        log_y_max= []
        for i in y_max:
            log_y_max.append( math.log(i, 10) )
        ajuste.ydatalist= log_y_max
        self.yH_sup= log_y_max
#
        self.figure.canvas.mpl_connect('button_press_event', ajuste.click)
        self.figure.canvas.mpl_connect('key_press_event', ajuste.handler_of_key_parable)
        
        self.Grafico_espec(4, ajuste.points)
        
        self.graficar_balmer_superior_activa(ajuste.p)
        
        self.clean_parables()
        
        # self.balmer_sup.coef= ajuste.p.coef
    
#
        return
    
    
#-------------------------------------------------------------------------------

    def create_parable_button(self, ax, label, parables, parable):
        """
        Create a toggle button for a given parable on the plot.

        Parameters:
        - ax (matplotlib.axes._axes.Axes): The Axes on which the button will be added.
        - label (str): The label/text for the button.
        - line (matplotlib.lines.Line2D): The line associated with the button.

        Returns:
        - None
        """
        
        self.colorear_botones(self.get_parable_buttons(), "grey")
        
        self.parables = parables
        button_ax = plt.axes([0.91, 0.9 - len(self.parable_buttons) * 0.1, 0.08, 0.05])
        parable_button = Button(button_ax, label+" "+str(len(self.parable_buttons)+1), color="green")
        parable_button.on_clicked(lambda event, l=parable, b = parable_button: self.toggle_parable(l, b))
        ax.figure.canvas.mpl_connect('pick_event', parable_button)
        self.parable_buttons.append(parable_button)

    def toggle_parable(self, parable, button):
        """
        Esta función se encarga de manejar la funcionalidad de la linea cuando se presiona el botón:
        Pinta todos los demás botones de gris y deja este del color verde.

        Parameters:
        - line (matplotlib.lines.Line2D): The line to be toggled.
        """
        for p in self.parables:
            if p != parable:
                p.grafico.set_color("grey")
                p.set_last(False)
                
        for b in self.get_parable_buttons():
            if b != button:
                b.color="gray"
            else:
               b.color = 'green'
                
        parable.grafico.set_color(parable.get_color_original())
        parable.set_last(True)
        plt.draw()
        
#-------------------------------------------------------------------------------
    def colorear_botones(self, botones, color):
        for b in botones:
            b.color =color
            
    def create_line_button(self, ax, label, lines, line):
        """
        Create a toggle button for a given line on the plot.

        Parameters:
        - ax (matplotlib.axes._axes.Axes): The Axes on which the button will be added.
        - label (str): The label/text for the button.
        - line (matplotlib.lines.Line2D): The line associated with the button.

        Returns:
        - None
        """
        self.colorear_botones(self.get_line_buttons(), "grey")
        
        self.lines = lines
        button_ax = plt.axes([0.91, 0.9 - len(self.get_line_buttons()) * 0.1, 0.08, 0.05])
        line_button = Button(button_ax, label+" "+str(len(self.get_line_buttons())+1), color="green")
        line_button.on_clicked(lambda event, l=line, b=line_button: self.toggle_line(l, b))
        ax.figure.canvas.mpl_connect('pick_event', line_button)
        self.line_buttons.append(line_button)

    def toggle_line(self, line, button):
        """
        Esta función se encarga de manejar la funcionalidad de la linea cuando se presiona el botón

        Parameters:
        - line (matplotlib.lines.Line2D): The line to be toggled.
        """
        for l in self.lines:
            if l != line:
                l.grafico.set_color("grey")
                l.set_last(False)
                
        for b in self.get_line_buttons():
            if b != button:
                b.color="gray"
            else:
               b.color = 'green'
                #b.set_facecolor("green")
                
        line.grafico.set_color(line.get_color_original())
        line.set_last(True)
        plt.draw()
        
#------------------------------------------------------------------------------------------
    def get_parable_buttons(self):
        return self.parable_buttons

#------------------------------------------------------------------------------------------
    def get_line_buttons(self):
        return self.line_buttons

    def get_lines(self):
        return self.lines

    def get_parables(self):
        return self.parables
    
    def get_last_line(self):          
        for line in self.get_lines():
            if line.is_last():
                return line
            
    def get_last_parable(self):
        for parable in self.get_parables():
            if parable.is_last():
                return parable
            
    def graficar_ajuste_pashen_activa(self, polinomio):
        last_line = self.get_last_line()
        coeficients = last_line.get_coeficient(polinomio)
        x_last_line = last_line.get_x()
        
        #Guardo los valores de la recta activa para graficar 
        self.paschen.coef= copy.copy( coeficients )
        self.xP= copy.copy( x_last_line )
        
    def graficar_ajuste_balmer_activa(self, polinomio):
        last_line = self.get_last_line()
        coeficients = last_line.get_coeficient(polinomio)
        x_last_line = last_line.get_x()
        
        #Guardo los valores de la recta activa para graficar 
        self.balmer.coef= copy.copy( coeficients )
        self.xB= copy.copy( x_last_line )
        
    def graficar_balmer_inferior_activa(self, polinomio):
        last_parable = self.get_last_parable()
        coeficients = last_parable.get_coeficient(polinomio)
        x_last_parable = last_parable.get_x()
        
        #Guardo los valores de la recta activa para graficar 
        
        self.balmer_inf.coef= copy.copy( coeficients )
        self.xB_inf= copy.copy( x_last_parable )
        
        
    def graficar_balmer_superior_activa(self, polinomio):
        last_parable = self.get_last_parable()
        coeficients = last_parable.get_coeficient(polinomio)
        x_last_parable = last_parable.get_x()
        
        #Guardo los valores de la recta activa para graficar 
        
        self.balmer_sup.coef= copy.copy( coeficients )
        
        