import subprocess
import matplotlib.pyplot as plt
import numpy as np
import statistics
import sys

# Define the programs
programs = ["blkcp", "blkmmap", "blkfsync", "blkfflush"]
blockSizes = ["4096","8192"]
argsTypes = ['SSD to SSD','SSD to PM','PM to SSD', 'PM to PM']
argsFiles = [
    ["/home-ext/LucasIC/test.img", "/home-ext/LucasIC/test2.img"],
    ["/home-ext/LucasIC/test.img", "/mnt/nvram0/test2.img"],
    ["/mnt/nvram0/test.img", "/home-ext/LucasIC/test2.img"],
    ["/mnt/nvram0/test.img", "/mnt/nvram0/test2.img"]
    # Add more tuples for each set of arguments
]


Rep = 5 #Number of repetitions


def plot_bar_with_confidence_interval(values, confidence_intervals, label):
    # Cria uma figura e um conjunto de subtramas
    fig, ax = plt.subplots()

    # Cria um array com a posição de cada barra
    x_pos = np.arange(len(values))

    # Cria as barras no gráfico de barras
    ax.bar(x_pos, values, yerr=confidence_intervals, align='center', alpha=0.5, ecolor='black', capsize=10)

    # Define as labels para o eixo x
    ax.set_xticks(x_pos)
    ax.set_xticklabels('SSD','PM')

    # Define os labels dos eixos e o título do gráfico
    ax.set_xlabel('Dispositivos')
    ax.set_ylabel('Tempo em segundos')
    ax.set_title(label)
    plt.savefig(label+".pdf")



# Define a função para calcular o intervalo de confiança bootstrap
def bootstrap_confidence_interval(data):
    num_samples=1000
    confidence_level=0.95
    # Gera amostras bootstrap
    bootstrap_samples = np.random.choice(data, (num_samples, len(data)))
    
    # Calcula a média de cada amostra
    bootstrap_means = np.mean(bootstrap_samples, axis=1)
    
    # Calcula os percentis inferior e superior para o intervalo de confiança
    lower_percentile = (1 - confidence_level) / 2 * 100
    upper_percentile = (1 + confidence_level) / 2 * 100
    
    # Calcula o intervalo de confiança
    confidence_interval = tuple(np.percentile(bootstrap_means, [lower_percentile, upper_percentile]))
    
    return confidence_interval


def benchmark(program,rm,arg):
    # Iterate over each set of arguments
    # Construct the command
    command = f"{'./'+program} {arg[0]} {arg[1]} {arg[2]}"
    
    # Execute the command
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if(rm==True):
        command2 =f"{'rm'} {arg[1]}"
        process2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
    # Return the output
    return(process.stdout.splitlines())

def salva(lista,nome):
    arq=open(nome+".txt","w")	#Nome do arquivo
    lista2=[]
    for line in lista:
        lista2.append(float(line[0]))
    arq.write(str(lista2))
    return

def abre(nome):
    arq=open(nome+".txt","r")	#Nome do arquivo
    lista=arq.read()
    lista=eval(lista)
    return lista

def run_bench():
    rm = True
    for program in programs:
        for block in blockSizes:
            i = 0
            for i in range(len(argsTypes)):
                counter = 0
                allruns = []
                while(counter<Rep):
                    text = benchmark(program,rm,[argsFiles[i][0],argsFiles[i][1], block])
                    allruns.append(text)
                    counter+=1
                salva(allruns,program+argsTypes[i]+block)

def grafico():
    lista1 = []
    lista2 = []
    for program in programs:
        for block in blockSizes:
            i = 0
            for i in range(len(argsTypes)):
                NameFile = program+argsTypes[i]+block
                lista1 = abre(NameFile)
                i+1
                NameFile = program+argsTypes[i]+block
                lista2 = abre(NameFile)
                interval1 = bootstrap_confidence_interval(lista1)
                interval2 = bootstrap_confidence_interval(lista2)

                plot_bar_with_confidence_interval([statistics.mean(lista1),statistics.mean(lista2)], 
                                                    [interval1,interval2], 
                                                    program+argsTypes[i][:3]+block)




def main(args):
    
    if(args[1]=='-b'):
        run_bench()
    
    elif(args[1]=='-g'):
        grafico()

    elif(args[1]=='-a'):
        run_bench()
        grafico()
    
    else:
        print("USAGE MODE:\n-b Runs benchmark\n-g Produces the graphics\n-a Execute both\n\n\n")

main(sys.argv)