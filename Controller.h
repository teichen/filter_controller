// Controller.h
#ifndef _CONTROLLER
#define _CONTROLLER

using namespace std;

class Controller
{
public:

    Controller();

    void update_filters(double);
    void boot_filter(int);
    void shutdown_filter(int);

    ~Controller();

private:
};

#endif
