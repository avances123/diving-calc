from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING

class Round():
    """
    Rounding modes
    decimal.ROUND_CEILING
    Round towards Infinity.

    decimal.ROUND_DOWN
    Round towards zero.

    decimal.ROUND_FLOOR
    Round towards -Infinity.

    decimal.ROUND_HALF_DOWN
    Round to nearest with ties going towards zero.

    decimal.ROUND_HALF_EVEN
    Round to nearest with ties going to nearest even integer.

    decimal.ROUND_HALF_UP
    Round to nearest with ties going away from zero.

    decimal.ROUND_UP
    Round away from zero.

    decimal.ROUND_05UP
    Round away from zero if last digit after rounding towards zero would have been 0 or 5; otherwise round towards zero.
    """
    @staticmethod
    def round_floor(value:float):
        our_value = Decimal(value)
        output = Decimal(our_value.quantize(Decimal('.01'), 
        rounding=ROUND_FLOOR))
        return float(output)


    @staticmethod
    def round_ceil(value:float):
        our_value = Decimal(value)
        output = Decimal(our_value.quantize(Decimal('.01'), 
        rounding=ROUND_CEILING))
        return float(output)