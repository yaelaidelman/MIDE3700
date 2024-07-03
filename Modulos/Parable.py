from Modulos.Line import Line

class Parable(Line):
    
    def get_coeficient(self, polinomio):
        polinomio.minimos_cuadrados(self.get_x(), self.get_y(), 2)
        
        return polinomio.coef