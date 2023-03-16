PROGRAMS = blkfsync blkfflush blkcp

all:	$(PROGRAMS)


blkfsync:	blkcopyfsync.c
	gcc -O3 -o blkfsync blkcopyfsync.c

blkfflush:	blkcopyfflush.c
	gcc -O3 -o blkfflush blkcopyfflush.c

blkcp:	blkcopy.c
	gcc -O3 -o blkcp blkcopy.c


clean:
	rm -f $(PROGRAMS) *.o
	rm -f $(PROGRAMS)