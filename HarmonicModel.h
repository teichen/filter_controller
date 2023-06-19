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

    int n;

    void initarrays();

    ~HarmonicModel();

private:
};

#endif
