// Controller.h
#ifndef _CONTROLLER
#define _CONTROLLER

#include "HarmonicModel.h"
#include "VanderPolModel.h"
#include "Filter.h"

#include <iostream>

using namespace std;

class Controller
{
public:

    Controller();
    Controller(bool&, string&, int&);
    bool logging;
    string model_typ;
    int n_filt;

    bool mem_test;
    void initarrays();

    int* filter_state;

    Filter filters[10]; // TODO: configurable upper bound on n_filt
    HarmonicModel harmonic_model;
    VanderPolModel vanderpol_model;

    void couple_filters_measurements();
    void update_filters(double, double*, int*);
    void boot_filter(int);
    void shutdown_filter(int);

    ~Controller();

private:
};

#endif
