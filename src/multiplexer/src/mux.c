/** A multiplexer

      a |\
  ----->| \  
        |  \--------> c
      b |  /
  ----->| /
        |/

Multiplex 2 inputs via STDIN.

The selector is c % 2, where c is the index of each character.

Example:
    $ echo hello bob  | ./mux
    hbeolbl o

*/

#define _XOPEN_SOURCE
#define _XOPEN_SOURCE_EXTENDED

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

void outputArray(char *array, int size);

int
main(int argc, char **argv)
{
    char a[1024];
    char b[1024];
    fscanf(stdin, "%s %s", a, b);

    assert(a != NULL);
    assert(b != NULL);

    int maxSize = strlen(a);
    if (maxSize < strlen(b))
    {
        maxSize = strlen(b);
    }

    maxSize += 1;  // terminating zero

    int cSize = maxSize * 2;
    char *c = (char *) calloc(cSize, sizeof(char));

    assert(c != NULL);

    char *ai = a;
    char *bi = b;
    for (int i = 0; i < cSize; i++)
    {
        if (i % 2)
        {
            c[i] = *bi == '\0' ? *bi : *bi++;
        }
        else
        {
            c[i] = *ai == '\0' ? *ai : *ai++;
        }
    }

    outputArray(c, cSize);

    free(c);
}

void
outputArray(char *array, int size)
{
    for (int i = 0; i < size; i++)
    {
        printf("%c", array[i] != '\0' ? array[i] : ' ');
    }
    printf("\n");
}

