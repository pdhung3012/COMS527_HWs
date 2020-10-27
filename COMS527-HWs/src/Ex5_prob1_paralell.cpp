#include <stdio.h>
#include <stdlib.h>
#include <chrono>
#include <algorithm>
#include <iostream>
#include<vector>
#include<omp.h>
using namespace std;
using namespace std::chrono;
/* Define length of dot product vectors */
#define NT 8
#define VECLEN 1000000000

long i;
unsigned seed;

int main(int argc, char *argv[]) {
	int i, len = VECLEN;
	double *a, *b,*c,*d;
	double sum;
	omp_set_num_threads(NT);
	printf("Starting omp_dotprod_parallel\n");
	auto start = high_resolution_clock::now();
	/* Assign storage for dot product vectors */
	a = (double*) malloc(len * sizeof(double));
	b = (double*) malloc(len * sizeof(double));
	c = (double*) malloc(len * sizeof(double));
	d = (double*) malloc(len * sizeof(double));
	/* Initialize dot product vectors */
//	run parallel a for loop for assignment
	#pragma omp parallel private(seed)
	{
		// Initialise the random number generator with different seed in each thread
		// The following constants are chosen arbitrarily... use something more sensible
		seed = 25234 + 17*omp_get_thread_num();
		#pragma omp for
		for(i=0;i<1000000;i++){
		    	a[i]=rand_r(&seed);
		    	b[i]=rand_r(&seed);
		}
	}
	/* Perform the dot product */
	//	run parallel a for loop for assignment
	#pragma omp for private(i)
	for (i = 0; i < len; i++) {
		c[i] = (a[i] + b[i]);
		d[i] = (a[i] * b[i]);
	}
	free(a);
	free(b);
	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

		cout << "Time taken with parallelization: "
			 << duration.count() << " microseconds" << endl;

}
