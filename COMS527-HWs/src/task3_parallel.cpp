#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#define N 50
#define CHUNKSIZE 5
int main (int argc, char *argv[]) {
int i, chunk, tid;
float a[N], b[N], c[N];
/* Some initializations */
for (i=0; i < N; i++)
a[i] = b[i] = i * 1.0;
chunk = CHUNKSIZE;


#pragma omp parallel for schedule(static) num_threads(chunk) default(none) shared(a,b,c,chunk) private(i,tid)
for (i=0; i < N; i++)
{
	tid = omp_get_thread_num();
c[i] = a[i] + b[i];
printf("tid= %d i= %d c[i]= %f\n", tid, i, c[i]);
}

return 0;
}
