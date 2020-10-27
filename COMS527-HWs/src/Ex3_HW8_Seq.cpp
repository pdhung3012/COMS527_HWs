#include <stdio.h>
#include <chrono>
#include <algorithm>
#include <iostream>
#include<vector>
#include <omp.h>
using namespace std;
using namespace std::chrono;

long i;
unsigned seed;
int arr1[1000000];
int arr2[1000000];

int main(){


    // Get starting timepoint
	auto start = high_resolution_clock::now();

	seed = 25234 + 17*2;
	for(i=0;i<1000000;i++){
			arr1[i]=rand_r(&seed);
			arr2[i]=rand_r(&seed);
	}




    // Get ending timepoint
	auto stop = high_resolution_clock::now();
	auto duration = duration_cast<microseconds>(stop - start);

	    cout << "Time taken without parallelization: "
	         << duration.count() << " microseconds" << endl;

    return 0;
}
