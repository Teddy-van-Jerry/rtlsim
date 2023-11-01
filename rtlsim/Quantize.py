import numpy as np

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
    class Overflow:
        """Overflow behavior
        """
        WRAP = 0
        """Wrap around (default behavior)"""
        SATURATE = 1

    class Rounding:
        """Rounding behavior
        """
        TRUNCATE = 0
        """Truncate the fractional part (default behavior)"""
        AROUND = 1
        FLOOR = 2
        CEIL = 3
        FIX = 4

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
        :param overflow: :class:`~rtlsim.Quantize.Overflow` behavior, defaults to :code:`'wrap'`
        :type overflow: str, optional
        :param rounding: :class:`~rtlsim.Quantize.Rounding` behavior, defaults to :code:`'truncate'`
        :type rounding: str, optional
        """
        self.S = S
        self.W = W
        self.F = F
        overflow_dict = {
            'wrap': self.Overflow.WRAP,
            'saturate': self.Overflow.SATURATE,
        }
        rounding_dict = {
            'truncate': self.Rounding.TRUNCATE,
            'around': self.Rounding.AROUND,
            'floor': self.Rounding.FLOOR,
            'ceil': self.Rounding.CEIL,
            'fix': self.Rounding.FIX,
        }
        self.overflow: self.Overflow = overflow_dict[overflow.lower()]
        self.rounding: self.Rounding = rounding_dict[rounding.lower()]
        pass
