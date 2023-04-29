import argparse
import sys
import os
import time 

def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument('-f','--file',type=str, help='file to be opened')
    args = parser.parse_args()



    archivo = open(args.file)
    lineas = archivo.readlines()

    #Cantidad de lineas del archivo
    lineas_count = len(open(args.file).readlines())

  
    linea_invertida = ""

   

    #Creo un tuberia para cada linea
    pipes = [os.pipe() for _ in range(3)]
    print(pipes)
    processes = []
        
    numero_linea = 0
    for i in pipes:
        # print(i)
        # print(numero_linea)
        fdr = i[0]
        fdw = i[1]
        pid = os.fork()
        if pid == 0:
            os.close(fdw)
            #Leo la linea que envio el padre
            linea = os.read(fdr,100).decode()
            print(linea)
            os._exit(0)
            
        else:
            os.close(fdr)
            # Envio la linea al hijo
            linea_enviar = lineas[numero_linea]
            numero_linea += 1
            os.write(fdw, linea_enviar.encode())
            processes.append(pid)
    for pid in processes:
            os.waitpid(pid,0)

    print(processes)
    
        





    # if pid == 0:
    #     os.close(w)
    #     linea_invertida1 = os.read(r,1000)
    #     decoded = linea_invertida1.decode()
    #     linea_invertida = linea_invertida + decoded
    #     # sys.stdout.write(linea_invertida)
    #     os.close(rh)
    #     os.write(wh, linea_invertida.encode())

    # else:
    #     os.close(r)
    #     linea = lineas[i]
    #     linea = linea[::-1]
    #     os.write(w, linea.encode())
    #     os.close(wh)
    #     linea_devuelta = os.read(rh,1000)
    #     linea_devuelta_decoded = linea_devuelta.decode()
    #     sys.stdout.write(linea_devuelta_decoded)


    # for i in range(3):
    #     pid = os.fork()
    
    #     if pid == 0:
    #         print("Soy el proceso hijo %d con PID %d" % (i+1, os.getpid()))
    #     # Código del proceso hijo
    #         exit(0)

# Código del proceso padre
    # time.sleep(1)
    # print("Soy el proceso padre con PID %d" % os.getpid())

if __name__ == '__main__':
    main()

