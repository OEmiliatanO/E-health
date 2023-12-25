CC:=g++
CFLAG:=-Wall -Wextra -Werror -std=c++17 -I ./include/
OBJ:=call_lab.o

call_lab.elf: $(OBJ)

dep:
	$(CC) -c call_lab.cpp $(CFLAG)

all: $(OBJ)
	$(CC) -o call_lab.elf call_lab.o

.PHONY: clean
clean:
	-rm -rf *.o
