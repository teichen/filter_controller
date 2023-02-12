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
    
    void rate(double);

    ~HarmonicModel();

private:
};

#endif
