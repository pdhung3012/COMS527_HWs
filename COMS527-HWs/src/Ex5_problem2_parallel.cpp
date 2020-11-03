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
#define NT 32
#define VECLEN 1000000000
#define L1 1000000
#define L2 10

long i, j;
unsigned seed;
int tid;

int main(int argc, char *argv[]) {
	int i, len = VECLEN;
	double sum;
	omp_set_num_threads(NT);
	printf("Starting omp_dotprod_parallel\n");
	auto start = high_resolution_clock::now();
	#pragma omp target
	{
		#pragma omp parallel for collapse(2) private(i,j,tid)
		for (i = 1; i <= L1; i++) {
			for (j = 1; j <= L2; j++) {
				tid = omp_get_thread_num();
				printf( "inside (i,j) (%d,%d) print thread id %d\n",i,j,tid);
			}
		}

	}

	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);
	long dCount=duration.count();
	printf( "Time taken with parallelization: %d microseconds\n",dCount );

}
