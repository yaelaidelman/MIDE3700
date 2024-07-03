from random import randint
import matplotlib.pyplot as plt

def probar_error(curvas):

   #Casos fijos:
    xs = [x/1000 for x in range(150, 600, 30)]
    ys = [y for y in range(10, 80, 5)]

    casos = [(0.15, 25), (0.15, 30), (0.18, 20), (0.18, 25), (0.21, 15), (0.21, 20), (0.24, 10), (0.24, 15), (0.27, 10), (0.3, 10), (0.39, 60), (0.39, 65), (0.42, 55), (0.42, 60), (0.42, 65), (0.42, 70), (0.45, 55), (0.45, 70), (0.48, 50), (0.48, 55), (0.48, 70), (0.48, 75), (0.51, 50), (0.51, 75), (0.54, 50), (0.57, 45), (0.57, 50)]
    errores = []
    magnitudes = []

    for c in casos:
        x = c[0]
        y = c[1]
        print(f"Prueba con {x , y}")
        m = curvas.Interpolo(x, y)[1]
        error = curvas.Error(x,y,m)
        print(f"Error:. {error}")
        errores.append(error)
        magnitudes.append(m)
   
    # print(f"Entrada: \nxs = {xs}\nys = {ys}")
    print("Magnitudes: ", magnitudes)
    print("Entrada: ", casos)
    print(f"Errores = ", errores)

def probar_mv(curvas):
    # print(f"Caso de entrada {x, y}")
    # x: 0.19 - 0.22
    # y: 43.0 - 84.0

    #Casos fijos:
    xs = [x/1000 for x in range(150, 600, 20)]
    ys = [y for y in range(10, 80, 5)]


    # xs = [0.20291153295793762, 0.20291153295793762, 0.20291153295793762, 0.20291153295793762, 0.20291153295793762]
    # ys = [5.77, 6.77, 7.77, 8.77, 9.77]
    
    # xs = [x/1000 for x in range(50, 500, 40)]
    # ys = [y for y in range(-10, 75,20)]

    # xs = [0.09]
    # ys =[70]
    fig, ax = plt.subplots()
    magnitudes = []
    ejex = []
    ejey = []
    par = []

    xs = [0.17, 0.19, 0.21, 0.21, 0.21, 0.23, 0.23, 0.25, 0.25, 0.27, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.39, 0.39, 0.39, 0.39, 0.41, 0.41, 0.41, 0.43, 0.43, 0.43, 0.43, 0.43, 0.45, 0.45, 0.47, 0.47, 0.47, 0.47, 0.49, 0.49, 0.49, 0.49, 0.49, 0.51, 0.51, 0.51, 0.51, 0.51, 0.53, 0.53, 0.53, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.57, 0.57, 0.57, 0.57, 0.57, 0.57, 0.57, 0.57, 0.59, 0.59, 0.59, 0.59, 0.59]
    ys = [65, 65, 20, 65, 75, 20, 65, 20, 65, 65, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 20, 50, 60, 65, 20, 30, 50, 15, 20, 25, 55, 70, 15, 20, 10, 15, 20, 25, 10, 15, 20, 50, 75, 10, 15, 20, 40, 50, 10, 15, 20, 10, 15, 20, 25, 30, 35, 40, 45, 10, 15, 20, 25, 30, 35, 40, 45, 10, 15, 20, 35, 45]
    
    # for x,y in zip(xs,ys):
    for x, y in zip(xs, ys):


        if (True):
        # x = float(randint(1900, 2200)/10000)
            # y = float(randint(4300, 8400)/100)
        
        # y = i / 100
            # y *= 10
            # y = 57.7
            y = round(y, 2)
            print(f"Prueba con {x , y}")
            ejex.append(x)
            ejey.append(y)
            par.append((x,y))
            a, b, c = curvas.Interpolo(x, y)

            magnitudes.append(b)

    # plt.scatter(ejex, ejey, color="blue", marker=".")
    plt.show()
    print(par)
    print(f"Esta son la lista de magnitudes: ")
    print(magnitudes)
    for i in magnitudes:
        print(i)

def probar(curvas, x , y):
    # print(f"Caso de entrada {x, y}")
    # x: 0.19 - 0.22
    # y: 43.0 - 84.0

    #Casos fijos:
    xs = [x/1000 for x in range(150, 220, 5)]
    ys = [y for y in range(45, 67)]


    xs = [0.20291153295793762, 0.20291153295793762, 0.20291153295793762, 0.20291153295793762, 0.20291153295793762]
    ys = [5.77, 6.77, 7.77, 8.77, 9.77]
    
    # xs = [x/1000 for x in range(50, 500, 40)]
    # ys = [y for y in range(-10, 75,20)]

    # xs = [0.09]
    # ys =[70]

    magnitudes = []
    ejex = []
    ejey = []
    par = []
    # for x,y in zip(xs,ys):
    for x in xs:
        for y in ys:
        # if (True):
        # x = float(randint(1900, 2200)/10000)
            # y = float(randint(4300, 8400)/100)
        
        # y = i / 100
            y *= 10
            # y = 57.7
            y = round(y, 2)
            print(f"Prueba con {x , y}")
            ejex.append(x)
            ejey.append(y)
            par.append((x,y))
            a, b, c = curvas.Interpolo(x, y)

            magnitudes.append(b)

    # plt.scatter(ejex, ejey, color="blue", marker=".")
    print(par)
    print(f"Esta son la lista de magnitudes: ")
    print(magnitudes)
    for i in magnitudes:
        print(i)