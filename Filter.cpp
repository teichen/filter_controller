#include "Filter.h"

using namespace std;

Filter::Filter()
{
}

void Filter::init_model(Model& model)
{
    n = model.n_states;

    mem_test = false;
    initarrays();
}

void Filter::propagate_update(double t)
{
}

void Filter::initarrays()
{
    x_prior = (double*) calloc (n, sizeof(double));
    x_post  = (double*) calloc (n, sizeof(double));

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
