// HarmonicModel.h
#ifndef _HARMONICMODEL
#define _HARMONICMODEL

#include "Model.h"

#include <iostream>

using namespace std;

class HarmonicModel : public Model
{
public:

    HarmonicModel();

    bool mem_test;

    void rate(double*, double*);
    void map_inputs_states(double*, double*);

    void initarrays();

    ~HarmonicModel();

private:
};

#endif
