// Filter.h
#ifndef _FILTER
#define _FILTER

#include "Model.h"
#include "RungeKutta.h"

#include <iostream>

using namespace std;

class Filter
{
public:

    bool mem_test;

    Filter();
    void init_model(Model&);

    int n;
    double* x_post;
    double* x_prior;
    double* sig_post;
    double* sig_prior;
    double* jacobian_linearized;

    double t0;

    void initialize_state();
    void initarrays();

    void propagate_update(double);

    void set_prior(double*, double*);
    void set_posterior(double*, double*);
    void update(double*);

    ~Filter();

private:
};

#endif
