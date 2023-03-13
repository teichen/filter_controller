#include "Filter.h"

using namespace std;

Filter::Filter()
{
}

void Filter::init_model(Model& model)
{
    n = model.n_states;

    RungeKutta propagator(model);

    mem_test = false;
    initarrays();

    initialize_state();

    t0 = 0.0;
}

void Filter::propagate_update(double t)
{
    /* propagate the prior estimate (mean and covariance of a Normal distriution)
       update the posterior estimate (mean and covariance of a Normal distribution)
    */
    double dt;
    dt = t - t0;

    set_prior(x_post, sig_post);
    propagator.propagate(t0, t, dt, x_prior);

    set_posterior(x_prior, sig_prior);
    update(x_post);

    t0 = t;
}

void Filter::update(double* x)
{
}

void Filter::set_prior(double* x, double* sigma)
{
    int i,j;
    for (i=0; i<n; i++)
    {
        x_prior[i] = x[i];
        for (j=0; j<n; j++)
        {
            sig_prior[i*n + j] = sigma[i*n + j];
        }
    }
}

void Filter::set_posterior(double* x, double* sigma)
{
    int i,j;
    for (i=0; i<n; i++)
    {
        x_post[i] = x[i];
        for (j=0; j<n; j++)
        {
            sig_post[i*n + j] = sigma[i*n + j];
        }
    }
}

void Filter::initialize_state()
{
    int i, j;
    
    for (i=0; i<n; i++)
    {
        x_prior[i] = 0.0;
    }
    for (i=0; i<n; i++)
    {
        x_prior[i] = 0.0;
        for (j=0; j<n; j++)
        {
            sig_prior[i*n + j] = 0.0;
        }
    }
}

void Filter::initarrays()
{
    x_prior   = (double*) calloc (n, sizeof(double));
    x_post    = (double*) calloc (n, sizeof(double));
    sig_prior = (double*) calloc (n * n, sizeof(double));
    sig_post  = (double*) calloc (n * n, sizeof(double));

    mem_test = true;
}

Filter::~Filter()
{
    if(mem_test==true)
    {
    delete [] x_prior;
    delete [] x_post;
    delete [] sig_prior;
    delete [] sig_post;

    cout << "Deallocate Filter memory" << endl;

    }
}
