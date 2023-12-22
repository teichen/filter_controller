#include "Filter.h"
#include <gsl/gsl_blas.h>
#include <gsl/gsl_linalg.h>

using namespace std;

Filter::Filter()
{
    mem_test = false;
}

void Filter::init_model(Model& model)
{
    n         = model.n_states;
    n_in      = model.n_inputs;
    jacobian  = model.linearized_jacobian;
    laplacian = model.linearized_laplacian;

    propagator.init_model(model);

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

    for (i=0; i<n_in; i++)
    {
        noise[i * n_in + i] = 0.001;
    }

    for (i=0; i<n; i++)
    {
        for (j=0; j<n_in; j++)
        {
            jacobian_T[i * n_in + j] = jacobian[j * n + i];
        }
    }

    calc_estimates(x, estimates);

    gsl_matrix_view sig_prior_matrix  = gsl_matrix_view_array(sig_prior, n, n);
    gsl_matrix_view jacobian_matrix   = gsl_matrix_view_array(jacobian, n_in, n);
    gsl_matrix_view jacobian_T_matrix = gsl_matrix_view_array(jacobian_T, n, n_in);
    gsl_matrix_view noise_matrix      = gsl_matrix_view_array(noise, n_in, n_in);

    double jac_sig[n_in * n];
    double jac_sig_T[n_in * n];
    double sig_inputs[n_in * n_in];

    gsl_matrix_view jac_sig_matrix    = gsl_matrix_view_array(jac_sig, n_in, n);
    gsl_matrix_view jac_sig_T_matrix  = gsl_matrix_view_array(jac_sig_T, n, n_in);
    gsl_matrix_view sig_inputs_matrix = gsl_matrix_view_array(sig_inputs, n_in, n_in);

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans, 1.0, &jacobian_matrix.matrix, 
            &sig_prior_matrix.matrix, 0.0, &jac_sig_matrix.matrix);

    for (i=0; i<n_in; i++)
    {
        for (j=0; j<n; j++)
        {
            jac_sig[i * n + j]      = gsl_matrix_get(&jac_sig_matrix.matrix, i, j);
            jac_sig_T[j * n_in + i] = jac_sig[i * n + j];
        }
    }

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans, 1.0, &jac_sig_matrix.matrix, 
            &jacobian_T_matrix.matrix, 0.0, &sig_inputs_matrix.matrix);

    for (i=0; i<n_in; i++)
    {
        for (j=0; j<n_in; j++)
        {
            sig_inputs[i * n_in + j] = gsl_matrix_get(&sig_inputs_matrix.matrix, i, j);
        }
    }

    double inputs_noise[n_in * n_in];

    for (i=0; i<n_in; i++)
    {
        for (j=0; j<n_in; j++)
        {
            inputs_noise[i * n_in + j] = sig_inputs[i * n_in + j] + noise[i * n_in + j];
        }
    }

    gsl_matrix_view inputs_noise_matrix = gsl_matrix_view_array(inputs_noise, n_in, n_in);

    gsl_matrix_view gain_matrix = gsl_matrix_view_array(gain, n_in, n);
    double inputs_noise_inv[n_in * n_in];
    gsl_matrix_view inputs_noise_inv_matrix = gsl_matrix_view_array(inputs_noise_inv, n_in, n_in);

    int s;
    gsl_matrix * lu = gsl_matrix_alloc (n_in, n_in);
    gsl_permutation * p = gsl_permutation_alloc (n_in);
    gsl_linalg_LU_decomp(lu, p, &s);
    gsl_linalg_LU_invert(lu, p, &inputs_noise_inv_matrix.matrix);

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans, 1.0, &inputs_noise_inv_matrix.matrix,
            &jac_sig_matrix.matrix, 0.0, &gain_matrix.matrix); 

    for (i=0; i<n_in; i++)
    {
        for (j=0; j<n; j++)
        {
            gain[i * n + j] = gsl_matrix_get(&gain_matrix.matrix, i, j);
        }
    }

    for (i=0; i<n; i++)
    {
        for (j=0; j<n_in; j++)
        {
            gain_T[i * n_in + j] = gain[j * n + i];
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

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans, 1.0, &gain_T_matrix.matrix, 
            &residuals_matrix.matrix, 0.0, &dx_matrix.matrix);

    for (i=0; i<n; i++)
    {
        dx[i]     = gsl_matrix_get(&dx_matrix.matrix, i, 0);
        x_post[i] = x_prior[i] + dx[i];
    }
}

void Filter::calc_estimates(double* x, double* estimates)
{
    // linearized jacobian to back out linearized estimates
    
    int i,j;
    for (i=0; i<n_in; i++)
    {
        for (j=0; j<n; j++)
        {
            estimates[i] = jacobian[i*n + j] * x[j];
        }
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
        x_post[i]  = 0.0;
        for (j=0; j<n; j++)
        {
            if (i == j)
            {
                sig_prior[i*n + j] = 0.001;
                sig_post[i*n + j]  = 0.001;
            }
            else
            {
                sig_prior[i*n + j] = 0.0;
                sig_post[i*n + j]  = 0.0;
            }
        }
    }
}

void Filter::initarrays()
{
    x_prior   = (double*) calloc (n, sizeof(double));
    x_post    = (double*) calloc (n, sizeof(double));
    sig_prior = (double*) calloc (n * n, sizeof(double));
    sig_post  = (double*) calloc (n * n, sizeof(double));

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

    cout << "Deallocate Filter memory" << endl;

    }
}
