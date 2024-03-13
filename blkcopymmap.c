#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>

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
    int input, output;
    void *source, *target;
    size_t i, filesize;
    input = open(infile, O_RDONLY);
    if (input < 0) {
        printf("Unable to open input file\n");
        return(1);
    }
    struct stat sb;
    if (fstat(input, &sb) == -1){
        printf("Input file has no size\n");
        return(1);
    }
    filesize = sb.st_size;

    // Map the source file into memory
    source = mmap(0, filesize, PROT_READ, MAP_SHARED, input, 0);
    if (source == MAP_FAILED) {
        printf("mmap error\n");
        return 1;
    }

    // Open the target file for writing
    output = open(outfile, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
    if (output < 0) {
        printf("Unable to open output file\n");
        return 1;
    }

    // Truncate the target file to the size of the source file
    if (ftruncate(output, filesize) == -1) {
        printf("ftruncate error\n");
        return 1;
    }

    // Map the target file into memory
    target = mmap(0, filesize, PROT_WRITE, MAP_SHARED, output, 0);
    if (target == MAP_FAILED) {
        printf("mmap error\n");
        return 1;
    }

    struct timeval begin, end;
    gettimeofday(&begin, 0);
    // Copy the source file to the target file block by block
    for (i = 0; i < filesize; i += blocksize) {
        size_t block;
        if(i + blocksize>filesize){
            block = filesize  -i;
        } 
        else{
            block = blocksize;
        }
        memcpy((char*)target + i, (char*)source + i, block);

        // Ensure the changes are written to the target file
        if (msync((char*)target + i, block, MS_SYNC) == -1) {
            printf("msync error\n");
            return 1;
        }
    }
    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;
    printf("%f\n", elapsed);
    // Unmap and close the files
    munmap(source, filesize);
    munmap(target, filesize);
    close(source);
    close(target);

    return 0;
}

