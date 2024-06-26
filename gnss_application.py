import ctypes
from ctypes import c_void_p, c_double, c_int, c_size_t, POINTER, pointer
import os
import sys
import numpy as np
from numpy import random
from memory_profiler import profile

# set seed
random.seed(10)

INPUT_BUFFER_SIZE = 200
PRN_BUFFER_SIZE   = 1023

@profile
def filter_data():
    """
    """
    path = os.path.dirname(__file__)
    multifilter_controller = ctypes.CDLL(os.path.join(path, "multifilter_controller.dylib"))

    # dynamic memory allocation handled by dylib
    allocate_inputs = multifilter_controller.allocate_inputs
    allocate_inputs.restype = POINTER(c_double * INPUT_BUFFER_SIZE)
    inputs    = allocate_inputs()

    allocate_prn_codes = multifilter_controller.allocate_prn_codes
    allocate_prn_codes.restype = POINTER(c_int * (INPUT_BUFFER_SIZE * PRN_BUFFER_SIZE))
    prn_codes = allocate_prn_codes()

    run = multifilter_controller.run
    run.restype  = c_void_p
    run.argtypes = [POINTER(c_double * INPUT_BUFFER_SIZE), POINTER(c_int * (INPUT_BUFFER_SIZE * PRN_BUFFER_SIZE))]

    # define inputs {transmission_time (float), carrier_id (int), carrier_freq (float), 
    #                carrier_phase (float)}
    # define prn_codes (PRN_BUFFER_SIZE ints each)
    n_inputs = 10
    times         = np.linspace(0, n_inputs-1, num=n_inputs).reshape((n_inputs, 1))
    carrier_id    = 1 * np.ones((n_inputs, 1))
    carrier_freq  = 1575.42 * np.ones((n_inputs, 1)) # MHz
    carrier_phase = random.rand(n_inputs).reshape((n_inputs, 1))

    prn_code = [create_prn_code() for idx in range(n_inputs)]

    for idx in range(n_inputs):
        inputs.contents[idx * 4]     = times[idx]
        inputs.contents[idx * 4 + 1] = carrier_id[idx]
        inputs.contents[idx * 4 + 2] = carrier_freq[idx]
        inputs.contents[idx * 4 + 3] = carrier_phase[idx]
        for prn_element in range(PRN_BUFFER_SIZE):
            prn_codes.contents[idx * PRN_BUFFER_SIZE + prn_element] = prn_code[idx][prn_element]

    run(inputs, prn_codes)

    free_inputs = multifilter_controller.free_inputs
    free_inputs.restype  = c_void_p
    free_inputs.argtypes = [POINTER(c_double * INPUT_BUFFER_SIZE)]
    free_inputs(inputs)

    free_prn_codes = multifilter_controller.free_prn_codes
    free_prn_codes.restype  = c_void_p
    free_prn_codes.argtypes = [POINTER(c_int * (INPUT_BUFFER_SIZE * PRN_BUFFER_SIZE))]
    free_prn_codes(prn_codes)

def create_prn_code():
    """
    """
    prn_code = [int(prn_element) for prn_element in np.array(np.floor(0.5 + random.rand(PRN_BUFFER_SIZE)))]

    return prn_code

if __name__ == "__main__":
    filter_data()
