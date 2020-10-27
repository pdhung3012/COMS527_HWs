

#include <stdio.h>
#include <omp.h>
#define NT 16
#define THRESHOLD 1


int fib(int n)
{
  int x, y;
  if (n < 2)
	  return n;
if(n<20){
	return fib(n-1)+fib(n-2);
} else{
#pragma omp task shared(x) firstprivate(n) final(n <= THRESHOLD)
  x = fib(n - 1);

#pragma omp task shared(y) firstprivate(n) final(n <= THRESHOLD)
  y = fib(n - 2);

}


#pragma omp taskwait
  return x+y;

}


int main()
{
  int n,fibonacci;

  omp_set_dynamic(NT);
  omp_set_num_threads(NT);
  double starttime;
  printf("Please insert n, to calculate fib(n): \n");
  scanf("%d",&n);
  starttime=omp_get_wtime();

#pragma omp parallel shared(n)
  {
     #pragma omp single
	  fibonacci=fib(n);

  }

  printf("fib(%d)=%d \n",n,fibonacci);
  printf("calculation took %lf sec\n",omp_get_wtime()-starttime);
  return 0;
}
