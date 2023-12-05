#include <iostream>

extern "C" {
#include "Controller.h"
}

using namespace std;

extern "C" {
    void multifilter_run(void);
}

extern "C" void multifilter_run(void){
    bool logging;
    string model_type;
    int n_filters;

    logging    = 0;
    model_type = "Harmonic";
    n_filters  = 4;

    // TODO: measurement data subject to corruption noise
    Controller process_data(logging, model_type, n_filters);
}

int main()
{
    return 0;
}
