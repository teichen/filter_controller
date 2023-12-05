import ctypes
import os
import sys
import numpy as np

path = os.path.dirname(__file__)
shared_controller = ctypes.CDLL(os.path.join(path, "multifilter_run.dylib"))

_multifilter_run = shared_controller.multifilter_run
