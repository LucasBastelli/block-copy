The program in C use fread nd fwrite to copy a file to another directory
to compile:

    gcc -o blkcopy blkcopy.c
    
and:

    gcc -o blkfsync blkcopyfsync.c

to use:

    ./blkcopy InputFile OutputFile BlockSize

Fsync forces the computer save the changes on the drive without a buff. The buff can change the final result.
