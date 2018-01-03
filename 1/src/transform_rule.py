
from aenum import Enum, auto


class TransformationRule(Enum):

    # Rules for basic operations
    NEGATIVE = auto()
    MINUS = auto()
    DIVIDE = auto()
    LOGARITHM = auto()

    # Rule about basic laws of algebra
    COMMUTATION = auto()
    ASSOCIATION = auto()
    DISTRIBUTION = auto()

    # Rules for fractions
    COMM_DENOMINATOR = auto()
    FRAC_REDUCTION = auto()
    NUMERATOR_FORM = auto()
    DENOMINATOR_FORM = auto()

    # Rules for polynomial transitions
    ACCUMULATION = auto()
    HORNER_FORM = auto()
    SHIFT = auto()

    # Rules about trigonometric functions
    TAN = auto()
    SEC = auto()
    COT = auto()
    CSC = auto()
    SIN_PLUS = auto()
    COS_PLUS = auto()

    # Rules about Taylor series
    TAYLOR_EXP = auto()
    TAYLOR_LN = auto()
    TAYLOR_SIN = auto()
    TAYLOR_COS = auto()

    # Rules for complex numbers
    POLAR_REPRESENTATION = auto()

    # Rules about gamma function
    STIRLING_GAMMA = auto()
    GAMMA_TRANS = auto()
    GAMMA_0 = auto()
    GAMMA_MINUS_1 = auto()
    GAMMA_MINUS_2 = auto()


def apply_rule(path, rule):
    return None

