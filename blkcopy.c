#include <stdio.h>
#include <stdlib.h>
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
    const void *ptr = (void *) buf;
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
    while ((n = fread(ptr, sizeof(char), blocksize, input)) == blocksize){
        fwrite(ptr, sizeof(char), blocksize, output);
    }
    fwrite(ptr, sizeof(char), n, output);
    pclose(input);
    pclose(output);
    return 0;
}