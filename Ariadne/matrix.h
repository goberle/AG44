#ifndef MATRIX_H
#define MATRIX_H

typedef struct matrix {
    int nrows;
    int ncols;
    int *data;
} matrix_t;

matrix_t *mat_alloc (matrix_t*, int, int);
int* mat_cell (const matrix_t*, int, int);
matrix_t* mat_print (FILE*, matrix_t*);
matrix_t* mat_addrow (matrix_t*);
matrix_t* mat_addcol (matrix_t*);

#endif
