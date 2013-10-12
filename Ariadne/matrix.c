#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "matrix.h"

matrix_t *
mat_alloc (matrix_t *mat, int nrows, int ncols) 
{
    assert(nrows > 0 && ncols > 0);
    mat->nrows = nrows;
    mat->ncols = ncols;
    mat->data = malloc(sizeof(int) * nrows * ncols);
    return mat;
}

int *
mat_cell (const matrix_t *mat, int row, int col)
{
    assert(row >= 0 && row < mat->nrows);
    assert(col >= 0 && col < mat->ncols);
    return mat->data + row * mat->ncols + col;
}

matrix_t *
mat_print (FILE *f, matrix_t *mat)
{
    for (int r = 0; r < mat->nrows; ++r)
    {
        for (int c = 0; c < mat->ncols; ++c)
            fprintf(f, "%4d ", *mat_cell(mat, r, c));
        fprintf(f, "\n");
    }
    return mat;
}

matrix_t *
mat_addrow (matrix_t *mat)
{
    mat->nrows++;
    mat->data = realloc(mat->data, sizeof(int) * mat->nrows * mat->ncols);
    return mat;
}

matrix_t * 
mat_addcol (matrix_t *mat)
{
    mat->ncols++;
    mat->data = realloc(mat->data, sizeof(int) * mat->nrows * mat->ncols);

    for (int r = mat->nrows - 1; r > 0; --r) {
        int *dest = mat->data + r * mat->ncols,
            *orig = mat->data + r * (mat->ncols - 1);
        memmove(dest, orig, sizeof(int) * (mat->ncols - 1));
    }
    return mat;
}