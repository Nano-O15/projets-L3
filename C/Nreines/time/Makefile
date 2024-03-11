#  Makefile 
#  Auteur : OUKHEMANOU Mohand L3-A 
#  Algorithmique Avancée

CC = gcc
SRC = fonctions.c time.c
OBJ = $(SRC:.c=.o)
FLAGS = -Wall -Wextra -03

nreines:	$(OBJ) fonctions.h
			$(CC) -o $@ $(OBJ)
%.o: 		%.c
			$(CC) -c $< $(CFLAGS)

clean:		
			rm *.o
