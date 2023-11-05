import numpy as np
from .common import *

def shift_left_(x, n):
    return x * (2 ** n)

def shift_right_(x, n):
    return x / (2 ** n)

class Quantize:

    """Fixed-point quantization scheme.

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
    def __init__(self, S, W, F, overflow: str = 'wrap', rounding: str = 'truncate') -> None:
        
        assert S in [True, False], 'Sign bit must be boolean.'
        assert W > 0, 'Word bit width must be positive.'
        assert overflow in FxpProps.overflow_dict.keys(), 'Overflow behavior must be one of ' + str(FxpProps.overflow_dict.keys())
        assert rounding in FxpProps.rounding_dict.keys(), 'Rounding behavior must be one of ' + str(FxpProps.rounding_dict.keys())
        self.S = S
        self.W = W
        self.F = F
        self.overflow: FxpProps.Overflow = FxpProps.overflow_dict[overflow.lower()]
        self.rounding: FxpProps.Rounding = FxpProps.rounding_dict[rounding.lower()]
        self.v_min = FxpProps.vMin(self.S, self.W, self.F)
        self.v_max = FxpProps.vMax(self.S, self.W, self.F)
        self.v_range = FxpProps.vRange(self.S, self.W, self.F)
        self.v_precision = FxpProps.vPrecision(self.S, self.W, self.F)
        self.v_min_int = FxpProps.vMinInt(self.S, self.W)
        self.v_max_int = FxpProps.vMaxInt(self.S, self.W)
        self.v_range_int = FxpProps.vRangeInt(self.S, self.W)
        pass

    def asBitsInt(self, x):
        """Get the integer representation of the quantized fixed-point number (from float-point).

        This considers the :class:`~rtlsim.FxpProps.Overflow` behavior and the :class:`~rtlsim.FxpProps.Rounding` behavior.

        :param x: Fixed-point number
        :type x: Float or ``numpy.ndarray``
        :return: Scaled integer value of the fixed-point number
        :rtype: Integer-valued float or ``numpy.ndarray``
        """
        raw_v = shift_left_(x, self.F) # shift left by F, which is still float | numpy.ndarray
        # Overflow behavior
        if self.overflow == FxpProps.Overflow.WRAP:
            clipped_v = raw_v % (1 << self.W)
            if self.S and clipped_v > self.v_max_int: # should be a negative value
                clipped_v = clipped_v - self.v_range_int
        else: # self.overflow == FxpProps.Overflow.SATURATE
            clipped_v = np.clip(raw_v, self.v_min_int, self.v_max_int)
        # Rounding behavior
        if self.rounding == FxpProps.Rounding.TRUNCATE:
            rounded_v = np.floor(clipped_v)
        elif self.rounding == FxpProps.Rounding.AROUND:
            rounded_v = np.round(clipped_v)
        elif self.rounding == FxpProps.Rounding.FLOOR:
            rounded_v = np.floor(clipped_v)
        elif self.rounding == FxpProps.Rounding.CEIL:
            rounded_v = np.ceil(clipped_v)
        elif self.rounding == FxpProps.Rounding.FIX:
            rounded_v = np.fix(clipped_v)
        else:
            raise NotImplementedError
        return rounded_v
    
    def asBitsUInt(self, x):
        """Get the unsigned integer representation of the quantized fixed-point number (from float-point).

        This considers the :class:`~rtlsim.FxpProps.Overflow` behavior and the :class:`~rtlsim.FxpProps.Rounding` behavior.

        :param x: Fixed-point number
        :type x: Float or ``numpy.ndarray``
        :return: Scaled unsigned integer value of the fixed-point number
        :rtype: Unsigned integer-valued float or ``numpy.ndarray``
        """
        rounded_v = self.asBitsInt(x)
        return rounded_v + self.v_range_int if rounded_v < 0 else rounded_v

    def asBits(self, x):
        """Get the string bits representation of the quantized fixed-point number (from float-point).

        :param x: Fixed-point number
        :type x: Float or ``numpy.ndarray``
        :return: String bits representation of the fixed-point number
        :rtype: String or ``numpy.ndarray`` of strings
        """
        rounded_v = self.asBitsInt(x)
        # if rounded_v is numpy.ndarray, then np.binary_repr will return a list of strings
        if isinstance(rounded_v, np.ndarray):
            return np.array([np.binary_repr(int(rounded_v_), width=self.W) for rounded_v_ in rounded_v.flatten()]).reshape(rounded_v.shape)
        else:
            return np.binary_repr(int(rounded_v), width=self.W)
    
    def quantize(self, x):
        """Quantize the fixed-point number (from float-point).

        This considers the :class:`~rtlsim.FxpProps.Overflow` behavior and the :class:`~rtlsim.FxpProps.Rounding` behavior.

        :param x: Fixed-point number
        :type x: Float or ``numpy.ndarray``
        :return: Quantized fixed-point number
        :rtype: Float or ``numpy.ndarray``
        """
        rounded_v = self.asBitsInt(x)
        return rounded_v / (2 ** self.F)
    
    def quantizeSelf(self, x):
        """Quantize the fixed-point number (from float-point) in-place.

        :param x: ``numpy.ndarray`` of fixed-point numbers
        :type x: ``numpy.ndarray``
        :raises TypeError: If ``x`` is not a ``numpy.ndarray``

        This considers the :class:`~rtlsim.FxpProps.Overflow` behavior and the :class:`~rtlsim.FxpProps.Rounding` behavior.

        .. Caution::
            The input ``x`` must be a ``numpy.ndarray``.
        """
        if not isinstance(x, np.ndarray):
            raise TypeError('Input must be a numpy.ndarray.')
        x[:] = self.quantize(x)

    q = quantize
    """Alias for :meth:`~rtlsim.Quantize.quantize`"""

    qs = quantizeSelf
    """Alias for :meth:`~rtlsim.Quantize.quantizeSelf`"""

def quantize(x, S, W, F, overflow: str = 'wrap', rounding: str = 'truncate'):
    """Quantize the fixed-point number (from float-point).

    This function internally creates a :class:`~rtlsim.Quantize` object and calls :meth:`~rtlsim.Quantize.quantize`.

    :param x: Fixed-point number
    :type x: Float or ``numpy.ndarray``
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
    :return: Quantized fixed-point number
    :rtype: Float or ``numpy.ndarray``
    """
    return Quantize(S, W, F, overflow, rounding).quantize(x)

def quantizeSelf(x, S, W, F, overflow: str = 'wrap', rounding: str = 'truncate'):
    """Quantize the fixed-point number (from float-point) in-place.

    This function internally creates a :class:`~rtlsim.Quantize` object and calls :meth:`~rtlsim.Quantize.quantizeSelf`.

    :param x: ``numpy.ndarray`` of fixed-point numbers
    :type x: ``numpy.ndarray``
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
    :raises TypeError: If ``x`` is not a ``numpy.ndarray``

    .. Caution::
        The input ``x`` must be a ``numpy.ndarray``.
    """
    Quantize(S, W, F, overflow, rounding).quantizeSelf(x)
