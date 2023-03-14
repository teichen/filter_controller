#include "Filter.h"
#include <gsl/gsl_blas.h>

using namespace std;

Filter::Filter()
{
}

void Filter::init_model(Model& model)
{
    n = model.n_states;
    jacobian_linearized = model.jacobian_linearized;

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
    double gain[n_meas * n];
    double gain_T[n_meas * n];
    double noise[n_meas * n_meas];

    int i,j;

    for (i=0; i<n_meas; i++)
    {
        for (j=0; j<n; j++)
        {
            gain[i*n + j] = sig_prior * jacobian_linearized.T * inv(jacobian_linearized * sig_prior * jacobian_linearized.T + noise);
        }
    }

    for (i=0; i<n; i++)
    {
        for (j=0; j<n_meas; j++)
        {
            gain_T[i*n_meas + j] = gain[j*n + i];
        }
    }

    for (i=0; i<n_meas; i++)
    {
        residuals[i] = inputs[i] - estimates[i];
    }

    double dx[n];

    gsl_matrix_view gain_T_matrix    = gsl_matrix_view_array(gain_T, n, n_meas);
    gsl_matrix_view residuals_matrix = gsl_matrix_view_array(residuals, n_meas, 1);
    gsl_matrix_view dx_matrix        = gsl_matrix_view_array(dx, n, 1);

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans, 1.0, gain_T_matrix, residuals_matrix, 0.0, dx_matrix);

    for (i=0; i<n; i++)
    {
        dx[i]     = gsl_matrix_get(dx_matrix, i, 0);
        x_post[i] = x_prior[i] + dx[i];
    }
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
    jacobian_linearized = (double*) calloc(n * n_meas, sizeof(double));

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
    delete [] jacobian_linearized;

    cout << "Deallocate Filter memory" << endl;

    }
}
