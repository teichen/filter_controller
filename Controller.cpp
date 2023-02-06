#include "Controller.h"
#include <gperftools/profiler.h>

using namespace std;

Controller::Controller()
{
}

Controller::Controller(bool& logger, string& model_type, int& n_filters)
{
    ProfilerStart("/tmp/prof.out"); // memory profiler

    logging   = logger;
    model_typ = model_type;
    n_filt    = n_filters;
}

void Controller::update_filters(double t)
{
}

void Controller::boot_filter(int idx_filter)
{
}

void Controller::shutdown_filter(int idx_filter)
{
}

Controller::~Controller()
{
}
