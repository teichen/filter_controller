// Filter.h
#ifndef _FILTER
#define _FILTER

using namespace std;

class Filter
{
public:

    bool mem_test;

    Filter();

    int n_states;
    void initarrays();

    void propagate_update(double);

    ~Filter();

private:
};

#endif
