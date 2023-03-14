#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <unistd.h>
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
    struct timeval begin, end;
    gettimeofday(&begin, 0);
    while ((n = fread(ptr, sizeof(char), blocksize, input)) == blocksize){
        write(output, ptr, sizeof(char)*blocksize);
        fsync(output);
    }
    write(output, ptr, sizeof(char)*n);
    fsync(output);
    free(buf);
    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;
    printf("%f\n", elapsed);
    fclose(input);
    close(output);
    return 0;
}
