#include "RungeKutta.h"

using namespace std;

RungeKutta::RungeKutta()
{
}

void RungeKutta::propagate(double t0, double tf, double dt, TODO rate, double* x_prior)
{
    /* classic Runge-Kutta method (RK4)
       dy/dt = f(t,y) ; y(t0) = x_prior
       further assume autonomous, f(t,y) = f(y)
   
       Args:
                t0 (double)     : initial time
                tf (double)     : final time
                dt (double)     : time interval step size
                rate
                x_prior (array) : mean prior estimate
    */
    double t;

    t = t0;
    while (t < tf)
    {
        t += dt
        k1 = rate(x_prior);
        k2 = rate(x_prior + 0.5 * dt * k1);
        k3 = rate(x_prior + 0.5 * dt * k2);
        k4 = rate(x_prior + dt * k3);

        x_prior += (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4);
        t0 = t
    }
}

RungeKutta::~RungeKutta()
{
}
