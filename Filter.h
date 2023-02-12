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
    void initarrays();

    void propagate_update(double);

    ~Filter();

private:
};

#endif
