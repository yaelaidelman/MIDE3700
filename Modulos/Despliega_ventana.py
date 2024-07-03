#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Crea una ventana
"""

import sys
from PyQt4 import QtGui, QtCore

##########################################################################################
class Communicate(QtCore.QObject):

    closeApp= QtCore.pyqtSignal()# señal para cerrar la ventana

class Ventana(QtGui.QMainWindow):
    # Atributos
    #c_o_f= ''

    """
    Ventana hereda la clase QtGui.QMainWindow
    Esto significa que podemos llamar a dos constructores.
    El primero para la clase Ventana y el segundo para la clase heredada.
    """
    def __init__(self):
        """
        El método super() devuelve el objeto primario de la clase Ventana
        y llamamos a su constructor.
        """
        self.c_o_f= ''
        super(Ventana, self).__init__()
        self.Creo_Ventana()

    def Creo_Ventana(self):

        self.c= Communicate()
        self.c.closeApp.connect(self.close)

        # ubicacion de la ventana en la pantalla y tamaño de la ventana
        self.setGeometry(300, 300, 450, 150)

        # Creo 2 botones en la ventana
        #self.btn1= QtGui.QPushButton("Si", self)
        self.btn1= QtGui.QPushButton("Yes", self)
        self.btn1.move(30, 100)

        self.btn2 = QtGui.QPushButton("No", self)
        self.btn2.move(320, 100)
             
        self.btn1.clicked.connect(self.onClicked)            
        self.btn2.clicked.connect(self.onClicked)

        #self.connect(btn1, SIGNAL('clicked()'),self.onClicked)
        #self.connect(btn2, SIGNAL('clicked()'),self.onClicked)

        self.statusBar()

        # titulo para la ventana
        self.setWindowTitle('Simple')

        lbl1 = QtGui.QLabel("La estrella es mas fria que una tipo A2? \n Is the star colder than a spectral type A2?", self)
        lbl1.setGeometry(98, 10, 255, 50)

        # muestra la ventana en la pantalla
        self.show()
        return

    def onClicked(self):

        sender= self.sender()
        #if sender.text() == 'Si':
        if sender.text() == 'Yes':
            self.c_o_f= 'f'
        else:
            self.c_o_f= 'c'
        self.c.closeApp.emit()# emite la señal para cerrar la ventana
        return
##########################################################################################
def Despliega_ventana():
    """
    Todas las aplicaciones PyQt4 deben crear un objeto aplicacion. El objeto aplicacion se ubica en el modulo QtGui. El parametro sys.argv es una lista de argumentos desde una linea de comnado.
    """
    app= QtGui.QApplication(sys.argv)
    ven= Ventana()
    app.exec_()# Cierro la aplicacion
    #sys.exit(app.exec_())
    return ven.c_o_f
##########################################################################################
##########################################################################################
##########################################################################################
