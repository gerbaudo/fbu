#include <cstdlib> // atoi
#include <iostream>
#include <stdio.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>

/* compile with
 * g++ -Wall  -o poisson_gen poisson_gen.cpp -lgsl -lgslcblas -lm
 *
 * script to compare the time required to generate a sequence of N
 * random number following Poisson's distribution.
 *
 * davide.gerbaudo@gmail.com August 2013
 */

using namespace std;

int main (int argc, char *argv[])
{
  if(argc<2){
    cout<<"Usage : "<<argv[0]<<" N_events"<<endl;
    return 0;
  }
  int n = atoi(argv[1]);
  const gsl_rng_type * T;
  gsl_rng * r;
  double mu = 2500.0;
  int seed  = 12345;
  double val=0;
  T = gsl_rng_mt19937; // use Mersenne Twister
  r = gsl_rng_alloc (T);
  gsl_rng_set (r, seed);
  printf("Generanting %d values using GSL with mu=%.2f\n", n, mu);
  for(int i=0; i<n; ++i) {
    val = gsl_ran_poisson (r, mu);
  } //end for(i)

  printf ("\n");
  gsl_rng_free (r);
  return 0;
}
