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

def plot_list(lst, label):
    plt.plot(lst)
    plt.xlabel('Index')
    plt.ylabel('Tempo')
    plt.xticks(range(len(lst)), range(len(lst)))
    plt.savefig(label+".pdf")
    plt.close()


def plot_bar_with_confidence_interval(values, confidence_intervals, xlabel, label):
    # Cria um array com a posição de cada barra
    fig, ax = plt.subplots()

    # Create an array for the positions of the bars on the x-axis
    x_pos = np.arange(len(values))

    #Random colors for the bars
    cmap = plt.cm.tab10
    colors = cmap(np.arange(len(values)) % cmap.N)
    # Create the bars
    ax.bar(x_pos, values, yerr=[confidence_intervals[0], confidence_intervals[1]], 
           align='center', alpha=0.5, ecolor='black', capsize=10, label=label, color=colors)

    # Set the x-axis tick labels to the names of the bars
    ax.set_xticks(x_pos)
    ax.set_xticklabels(xlabel)
    plt.title(label)
    plt.savefig(label+".pdf")
    plt.close()




# Define a função para calcular o intervalo de confiança bootstrap
def bootstrap_confidence_interval(data):
    num_samples=10000
    confidence_level=0.95
    # Gera amostras bootstrap
    bootstrap_samples = np.random.choice(data, (num_samples, len(data)))
    
    # Calcula a média de cada amostra
    bootstrap_means = np.mean(bootstrap_samples, axis=1)
    
    # Calcula os percentis inferior e superior para o intervalo de confiança
    lower_percentile = (1 - confidence_level) / 2 * 100
    upper_percentile = (1 + confidence_level) / 2 * 100
    
    # Calcula o intervalo de confiança
    confidence_interval = np.percentile(bootstrap_means, [lower_percentile, upper_percentile])
    
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
            print("Blocks: ",block)
            i = 0
            for i in range(len(argsTypes)):
                print("Type: ", argsTypes[i])
                counter = 0
                allruns = []
                while(counter<Rep):
                    text = benchmark(program,rm,[argsFiles[i][0],argsFiles[i][1], block])
                    allruns.append(text)
                    counter+=1
                salva(allruns,program+argsTypes[i]+block)

def grafico():
    for program in programs:
        for block in blockSizes:
            xlables=[]
            auxlist = []
            meanlist = []
            interval = []
            reup = 0
            redown = 0
            resultsUP = []
            resultsDOWN = []
            for copytype in argsTypes:
                xlables.append(copytype)
                NameFile = program+copytype+block
                auxlist = abre(NameFile)
                meanlist.append(statistics.mean(auxlist))
                redown, reup = bootstrap_confidence_interval(auxlist)
                resultsUP.append(reup)
                resultsDOWN.append(redown)

            interval.append(resultsDOWN)
            interval.append(resultsUP)
            plot_bar_with_confidence_interval(meanlist, interval, xlables, program+block)


def graficoSeq():
    for program in programs:
        for block in blockSizes:
            for copytype in argsTypes:
                auxlist = []
                NameFile = program+copytype+block
                auxlist = abre(NameFile)
                plot_list(auxlist,NameFile)


def main(args):
    
    if(args[1]=='-b'):
        run_bench()
    
    elif(args[1]=='-g'):
        grafico()
        
    elif(args[1]=='-s'):
        graficoSeq()

    elif(args[1]=='-a'):
        run_bench()
        grafico()
    
    else:
        print("USAGE MODE:\n-b Runs benchmark\n-g Produces the graphics to compare\n-s Create graphics of each run\n-a Execute both\n\n\n")

main(sys.argv)
