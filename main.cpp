#include <iostream>
#include <fstream>
#include <stdlib.h>
using std::cerr;
using std::cout;
using std::endl;
#include <sstream>
using std::ifstream;
#include <cstring>
#include <cstdlib>

#include "Controller.h"

using namespace std;

int main(int argc, char* argv[])
{
    // TODO: parse inputs
    // TODO: measurement data subject to corruption noise
    // TODO: execute multi-filter system using the Controller

    cout << "Program Running..." << endl;
    cout << "" << endl;

    if (argc != 4)
    {
        if (argv[0])
            std::cout << "Usage: " << argv[0] << " <logging> <model> <n_filters>" << '\n';
        else
            std::cout << "Usage: multifilter_run <logging> <model> <n_filters>" << '\n';
        
        exit(1);
    }

    std::stringstream logging_input(argv[1]);
    std::stringstream model_input(argv[2]);
    std::stringstream n_filters_input(argv[3]);

    bool logging;
    string model;
    int n_filters;

    if (!(logging_input >> logging))
        logging = false;
    if (!(model_input >> model))
        model = "";
    if (!(n_filters_input >> n_filters))
        n_filters = -1;

    Controller multifilter_run(logging, model, n_filters); 

    cout << "Program Exiting..." << endl;
    cout << "" << endl;

    return 0;
}
