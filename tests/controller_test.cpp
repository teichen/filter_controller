#include <iostream>
#include <cassert>
using std::cerr;
using std::cout;
using std::endl;
#include <math.h>
#include "../Controller.h"

using namespace std;
int main()
{
    // unit testing with run time asserts
    // controller tests:

    bool logging;
    string model_type;
    int n_filters;

    logging    = 0;
    model_type = "Harmonic";
    n_filters  = 4;

    Controller controller(logging, model_type, n_filters);

    // assert(TODO);

    // test 0 - single filter, moderate measurement noise
    //          initial state near stable fixed point
    //          expect small deviations about initial state
    // test 1 - single filter, strong measurement noise
    //          unstable estimate
    // test 2 - multiple filters, strong measurement noise
    //          for a finite period
    //          multi-filter system stabalizes after noise reduction

    return 0;
}
