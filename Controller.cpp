#include "Controller.h"
#include <gperftools/profiler.h>

#include <iostream>
#include <cstring>

using namespace std;

Controller::Controller()
{
    mem_test = false;
}

Controller::Controller(bool& logger, string& model_type, int& n_filters)
{
    /* multi-filter controller runs multiple filters
    */
    ProfilerStart("/tmp/prof.out"); // memory profiler

    logging   = logger;
    model_typ = model_type;
    n_filt    = n_filters;

    initarrays();

    int i;
    for (i=0; i<n_filt; i++)
    {
        if(model_typ == "HarmonicModel")
        {
            filters[i].init_model(harmonic_model);
        }
        else if(model_typ == "VanderPolModel")
        {
            filters[i].init_model(vanderpol_model);
        }
        filter_state[i] = 0;
    }
}

void Controller::couple_filters_measurements()
{
    /* pair each filter with a measurement/carrier group
    */
    boot_filter(0);
}

void Controller::update_filters(double t, double* input_data)
{
    /* extended Kalman filter update
    */
    int i;
    for (i=0; i<n_filt; i++)
    {
        if (filter_state[i] == 1)
        {
            filters[i].propagate_update(t, input_data);
        }
    }
}

void Controller::boot_filter(int idx_filter)
{
    /* boot an individual filter instance
    */
    filter_state[idx_filter] = 1;
}

void Controller::shutdown_filter(int idx_filter)
{
    /* shutdown an individual filter instance
    */
    filter_state[idx_filter] = 0;
}

void Controller::initarrays()
{
    filter_state = (int*) calloc (n_filt, sizeof(int));

    mem_test = true;
}

Controller::~Controller()
{
    if(mem_test==true)
    {
    delete [] filter_state;
    }
}

