These programs use different ways to copy a file to another directory. You can use this to compare the performance difference between a normal copy and a copy using methods to force the OS to do not use cache.
Fflush just remove the cache of the program, but not the cache of the OS.
Mmap and fsync forces OS to do not use its cache.
to compile:

    make

to use:

    ./program InputFile OutputFile BlockSize

Fsync forces the computer save the changes on the drive without a buff. The buff can change the final result.
