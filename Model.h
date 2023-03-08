// Model.h
#ifndef _MODEL
#define _MODEL

#include <iostream>

using namespace std;

class Model
{
public:

    Model();
    
    int n_states;

    double* linearized_rate;

    ~Model();

private:
};

#endif
