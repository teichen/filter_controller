#include "HarmonicModel.h"

using namespace std;

HarmonicModel::HarmonicModel()
{
    n_states = 4;
    n_inputs = 2;

    mem_test = false;
    initarrays();

    int i,j;

    // linearized rate of change of state
    for (i=0; i<n_states; i++)
    {
        for (j=0; j<n_states; j++)
        {
            linearized_rate[i*n_states + j] = 0;
        }
    }

    for (i=0; i<(int)(n_states/2); i++)
    {
        linearized_rate[2*i*n_states + 2*(i+1)] = 1;
        linearized_rate[(2*i+1)*n_states + 2*i] = -1;
    }

    // linearized jacobian of input estimates
    for (i=0; i<n_inputs; i++)
    {
        for (j=0; j<n_states; j++)
        {
            linearized_jacobian[i*n_states + j] = 
        }
    }
}

void HarmonicModel::rate(double* x, double* r)
{
    int i,j;

    for (i=0; i<n_states; i++)
    {
        for (j=0; j<n_states; j++)
        {
            r[i*n_states + j] = 0;
        }
    }

    for (i=0; i<(int)(n_states/2); i++)
    {
        r[2*i*n_states + 2*(i+1)] = x[2*(i+1)];
        r[(2*i+1)*n_states + 2*i] = -x[2*i];
    }
}

void HarmonicModel::initarrays()
{
    linearized_rate = (double*) calloc (n_states * n_states, sizeof(double));

    mem_test = true;
}

HarmonicModel::~HarmonicModel()
{
    if(mem_test==true)
    {
    delete [] linearized_rate;
    }
}

