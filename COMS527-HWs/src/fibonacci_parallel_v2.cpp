
#include <stdio.h>
#include <stdlib.h>
#include <chrono>
#include <algorithm>
#include <iostream>
#include<vector>
#include <omp.h>

using namespace std;
using namespace std::chrono;

#define NT 16
#define THRESHOLD 1
#define VECLEN 10000000
int* arrCaches;

int fib(int n)
{
  int x, y,n1,n2;
  if (n < 2)
	  return n;
  if(arrCaches[n]>0){
	  return arrCaches[n];
  }
  n1=n-1;
  n2=n-2;

  #pragma omp task shared(x) firstprivate(n1) final(n <= THRESHOLD)
  x = fib(n1);

#pragma omp task shared(y) firstprivate(n2) final(n <= THRESHOLD)
  y = fib(n2);

#pragma omp taskwait
  arrCaches[n]=x+y;

return arrCaches[n];

}


int main()
{
  int n,fibonacci,i;

  omp_set_dynamic(NT);
  omp_set_num_threads(NT);


  double starttime;
  printf("Please insert n, to calculate fib(n): \n");
  scanf("%d",&n);
  starttime=omp_get_wtime();
  arrCaches = (int*) malloc(VECLEN * sizeof(int));
// 	#pragma omp for
// 	for (i = 0; i < VECLEN; i++) {
// 		arrCaches[i]=-1;
// 	}


#pragma omp parallel shared(n)
  {
     #pragma omp single
	  fibonacci=fib(n);

  }

  printf("fib(%d)=%d \n",n,fibonacci);
  printf("calculation took %lf sec\n",omp_get_wtime()-starttime);
  return 0;
}
