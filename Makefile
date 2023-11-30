CC:=g++
CFLAG:=-Wall -Wextra -Werror -std=c++17 -I ./include/
OBJ:=unit_test.o

unit_test.elf: $(OBJ)

dep:
	$(CC) -c unit_test.cpp $(CFLAG)

all: $(OBJ)
	$(CC) -o unit_test.elf unit_test.o

.PHONY: clean
clean:
	-rm -rf *.o
