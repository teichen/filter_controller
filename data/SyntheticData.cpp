#include "SyntheticData.h"

#include <cstdio>

using namespace std;

SyntheticData::SyntheticData()
{
    /* generate regularized continuous data on a 5 sec period,
       Normally distributed values about equilibrium points,
       also irregular data with Poisson-distributed measurement times (e.g. 4 times per day)
    */
}

// TODO: read from disk

// TODO: remove data from disk, std::remove("./file.txt")

SyntheticData::~SyntheticData()
{
}
