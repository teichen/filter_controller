#include "VanderPolModel.h"

using namespace std;

VanderPolModel::VanderPolModel()
{
    n_states = 4;

    mem_test = false;
    initarrays();

    int i,j;

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
}

void VanderPolModel::rate(double* x, double* r)
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
        r[(2*i+1)*n_states + 2*i] = -x[2*i] + (1 - x[2*i] * x[2*i]) * x[2*(i+1)];
    }
}

void VanderPolModel::initarrays()
{
    linearized_rate = (double*) calloc (n_states * n_states, sizeof(double));

    mem_test = true;
}

VanderPolModel::~VanderPolModel()
{
    if(mem_test==true)
    {
    delete [] linearized_rate;
    }
}

