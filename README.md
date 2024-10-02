# MIDE3700

**M***edición* **I***nteractiva de la* **D***iscontinuidad* **E***n* **3700** *angstroms*

Autores: Yael Aidelman (versión original en python 2.7) y Valentín Domé (versión actualizada en python 3.8)
Authors: Yael Aidelman (original version in python 2.7) and Valentín Domé (update version in python 3.8)

## Resumen
M.I.D.E.3700 es un código que permite medir interactivamente los parámetros que caracterizan la discontinuidad de Balmer y el gradiente de color (D, &lambda;<sub>1</sub> y &Phi;) del sistema espectrofotométrico BCD. Su nombre corresponde a la sigla de Medición Interactiva de la Discontinuidad En 3700 &#8491;.
Con esta herramienta el usuario puede trabajar de manera interactiva sobre el espectro estelar, y ası́, elegir los mejores ajustes. De este modo M.I.D.E.3700 estima los valores de D, &lambda;<sub>1</sub> y &Phi; de manera rápida y sencilla, con los cuales determina el tipo espectral, la clase de luminosidad y los parámetros fundamentales estelares (temperatura efectiva, logaritmo de la gravedad superficial, magnitud viasual absoluta, magnitud bolométrica y el exceso de color). A partir de estos resultados, también estima la distancia. 

## Abstract
M.I.D.E.3700 is a code that allows to interactively measure the parameters that characterize the Balmer discontinuity and the color gradient (D, &lambda;<sub>1</sub> and &Phi;) of the BCD spectrophotomic system. Its name corresponds to the acronym for Medición Interactiva de la Discontinuidad En 3700 &#8491; (Interactive Discontinuity Measurement at 3700 &#8491;). With this tool the user can work interactively on the spectrum, and thus choose the best fit. In this way M.I.D.E.3700 estimates the values of D, &lambda;<sub>1</sub> and &Phi; quickly and easily, with which it determines the spectral type, luminosity class and fundamental stellar parameters (effective temperature, logarithm of surface gravity, absolute visual magnitude, bolometric magnitude and colour excess) of the star in question. Additionally, the results are used to estimate the distance.


# Descarga e Instalación

**Paso 1:** Descarga el repositorio.

```
git clone https://github.com/yaelaidelman/MIDE3700
```

Al clonar el repositorio se genera un directorio llamado MIDE3700, dentro del cual encontraremos varios directorios y archivos:

* Los directorios `Modulos`, `Matrices`, `Curvas`, `Curvas_Muestreadas` e `Input` contienen archivos de uso interno del programa.

* En el directorio `Estrellas` debe guardar los archivos ascii de los espectros de las estrellas que desea medir. El nombre del archivo ascii debe ser de la forma `star_id.dat`. Es importante tener en cuenta que los espectros deben estar en baja resolución, $R \sim 900$. Los valores de la altura (_D_) y la posición media ($\lambda_{1}$) del salto de Balmer cambian con la resolución espectral. Para utilizar las calibraciones realizadas por Barbier, Chalonge y Divan es necesario que la resolución espectral sea igual a la resolución con la que ellos trabajaron.

* El directorio `Ajustes` contiene los archivos de salida del programa relacionados con los ajustes realizados para cada estrella. Aquí se almacenan 4 archivos para cada estrella: `star_id.1.png`, `star_id.2.png`, `star_id.3.png` y `star_id.out`. Las extensiones 1, 2 y 3 de los archivos png corresponden a: el primer ajuste (con el que se estima $T_{\rm eff}$), el ajuste realizado en el espectro normalizado por el cuerpo negro y el ajuste final, respectivamente. En el archivo `star_id.out` se almacenan los puntos utilizados para realizar los ajustes y las expresiones de las rectas y parábolas correspondientes a cada ajuste.

* `estrellas.in` es el archivo de entrada al programa. En él se listan los nombres de los archivos ascii sin la extensión .dat (`star_id`) correspondientes a los espectros de las estrellas a medir y el valor de la magnitud visual aparente, $m_{\rm v}$. En el caso en que no se cuente con el dato de la magnitud visual aparente de la estrella, no hay que poner nada (y el programa no podrá calcular la distancia).

* Los archivos de salida del programa son: `BCD.out`, `ParFun.out` y `Dist.out`, que listan los parámetros BCD, los parámetros fundamentales y la distancia, respectivamente, medidos para cada espectro listado en el archivo de entrada `estrellas.in`.


**Paso 2** (opcional): Si es usuario de conda puedes generar un entorno.

```
conda create --name mide3700
conda activate mide3700
```

**Paso 3**: Dirígete al directorio creado.

```
cd MIDE3700
```

**Paso 4**: Instala las librerias de python requeridas.

```
pip install -r requirement.py
```

Puedes cambiar el tamaño de resolución de pantalla en el archivo /Configuraciones/resolucion.txt

altura,ancho (sin espacios)

**Paso 5**: Ejecuta el programa con el siguiente comando:

```
python3 MIDE3700.py
```

