

#include <stdio.h>
#include <omp.h>
#define NT 1

int fib(int n)
{
  int x, y;
  if (n < 2) 
	  return n;

  x = fib(n - 1);

  y = fib(n - 2);

  return x+y;

}


int main()
{
  int n,fibonacci;
  omp_set_num_threads(NT);
  double starttime;
  printf("Please insert n, to calculate fib(n): \n");
  scanf("%d",&n);
  starttime=omp_get_wtime();

  fibonacci=fib(n);

  printf("fib(%d)=%d \n",n,fibonacci);
  printf("calculation took %lf sec\n",omp_get_wtime()-starttime);
  return 0;
}
