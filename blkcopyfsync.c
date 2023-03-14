#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

int main(int argc, char *argv[]){
    if (argc < 4)
    {
        printf("Missing something\n");
        printf("USAGE: file output_file sizeof_blocks\n");
        return(1);
    }
    char *infile= argv[1];
    char *outfile= argv[2];
    int blocksize = atoi(argv[3]);
    if(blocksize==0){
        printf("invalid size number\n");
        return(1);
    }
    char *buf;
    buf = malloc(sizeof(char) * blocksize);
    void *ptr = (void *) buf;
    FILE *input;
    int output;
    size_t n;
    input = fopen(infile, "r");
    if (!input) {
        printf("Unable to open input file\n");
        return(1);
    }
    output = creat(outfile, S_IWUSR | S_IRUSR);
    if (output < -1) {
        printf("Unable to open output file\n");
        return(1);
    }
    clock_t inicio, fim;
    double tempo_execucao;

    inicio = clock(); // registra o tempo de início da execução
    while ((n = fread(ptr, sizeof(char), blocksize, input)) == blocksize){
        write(output, ptr, sizeof(char)*blocksize);
        fsync(output);
    }
    write(output, ptr, sizeof(char)*n);
    fsync(output);
    free(buf);
    fim = clock(); // registra o tempo de término da execução

    tempo_execucao = ((double) (fim - inicio)) / CLOCKS_PER_SEC;
    printf("%f\n", tempo_execucao);
    fclose(input);
    close(output);
    return 0;
}
