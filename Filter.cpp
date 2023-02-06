#include "Filter.h"

using namespace std;

Filter::Filter()
{
    n_states = 4;

    mem_test = false;
    initarrays();
}

void Filter::propagate_update(double t)
{
}

void Filter::initarrays()
{
    x_prior = (double*) calloc (n_states, sizeof(double));
    x_post  = (double*) calloc (n_states, sizeof(double));

    mem_test = true;
}

Filter::~Filter()
{
    if(mem_test==true)
    {
    delete [] x_prior;
    delete [] x_post;

    cout << "Deallocate Filter memory" << endl;

    }
}