Lo primero que hace el programa es cargar todas las curvas que necesita para calcular los parámetros fundamentales. Después despliega el espectro de la estrella para poder hacer todos los ajustes: continuos de Paschen y Balmer y envolventes inferior y superior de las líneas de Balmer. Por último, despliega el espectro con todos los ajustes realizados y pregunta, a través del terminal, si la estrella es más fría que una estrella de tipo A2. La respuesta debe teclearse en la misma terminal. En el siguiente link: [https://youtu.be/QZ2-Hz9hQL0](https://youtu.be/QZ2-Hz9hQL0), se puede ver un video donde se muestra como funciona la versión original de MIDE3700.


## Cómo realizar los ajustes sobre el espectro

Cuando se muestra el espectro, el título de la ventana indica qué ajuste hay que hacer. Primero se ajusta el continuo de Paschen, luego el continuo de Balmer, después la envolvente inferior y finalmente la envolvente superior de las líneas de hidrógeno. Los continuos de Paschen y Balmer se ajustan con una línea recta mientras que las envolventes con una parábola. 

* Con el botón izquierdo del ratón se selecciona el punto sobre el espectro más cercano a la posición del cursor. Se graficarán en rojo sobre el espectro. Para realizar el ajuste es necesario seleccionar 3 o más puntos.

* Pulsando la tecla «p» del teclado se selecciona el punto correspondiente a la posición del cursor. Se graficarán en rojo sobre el espectro.

* Pulsando la tecla «a» del teclado realizamos el ajuste, que se representará inmediatamente en el espectro en color verde.

* Si el ajuste no es bueno, se pueden "desactivar" los puntos con el botón derecho del ratón y se graficarán en gris sobre el espectro. Se pueden eligir nuevos puntos con el botón izquierdo del ratón o con la presionando la letra «p». Cada vez que pulsemos la tecla «a» obtendremos un nuevo ajuste. Por cada ajuste realizado aparecerá un botón. Estos botones permitirán seleccionar el mejor ajuste. El ajuste seleccionado queda represando por el botón en color verde, como se muestra en la [Fig. 11](https://github.com/user-attachments/assets/80c587d5-a3e0-4e9e-83d0-26ca22ecb913).

* Una vez estemos satisfechos con el ajuste, pulsaremos la tecla «q» para guardar y pasar al siguiente ajuste.

# Download and Installation

**Step 1**: Download the repository.

```
git clone https://github.com/yaelaidelman/MIDE3700
```

Cloning the repository generates a directory called MIDE3700, inside which you will find several directories and files:

* The `Modulos`, `Matrices`, `Curvas`, `Curvas_Muestreadas` and `Input` directories contain files for internal programme use.

* In the `Estrellas` directory you must store the ascii files of the spectra of the stars you want to measure. The name of the ascii file should be of the form `star_id.dat`. It is important to note that the spectra must be in low resolution, $R \sim 900$. The values of the height (_D_) and the mean position ($\lambda_{1}$}) of the Balmer jump change with the spectral resolution. To use the calibrations made by Barbier, Chalonge and Divan it is necessary that the spectral resolution is equal to the resolution they worked with.

* The `Ajustes` directory contains the program output files related to the settings made for each star. Four files are stored here for each star: `star_id.1.png`, `star_id.2.png`, `star_id.3.png` and `star_id.out`. Extensions 1, 2 and 3 of the png files correspond to: the first fit (with which $T_{\rm eff}$ is estimated), the fit made to the blackbody-normalised spectrum and the final fit, respectively. The `star_id.out` file stores the points used to make the fits and the expressions of the straight lines and parabolas corresponding to each fit.

* `estrellas.in` is the input file to the program. It lists the names of the ascii files without the .dat extension (`star_id`) corresponding to the spectra of the stars to be measured and the value of the apparent visual magnitude, $m_{\rm v}$. In the case where the apparent visual magnitude of the star is not available, do not enter anything (and the program will not be able to calculate the distance).

* The output files of the program are `BCD.out`, `ParFun.out` and `Dist.out`, which list the BCD parameters, fundamental parameters and distance, respectively, measured for each spectrum listed in the input file `estrellas.in`.

**Step 2** (optional): If you are a conda user you can generate an environment.

```
conda create --name mide3700
conda activate mide3700
```

**Step 3**: Go to the created directory.

```
cd MIDE3700
```

**Step 4**: Install the required python libraries.

```
pip install -r requirement.py
```

You can change the screen resolution size in the file /Configuraciones/resolucion.txt

height,width (without spaces)

**Step 5**: Execute the program with the following command:

```
python3 MIDE3700.py
```

The first thing the program does is to load all the curves it needs to calculate the fundamental parameters. Then it displays the spectrum of the star in order to make all the adjustments: Paschen and Balmer continua and lower and upper envelopes of the Balmer lines. Finally, it displays the spectrum with all the adjustments made and asks, via the terminal, whether the star is cooler than a type A2 star. The answer must be typed in the same terminal. In the following link: [https://youtu.be/QZ2-Hz9hQL0](https://youtu.be/QZ2-Hz9hQL0), you can see a video showing how the original version of MIDE3700 works.

## How to make spectrum adjustments

When the spectrum is displayed, the window title indicates which adjustment to make. First the Paschen continuum is fitted, then the Balmer continuum, then the lower envelope and finally the upper envelope of the hydrogen lines. The Paschen and Balmer continua are set with a straight line while the envelopes are set with a parabola.

* The left mouse button is used to select the point on the spectrum closest to the cursor position. It will be plotted in red on the spectrum. To make the adjustment it is necessary to select 3 or more points.

* Pressing the «p» key on the keyboard selects the point corresponding to the cursor position. They will be plotted in red on the spectrum.

* By pressing the «a» key on the keyboard, the setting is made, which is immediately displayed in green on the spectrum.

* If the setting is not good, the points can be "deactivated" with the right mouse button and will be plotted in grey on the spectrum. New points can be selected with the left mouse button or by pressing the letter «p». Each time the «a» key is pressed, a new adjustment is made. A button will appear for each adjustment made. These buttons allow you to select the best setting. The selected setting is represented by the green button, as shown in [Fig. 11](https://github.com/user-attachments/assets/80c587d5-a3e0-4e9e-83d0-26ca22ecb913).

* Once you are satisfied with the setting, press the ‘q’ key to save and move on to the next setting.
