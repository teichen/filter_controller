import ctypes
from ctypes import c_size_t
import os
import sys
import numpy as np

path = os.path.dirname(__file__)
multifilter_controller = ctypes.CDLL(os.path.join(path, "multifilter_controller.dylib"))

run = multifilter_controller.run

run.restype = None
run.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags="C"), c_size_t]

inputs = np.ones(100, np.float64)
res = run(inputs, inputs.size)

print(res)

