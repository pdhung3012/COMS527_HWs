#include <stdio.h>
#include <stdlib.h>
#include <chrono>
#include <algorithm>
#include <iostream>
#include<vector>
using namespace std;
using namespace std::chrono;
/* Define length of dot product vectors */

#define VECLEN 1000000000
int main(int argc, char *argv[]) {
	int i, len = VECLEN;
	double *a, *b;
	double sum;

	printf("Starting omp_dotprod_serial\n");
	auto start = high_resolution_clock::now();
	/* Assign storage for dot product vectors */
	a = (double*) malloc(len * sizeof(double));
	b = (double*) malloc(len * sizeof(double));
	/* Initialize dot product vectors */
	for (i = 0; i < len; i++) {
		a[i] = 10.0;
		b[i] = a[i];
	}
	/* Perform the dot product */
	sum = 0.0;
	for (i = 0; i < len; i++) {
		sum += (a[i] * b[i]);
	}
	printf("Done. Serial version: sum = %f \n", sum);
	free(a);
	free(b);
	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

		cout << "Time taken without parallelization: "
			 << duration.count() << " microseconds" << endl;

}
