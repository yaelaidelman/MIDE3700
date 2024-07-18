# MIDE3700

**M***edición* **I***nteractiva de la* **D***iscontinuidad* **E***n* **3700** *angstroms*

Autores: Yael Aidelman (versión original en python 2.7) y Valentín Domé (versión actualizada en python 3.8)
Authors: Yael Aidelman (original version in python 2.7) and Valentín Domé (update version in python 3.8)

## Resumen
M.I.D.E.3700 es un código que permite medir interactivamente los parámetros que caracterizan la discontinuidad de Balmer y el gradiente de color (D, &lambda;<sub>1</sub> y &Phi;) del sistema espectrofotométrico BCD. Su nombre corresponde a la sigla de Medición Interactiva de la Discontinuidad En 3700 &#8491;.
Con esta herramienta el usuario puede trabajar de manera interactiva sobre el espectro estelar, y ası́, elegir los mejores ajustes. De este modo M.I.D.E.3700 estima los valores de D, &lambda;<sub>1</sub> y &Phi; de manera rápida y sencilla, con los cuales determina el tipo espectral, la clase de luminosidad y los parámetros fundamentales estelares (temperatura efectiva, logaritmo de la gravedad superficial, magnitud viasual absoluta, magnitud bolométrica y el exceso de color). A partir de estos resultados, también estima la distancia. 

## Abstract
M.I.D.E.3700 is a code that allows to interactively measure the parameters that characterize the Balmer discontinuity and the color gradient (D, &lambda;<sub>1</sub> and &Phi;) of the BCD spectrophotomic system. Its name corresponds to the acronym for Medición Interactiva de la Discontinuidad En 3700 &#8491; (Interactive Discontinuity Measurement at 3700 &#8491;). With this tool the user can work interactively on the spectrum, and thus choose the best fit. In this way M.I.D.E.3700 estimates the values of D, &lambda;<sub>1</sub> and &Phi; quickly and easily, with which it determines the spectral type, luminosity class and fundamental stellar parameters (effective temperature, logarithm of surface gravity, absolute visual magnitude, bolometric magnitude and colour excess) of the star in question. Additionally, the results are used to estimate the distance.


## Descarga e Instalación / Download and Installation

Paso 1: Descarga el repositorio.
Step 1: Download the repository.

```
git clone https://github.com/yaelaidelman/MIDE3700
```

Paso 2 (opcional): Si es usuario de conda puedes generar un entorno.
Step 2 (optional): If you are a conda user you can generate an environment.

```
conda create --name mide3700
conda activate mide3700
```

Paso 3: Dirígete al directorio creado.
Step 3: Go to the created directory.

```
cd MIDE3700
```

Paso 4: Instala las librerias de python requeridas.
Step 4: Install the required python libraries.

```
pip install -r requirement.py
```

Paso 5: Ejecuta el programa con el siguiente comando:
Step 5: Execute the program with the following command:

```
python3 MIDE3700.py
```

Puedes cambiar el tamaño de resolución de pantalla en el archivo /Configuraciones/resolucion.txt
altura,ancho (sin espacios)

You can change the screen resolution size in the file /Configuraciones/resolucion.txt
height,width (without spaces)
