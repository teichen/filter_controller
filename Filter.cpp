#include "Filter.h"
#include <gsl/gsl_blas.h>

using namespace std;

Filter::Filter()
{
}

void Filter::init_model(Model& model)
{
    n         = model.n_states;
    n_in      = model.n_inputs;
    jacobian  = model.linearized_jacobian;
    laplacian = model.linearized_laplacian;

    RungeKutta propagator(model);

    mem_test = false;
    initarrays();

    initialize_state();

    t0 = 0.0;
}

void Filter::propagate_update(double t, double* input_data)
{
    /* propagate the prior estimate (mean and covariance of a Normal distriution)
       update the posterior estimate (mean and covariance of a Normal distribution)
    */
    double dt;
    dt = t - t0;

    set_prior(x_post, sig_post);
    propagator.propagate(t0, t, dt, x_prior);

    set_posterior(x_prior, sig_prior);
    update(x_post, input_data);

    t0 = t;
}

void Filter::update(double* x, double* inputs)
{
    double gain[n_in * n];
    double gain_T[n_in * n];
    double noise[n_in * n_in];
    double residuals[n_in];
    double estimates[n_in];
    double jacobian_T[n_in * n];

    int i,j;

    for (i=0; i<n; i++)
    {
        for (j=0; j<n_in; j++)
        {
            jacobian_T[i*n + j] = jacobian[j*n + i];
        }
    }

    calc_estimates(x, estimates);

    gsl_matrix_view sig_prior_matrix  = gsl_matrix_view_array(sig_prior, n, n);
    gsl_matrix_view jacobian_matrix   = gsl_matrix_view_array(jacobian, n_in, n);
    gsl_matrix_view jacobian_T_matrix = gsl_matrix_view_array(jacobian_T, n, n_in);
    gsl_matrix_view noise_matrix      = gsl_matrix_view_array(noise, n_in, n_in);

    double jac_sig[n_in * n];
    double jac_sig_T[n_in * n];

    gsl_matrix_view jac_sig_matrix = gsl_matrix_view_array(jac_sig, n_in, n);

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans, 1.0, jacobian_matrix, sig_prior_matrix, 0.0, jac_sig_matrix);

    for (i=0; i<n_in; i++)
    {
        for (j=0; j<n; j++)
        {
            jac_sig[i * n + j]      = gsl_matrix_get(jac_sig_matrix, i, j);
            jac_sig_T[j * n_in + i] = jac_sig[i * n + j];
        }
    }

    for (i=0; i<n_in; i++)
    {
        for (j=0; j<n; j++)
        {
            gain[i * n + j] = jac_sig_T * inv(jac_sig * jacobian_T + noise);
        }
    }

    for (i=0; i<n; i++)
    {
        for (j=0; j<n_in; j++)
        {
            gain_T[i*n_in + j] = gain[j*n + i];
        }
    }

    for (i=0; i<n_in; i++)
    {
        residuals[i] = inputs[i] - estimates[i];
    }

    double dx[n];

    gsl_matrix_view gain_T_matrix    = gsl_matrix_view_array(gain_T, n, n_in);
    gsl_matrix_view residuals_matrix = gsl_matrix_view_array(residuals, n_in, 1);
    gsl_matrix_view dx_matrix        = gsl_matrix_view_array(dx, n, 1);

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans, 1.0, gain_T_matrix, residuals_matrix, 0.0, dx_matrix);

    for (i=0; i<n; i++)
    {
        dx[i]     = gsl_matrix_get(dx_matrix, i, 0);
        x_post[i] = x_prior[i] + dx[i];
    }
}

void Filter::calc_estimates(double* x, double* estimates)
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
    jacobian  = (double*) calloc(n * n_in, sizeof(double));
    laplacian = (double*) calloc(n * n * n_in, sizeof(double));

    mem_test  = true;
}

Filter::~Filter()
{
    if(mem_test==true)
    {
    delete [] x_prior;
    delete [] x_post;
    delete [] sig_prior;
    delete [] sig_post;
    delete [] jacobian;
    delete [] laplacian;

    cout << "Deallocate Filter memory" << endl;

    }
}
