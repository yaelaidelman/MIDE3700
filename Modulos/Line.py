import matplotlib.pyplot as plt

class Line:
    #Por defecto siempre van a tener el mismo tamaño y color verde
    def __init__(self, grafico, color='green', last=True, x_active = None ,y_active = None):
        self.x = x_active
        self.y = y_active
        self.last = last
        self.color_original = grafico.get_color()
        self.grafico = grafico
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def set_last(self, activate):
        self.last = activate

    def is_last(self):
        return self.last
    
    def set_color(self, color):
        self.grafico.set_color(color)
        
    def get_color(self):
        return self.grafico.get_color()
    
    def get_color_original(self):
        return self.color_original
    
    
    def get_coeficient(self, polinomio):
        polinomio.minimos_cuadrados(self.get_x(), self.get_y(), 1)
        
        return polinomio.coef