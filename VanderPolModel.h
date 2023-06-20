// VanderPolModel.h
#ifndef _VANDERPOLMODEL
#define _VANDERPOLMODEL

#include "Model.h"

#include <iostream>

using namespace std;

class VanderPolModel : public Model
{
public:

    VanderPolModel();

    bool mem_test;

    void rate(double*, double*);
    void map_inputs_states(double*, double*);

    void initarrays();

    ~VanderPolModel();

private:
};

#endif
