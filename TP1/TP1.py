import argparse
import sys
import os
import time 

def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument('-f','--file',type=str, help='file to be opened')
    args = parser.parse_args()
    try:
        archivo = open(args.file) 
    except:
        sys.stdout.write("Error: por favor seleccione un archivo válido")
        return 
    lineas = archivo.readlines()
    numero_linea = 0
    
    #Cantidad de lineas del archivo
    lineas_count = len(open(args.file).readlines())

    #Creo un tuberia para cada linea
    pipes1 = [os.pipe() for _ in range(lineas_count)]
    pipes2 = [os.pipe() for _ in range(lineas_count)]
    processes = []
    i2 = 0
 
    for i in pipes1:
        fdr = i[0]
        fdw = i[1]
        fdr2 = pipes2[i2][0]
        fdw2 = pipes2[i2][1]
        pid = os.fork()

        if pid == 0:
            os.close(fdw)
            # Leo la linea que envio el padre, la invierto
            linea = os.read(fdr,100).decode()
            linea = linea[::-1]
            os.close(fdr)
            # Envio la linea invertida al padre, usando la segunda tuberia
            os.write(fdw2, linea.encode())  
            os.close(fdw2) 
            os._exit(0)
               
        else:
            os.close(fdr)
            # Envio la linea al hijo
            linea_enviar = lineas[numero_linea]
            numero_linea += 1
            os.write(fdw, linea_enviar.encode())

            # Recibo la linea del hijo
            linearecibida = os.read(fdr2,100).decode()
            sys.stdout.write(linearecibida)
            os.close(fdr2)
            processes.append(pid)
        i2 += 1 
    for pid in processes:
            os.waitpid(pid,0)

if __name__ == '__main__':
    main()

