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

void Controller::couple_filters_measurements()
{
    /* pair each filter with a measurement
       based on the measurement frequency,
       first filter processes regularizes the measurement
       times and dampens the measurement noise for the highest
       frequency measurement, the second filter the second highest
       frequency measurement, and so on
    */
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
