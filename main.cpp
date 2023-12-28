#include <iostream>
#include <gperftools/profiler.h>

extern "C" {
#include "Controller.h"
}

using namespace std;

extern "C" {
    double* allocate_inputs(){
    double* inputs;
    inputs = (double*) calloc(100, sizeof(double));
    return inputs;
    }
}

extern "C" {
    void free_inputs(double* inputs){
    delete [] inputs;
    }
}

extern "C" {
    void run(double *inputs){
    // inputs: 4-pairs of
    //     timestamp (float)
    //     carrier_id (int)
    //     carrier_freq (float)
    //     carrier_phase (float)}

    ProfilerStart("/tmp/prof.out"); // memory profiler

    bool logging;
    string model_type;
    int n_filters;

    logging    = 0;
    model_type = "HarmonicModel";
    n_filters  = 4;

    // TODO instantiate controller
    Controller multifilter_controller(logging, model_type, n_filters);

    // process data (measurement data subject to corruption noise)
    double t;
    double input_data_t[3];

    // boot/pair inputs and filters
    multifilter_controller.couple_filters_measurements();

    // test first time
    t = inputs[0];
    input_data_t[0] = inputs[1];
    input_data_t[1] = inputs[2];
    input_data_t[2] = inputs[3];

    multifilter_controller.update_filters(t, input_data_t);

    ProfilerStop();
    }
}

int main()
{
    double inputs[4];
    inputs[0] = 0.0; inputs[1] = 0.2; inputs[2] = 0.0; inputs[3] = 0.0;
    run(inputs);
    return 0;
}
