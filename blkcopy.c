#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>


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
    FILE *input, *output;
    size_t n;
    input = fopen(infile, "r");
    if (!input) {
        printf("Unable to open input file\n");
        return(1);
    }
    output = fopen(outfile, "w");
    if (!output) {
        printf("Unable to open output file\n");
        return(1);
    }
    struct timeval begin, end;
    gettimeofday(&begin, 0);
    while ((n = fread(ptr, sizeof(char), blocksize, input)) == blocksize){
        fwrite(ptr, sizeof(char), blocksize, output);
    }
    fwrite(ptr, sizeof(char), n, output);
    free(buf);
    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;
    printf("%f\n", elapsed);
    fclose(input);
    fclose(output);
    return 0;
}
