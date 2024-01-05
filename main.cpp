#include <iostream>
#include <gperftools/profiler.h>

extern "C" {
#include "Controller.h"
}

using namespace std;

const int INPUT_BUFFER_SIZE = 100;
const int PRN_BUFFER_SIZE   = 1023;

extern "C" {
    double* allocate_inputs(){
    double* inputs;
    inputs = (double*) calloc(INPUT_BUFFER_SIZE, sizeof(double));
    return inputs;
    }
}

extern "C" {
    int* allocate_prn_codes(){
    int* prn_codes;
    prn_codes = (int*) calloc(INPUT_BUFFER_SIZE * PRN_BUFFER_SIZE, sizeof(int));
    return prn_codes;
    }
}

extern "C" {
    void free_inputs(double* inputs){
    delete [] inputs;
    }
}

extern "C" {
    void free_prn_codes(int* prn_codes){
    delete [] prn_codes;
    }
}

extern "C" {
    void run(double *inputs, int *prn_codes){
    // inputs: 4-pairs of
    //     timestamp (float)
    //     carrier_id (int)
    //     carrier_freq (float)
    //     carrier_phase (float)}
    // prn_codes: array of prn_codes (PRN_BUFFER_SIZE ints each)

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
    int prn_code_t[PRN_BUFFER_SIZE];

    // boot/pair inputs and filters
    multifilter_controller.couple_filters_measurements();

    // test first time
    t = inputs[0];
    input_data_t[0] = inputs[1];
    input_data_t[1] = inputs[2];
    input_data_t[2] = inputs[3];

    for (int i=0; i<PRN_BUFFER_SIZE; i++)
    {
        prn_code_t[i] = prn_codes[0*PRN_BUFFER_SIZE + i];
    }

    multifilter_controller.update_filters(t, input_data_t, prn_code_t);

    ProfilerStop();
    }
}

int main()
{
    double inputs[4];
    inputs[0] = 0.0; inputs[1] = 0.2; inputs[2] = 0.0; inputs[3] = 0.0;

    int prn_codes[PRN_BUFFER_SIZE];
    for (int i=0; i<PRN_BUFFER_SIZE; i++)
    {
        prn_codes[i] = 0;
    }

    run(inputs, prn_codes);
    return 0;
}
