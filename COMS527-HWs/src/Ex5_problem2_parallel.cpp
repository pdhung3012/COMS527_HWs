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
#define L1 2000000
#define L2 1000000

long i,j;
unsigned seed;
int tid;

int main(int argc, char *argv[]) {
	int i, len = VECLEN;
	double *a, *b,*c,*d;
	double sum;
	omp_set_num_threads(NT);
	printf("Starting omp_dotprod_parallel\n");
	auto start = high_resolution_clock::now();

	#pragma omp parallel for collapse(2) private(i,j,tid)
	for(i=1;i<=L1;i++){
		for(j=1;j<=L1;j++){
			tid = omp_get_thread_num();
			cout<<"inside (i,j) ("<<i<<","<<j<<") print thread id "<<tid<<endl;
		}
	}


	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

		cout << "Time taken with parallelization: "
			 << duration.count() << " microseconds" << endl;

}
