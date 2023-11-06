"""Common definitions for the RTL Sim
"""

class FxpProps:
    """Fixed-point properties.
    """
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
    
    overflow_dict = {
        'wrap': Overflow.WRAP,
        'saturate': Overflow.SATURATE,
    }
    rounding_dict = {
        'truncate': Rounding.TRUNCATE,
        'around': Rounding.AROUND,
        'floor': Rounding.FLOOR,
        'ceil': Rounding.CEIL,
        'fix': Rounding.FIX,
    }
    overflow_options = list(overflow_dict.keys())
    rounding_options = list(rounding_dict.keys())

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'FxpProps()'
    
    @staticmethod
    def vMinInt(S, W):
        """Minimum value of the integer number (disregarding :code:`F`).

        :param S: Sign bit (:code:`True` for signed, :code:`False` for unsigned)
        :type S: boolean
        :param W: Word bit width
        :type W: positive integer
        """
        return -(1 << (W - 1)) if S else 0
    
    @staticmethod
    def vMin(S, W, F):
        """Minimum value of the fixed-point number.

        :param S: Sign bit (:code:`True` for signed, :code:`False` for unsigned)
        :type S: boolean
        :param W: Word bit width
        :type W: positive integer
        :param F: Fractional bit width
        :type F: integer
        """
        return FxpProps.vMinInt(S, W) / (2 ** F)
    
    @staticmethod
    def vMaxInt(S, W):
        """Maximum value of the integer number (disregarding :code:`F`).

        :param S: Sign bit (:code:`True` for signed, :code:`False` for unsigned)
        :type S: boolean
        :param W: Word bit width
        :type W: positive integer
        """
        return (1 << (W - 1)) - 1 if S else (1 << W) - 1
    
    @staticmethod
    def vMax(S, W, F):
        """Maximum value of the fixed-point number.

        :param S: Sign bit (:code:`True` for signed, :code:`False` for unsigned)
        :type S: boolean
        :param W: Word bit width
        :type W: positive integer
        :param F: Fractional bit width
        :type F: integer
        """
        return FxpProps.vMaxInt(S, W) / (2 ** F)

    @staticmethod
    def vRangeInt(S, W):
        """Range of the integer number (disregarding :code:`F`).

        :param S: Sign bit (:code:`True` for signed, :code:`False` for unsigned)
        :type S: boolean
        :param W: Word bit width
        :type W: positive integer
        """
        return FxpProps.vMaxInt(S, W) - FxpProps.vMinInt(S, W)

    @staticmethod
    def vRange(S, W, F):
        """Range of the fixed-point number.

        :param S: Sign bit (:code:`True` for signed, :code:`False` for unsigned)
        :type S: boolean
        :param W: Word bit width
        :type W: positive integer
        :param F: Fractional bit width
        :type F: integer
        """
        return FxpProps.vMax(S, W, F) - FxpProps.vMin(S, W, F)

    @staticmethod
    def vPrecision(F):
        """Precision of the fixed-point number (:math:`2^{-F}`).

        :param F: Fractional bit width
        :type F: integer
        """
        return 1 / (2 ** F)
