/** Demultiplex from stdin
    
          /|    a
 c       / |----->  
 ------>/  |
        \  |    b
         \ |----->
          \|


This executable takes multiplexed input via STDIN
and demultiplexes it.

The selector is c % 2, where c is the index of each character.

Example:
    $ echo hello bob  | ./mux | ./demux
    hello
    bob

*/

#define _XOPEN_SOURCE
#define _XOPEN_SOURCE_EXTENDED

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void outputArray(char *array, int size);

int
main(int argc, char **argv)
{
    if (argc != 1)
    {
        printf("Usage: demux\n");
        return 1;
    }

    int cSize = 0;
    char c[1024];
    for (int in = fgetc(stdin); in != EOF; in = fgetc(stdin))
    {
        /* Last character on stdin is bound to be a newline */
        if (in == '\n')
        {
            continue;
        }

        c[cSize] = in == ' ' ? '\0' : in;
        cSize += 1;

        if (cSize > 1000)
        {
            printf("ERROR: Input too large.\n");
            return 1;
        }
    }

    c[cSize - 1] = '\0';

    outputArray(c, cSize);

    char *b = (char *) calloc(cSize, 1);
    char *a = (char *) calloc(cSize, 1);

    if (a == NULL || b == NULL)
    {
        printf("ERROR: Could not allocate memory.\n");
        return 1;
    }

    char *ai = a;
    char *bi = b;
    for (int i = 0; i < (cSize); i++)
    {
        if (i % 2)
        {
            *bi = c[i];
            bi++;
        }
        else
        {
            *ai = c[i];
            ai++;
        }
    }

    for (int i = 0; i < strlen(a); i++)
    {
        printf("%c", a[i]);
    }
    printf(" ");
    for (int i = 0; i < strlen(b); i++)
    {
        printf("%c", b[i]);
    }
    printf("\n");

    free(a);
    free(b);
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

