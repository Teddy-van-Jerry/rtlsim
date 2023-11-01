import numpy as np
from .common import *

def shift_left_(x, n):
    return x * (2 ** n)

def shift_right_(x, n):
    return x / (2 ** n)

def round_(x):
    return np.round(x)

def clip_(x, dwt):
    min_v = -(1 << (dwt - 1))
    max_v = (1 << (dwt - 1)) - 1
    return np.clip(x, min_v, max_v)

class Quantize:

    """Fixed-point quantization
    """
    def __init__(self, S, W, F, overflow: str = 'wrap', rounding: str = 'truncate') -> None:
        """Initialize the fixed-point quantization scheme.

        :param S: Sign bit (:code:`True` for signed, :code:`False` for unsigned)
        :type S: boolean
        :param W: Word bit width
        :type W: positive integer
        :param F: Fractional bit width
        :type F: integer
        :param overflow: :class:`~rtlsim.FxpProps.Overflow` behavior, defaults to :code:`'wrap'`
        :type overflow: str, optional
        :param rounding: :class:`~rtlsim.FxpProps.Rounding` behavior, defaults to :code:`'truncate'`
        :type rounding: str, optional
        """
        assert S in [True, False], 'Sign bit must be boolean.'
        assert W > 0, 'Word bit width must be positive.'
        assert overflow in FxpProps.overflow_dict.keys(), 'Overflow behavior must be one of ' + str(FxpProps.overflow_dict.keys())
        assert rounding in FxpProps.rounding_dict.keys(), 'Rounding behavior must be one of ' + str(FxpProps.rounding_dict.keys())
        self.S = S
        self.W = W
        self.F = F
        self.overflow: FxpProps.Overflow = FxpProps.overflow_dict[overflow.lower()]
        self.rounding: FxpProps.Rounding = FxpProps.rounding_dict[rounding.lower()]
        pass
