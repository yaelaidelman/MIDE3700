def Leo_estrellas_in():
    file_in= open('estrellas.in', 'r') # Abro el archivo de lectura
    linea= file_in.readline()
    linea= file_in.readline()
    lista_estrellas= []
    m= []
    lohice_m= []
#
    # Leemeos el archivo
    while linea != "": # Lee linea por linea hasta el final del archivo
# Como las columnas estan separadas por espacios guardamos las columnas
# en una lista
        columna= linea.split(" ")
        lista_estrellas.append( columna[0] )# Primera columna del archivo
#
        i= 1
        n= len(columna)
        if n > 1:
            while columna[i] == '' and i <= n-2:
                i= i + 1
            if columna[i] != '' and columna[i] != '\n':
                m.append( float(columna[i]) )
                lohice_m.append( True )
            else:
                m.append( 99999. )
                lohice_m.append( False )
        else:
            m.append( 99999. )
            lohice_m.append( False )
#
        linea= file_in.readline()# leemos la siguiente linea del archivo
#
    file_in.close()
    return lista_estrellas, m, lohice_m
#-------------------------------------------------------------------------------
def Genero_BCD_out():
    f_BCD= open("BCD.out","w")
    f_BCD.write("#  ID                  D     D*    d    lambda1  Phi\n")
    f_BCD.write("#\n")
    f_BCD.close()
    return
#-------------------------------------------------------------------------------
def Genero_ParFun_out():
    f_ParFun= open("ParFun.out","w")
    f_ParFun.write("#  ID                  D*  lambda1  TE   CL    Teff  dTeff Logg dLogg    Mv   dMv     Mbol dMbol  Phio dPhio\n")
    f_ParFun.write("#\n")
    f_ParFun.close()
    return
#-------------------------------------------------------------------------------
def Genero_Dist_out():
    f_Dist= open("Dist.out","w")
    f_Dist.write("#  ID                  Phi dPhi   Phio dPhio E(B-V) dE(B-V) m      Mv  dMv    mMo  dmMo   Dist dDist\n")
    f_Dist.write("#\n")
    f_Dist.close()
    return
#-------------------------------------------------------------------------------
