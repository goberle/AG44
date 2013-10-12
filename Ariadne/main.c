#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "main.h"
#include "matrix.h"

int main (int argc, char **argv) {
    if (argc > 1) {
        init(argv);
    } else {
        printf("Veuillez entrer la matrice en argument.\n");
    }

    return 0;
}

void init (char **argv) {
    int error;
    matrix_t mat;

    if ((error = fparse_matrix(argv[1], &mat)))
        exit(error);

    mat_print (stdout, &mat);

}

int fparse_matrix (char *fname, matrix_t *mat) {
    FILE *fmp = NULL;
    char buf;
    int nrows = 0, 
        ncols = 0,
        r = 0,
        c = 0;

    /* Open the matrix file */
    fmp = fopen(fname, "r");

    /* Open file verification */
    if (fmp == NULL)
        return ENOENT;

    /* Compute numbers of rows */
    rewind(fmp);
    while ((buf = fgetc(fmp)) != EOF) {
        if (buf == '\n')
            nrows++;
    }
    nrows++;

    /* Compute numbers of columns */
    rewind(fmp);
    while ((buf = fgetc(fmp)) != '\n') {
        if (buf != ' ')
            ncols++;
    }

    /* Matrix allocation */
    mat = mat_alloc (mat, nrows, ncols);
    printf("Matrix : nrows = %d and ncols = %d.\n", nrows, ncols);

    /* Parsing */
    rewind(fmp);
    while((buf = fgetc(fmp)) != EOF) {
        if (buf == ' ') 
            continue;
        if (buf == '\n') {
            r++;
            c = 0;
            continue;
        }
        *mat_cell(mat, r, c) = atoi(&buf);
        c++;
    }

    /* Close matrix file */
    fclose(fmp);

    return 0;
}