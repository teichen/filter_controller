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
    
    void rate(double*, double*);

    void initarrays();

    ~VanderPolModel();

private:
};

#endif
