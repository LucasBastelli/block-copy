import subprocess
import sys
import os
import matplotlib.pyplot as plt

def grafico(y1,y2,y3):
    y1=sum(y1)/len(y1)
    y2=sum(y2)/len(y2)
    y3=sum(y3)/len(y3)
    plt.rcParams['figure.figsize'] = (11,7)
    plt.bar(1, y1, color='r')
    plt.bar(2, y2, color='b')
    plt.bar(3, y3, color='g')
    plt.ylabel('Tempo')
    plt.title('Comparação PM vs RAM vs SSD fsync')
    plt.legend(labels=['RAM', 'PM', 'SSD'])
    plt.savefig("graficoComparacaofsync.pdf")
    #plt.show()

def rodar(rep,programa,copia,cola,tamanho):
    retorno = []
    aux = 1
    while(aux<=rep):			#Quantidade de repeticoes
        print("Repetição "+str(aux)+" de "+str(rep))
        teste=subprocess.run([programa, copia,cola,str(tamanho)], stdout=subprocess.PIPE)
        os.remove(cola)
        tempo = teste.stdout.splitlines()
        retorno.append(tempo)
        aux+=1
		
    return retorno

def abre(nome):
    arq=open(nome,"r")	#Nome do arquivo
    lista=arq.read()
    lista=eval(lista)
    return lista


def salva(lista,nome):
    arq=open(nome+".txt","w")	#Nome do arquivo
    lista2=[]
    for line in lista:
        lista2.append(float(line[0]))
    arq.write(str(lista2))
    return

def main(arg):
    rep = 10
    if(arg[1]=='r'):
        if os.path.isfile(arg[4]):
            os.remove(arg[4])
        lista = rodar(rep, arg[2], arg[3], arg[4], arg[5])
        salva(lista,arg[6])

    elif(arg[1]=='g'):
        lista1 = abre(arg[2])
        lista2 = abre(arg[3])
        lista3 = abre(arg[4])
        grafico(lista1,lista2,lista3)
    
    else:
        print("USAGE: \nr PROGRAM FILE_INPUT FILE_OUTPUT SIZE TXT_NAME")
        print("OR:\ng RAM PM SSD")


main(sys.argv)
