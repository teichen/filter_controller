#include "Controller.h"
#include <gperftools/profiler.h>

#include <iostream>
#include <cstring>

using namespace std;

Controller::Controller()
{
}

Controller::Controller(bool& logger, string& model_type, int& n_filters)
{
    /* multi-filter controller runs multiple filters
    */
    ProfilerStart("/tmp/prof.out"); // memory profiler

    logging   = logger;
    model_typ = model_type;
    n_filt    = n_filters;

    if(model_typ == "HarmonicModel")
    {
        filter.init_model(harmonic_model);
    }
    else if(model_typ == "VanderPolModel")
    {
        filter.init_model(vanderpol_model);
    }
}

void Controller::update_filters(double t)
{
    /* extended Kalman filter update
    */
}

void Controller::boot_filter(int idx_filter)
{
    /* boot an individual filter instance
    */
}

void Controller::shutdown_filter(int idx_filter)
{
    /* shutdown an individual filter instance
    */
}

Controller::~Controller()
{
}
