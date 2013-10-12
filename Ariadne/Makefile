CC=gcc
CFLAGS=-W -Wall -pedantic -std=c99
LDFLAGS=
EXEC=ag44

all: $(EXEC)

ag44: main.o matrix.o
	$(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) -o $@ -c $< $(CFLAGS)

clean:
	rm -rf *.o

mrproper: clean
	rm -rf $(EXEC)
