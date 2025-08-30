"""
Variety of math and logic fuctions for ffmpeg evaluation during runtime.
"""

from typing import LiteralString


def f_abs(x) -> str:
    "Compute absolute value of x."
    return f"abs({x})"


def f_acos(x) -> str:
    "Compute arccosine of x."
    return f"acos({x})"


def f_asin(x) -> str:
    "Compute arcsine of x."
    return f"asin({x})"


def f_atan(x) -> str:
    "Compute arctangent of x."
    return f"atan({x})"


def f_atan2(y, x) -> str:
    """Compute principal value of the arc tangent of y/x."""
    return f"atan2({y}, {x})"


def f_between(x, min, max) -> str:
    "Return 1 if x is greater than or equal to min and lesser than or equal to max, 0 otherwise."
    return f"between({x}, {min}, {max})"


def f_bitand(x, y) -> str:
    "Compute bitwise and/or operation on x and y."
    return f"bitand({x}, {y})"


def f_bitor(x, y) -> str:
    """
    The results of the evaluation of x and y are converted to integers before executing the bitwise operation.
    Note that both the conversion to integer and the conversion back to floating point can lose precision. Beware of unexpected results for large numbers (usually 2^53 and larger).
    """
    return f"bitor({x}, {y})"


def f_ceil(expr) -> str:
    """Round the value of expression expr upwards to the nearest integer. For example, "ceil(1.5)" is "2.0"."""
    return f"ceil({expr})"


def f_clip(x, min, max) -> str:
    "Return the value of x clipped between min and max."
    return f"clip({x}, {min}, {max})"


def f_cos(x):
    "Compute cosine of x."
    return f"cos({x})"


def f_cosh(x) -> str:
    "Compute hyperbolic cosine of x."
    return f"cosh({x})"


def f_eq(x, y) -> str:
    "Return 1 if x and y are equivalent, 0 otherwise."
    return f"eq({x}, {y})"


def f_exp(x) -> str:
    "Compute exponential of x (with base e, the Euler’s number)."
    return f"exp({x})"


def f_floor(expr) -> str:
    'Round the value of expression expr downwards to the nearest integer. For example, "floor(-1.5)" is "-2.0".'
    return f"floor({expr})"


def f_gauss(x) -> str:
    "Compute Gauss function of x, corresponding to exp(-x*x/2) / sqrt(2*PI)."
    return f"gauss({x})"


def f_gcd(x, y) -> str:
    "Return f_the greatest common divisor of x and y. If both x and y are 0 or either or both are less than zero then behavior is undefined."
    return f"gcd({x}, {y})"


def f_gt(x, y) -> str:
    "Return 1 if x is greater than y, 0 otherwise."
    return f"gt({x}, {y})"


def f_gte(x, y) -> str:
    "Return 1 if x is greater than or equal to y, 0 otherwise."
    return f"gte({x}, {y})"


def f_hypot(x, y) -> str:
    'This function is similar to the C function with the same name; it returns "sqrt(x*x + y*y)", the length of the hypotenuse of a right triangle with sides of length x and y, or the distance of the point (x, y) from the origin.:'
    return f"hypot({x}, {y})"


def f_if(x, y, z) -> str:
    "Evaluate x, and if the result is non-zero return the evaluation result of y, otherwise the evaluation result of z."
    return f"if({x}, {y}, {z})"


def f_ifnot(x, y, z) -> str:
    "Evaluate x, and if the result is zero return the evaluation result of y, otherwise the evaluation result of z."
    return f"ifnot({x}, {y}, {z})"


def f_isinf(x) -> str:
    "Return 1.0 if x is +/-INFINITY, 0.0 otherwise."
    return f"isinf({x})"


def f_isnan(x) -> str:
    "Return 1.0 if x is NAN, 0.0 otherwise."
    return f"isnan({x})"


def f_ld(idx) -> str:
    "Load the value of the internal variable with index idx, which was previously stored with st(idx, expr). The function returns the loaded value."
    return f"ld({idx})"


def f_lerp(x, y, z) -> str:
    "Return linear interpolation between x and y by amount of z."
    return f"lerp({x}, {y}, {z})"


def f_log(x) -> str:
    "Compute natural logarithm of x."
    return f"log({x})"


def f_lt(x, y) -> str:
    "Return 1 if x is lesser than y, 0 otherwise."
    return f"lt({x}, {y})"


def f_lte(x, y) -> str:
    "Return 1 if x is lesser than or equal to y, 0 otherwise."
    return f"lte({x}, {y})"


def f_max(x, y) -> str:
    "Return the maximum between x and y."
    return f"max({x}, {y})"


def f_min(x, y) -> str:
    "Return the minimum between x and y."
    return f"min({x}, {y})"


def f_mod(x, y) -> str:
    "Compute the remainder of division of x by y."
    return f"mod({x}, {y})"


def f_not(expr) -> str:
    """Return 1.0 if expr is zero, 0.0 otherwise."""
    return f"not({expr})"


def f_pow(x, y) -> str:
    'Compute the power of x elevated y, it is equivalent to "(x)^(y)".'
    return f"pow({x}, {y})"


def f_print(t, l) -> str:
    """Pf_rint the value of expression t with loglevel l. If l is not specified then a default log level is used. Return the value of the expression printed.:"""
    return f"print({t}, {l})"


def f_random(idx) -> str:
    """
    Return a pseudo random value between 0.0 and 1.0. idx is the index of the internal variable used to save the seed/state, which can be previously stored with st(idx).
    To initialize the seed, you need to store the seed value as a 64-bit unsigned integer in the internal variable with index idx.
    For example, to store the seed with value 42 in the internal variable with index 0 and print a few random values:
    """
    return f"random({idx})"


def f_randomi(idx, min, max) -> str:
    """
    Return a pseudo random value in the interval between min and max. idx is the index of the internal variable which will be used to save the seed/state, which can be previously stored with st(idx).
    To initialize the seed, you need to store the seed value as a 64-bit unsigned integer in the internal variable with index idx.
    """
    return f"randomi({idx}, {min}, {max})"


def f_root(expr, max) -> str:
    """Find an input value for which the function represented by expr with argument ld(0) is 0 in the interval 0..max.

    The expression in expr must denote a continuous function or the result is undefif_ned.
    ld(0) is used to represent the function input value, which means that the given expression will be evaluated multiple times with various input values that the expression can access through ld(0). When the expression evaluates to 0 then the corresponding input value will be returned.
    """
    return f"root({expr}, {max})"


def f_round(expr) -> str:
    """Round the value of expression expr to the nearest integer. For example, "round(1.5)" is "2.0"."""
    return f"round({expr})"


def f_sgn(x) -> str:
    """Compute sign of x."""
    return f"sgn({x})"


def f_sin(x) -> str:
    "Compute sine of x."
    return f"sin({x})"


def f_sinh(x) -> str:
    "Compute hyperbolic sine of x."
    return f"sinh({x})"


def f_sqrt(expr) -> str:
    "Compute the square root of expr. This is equivalent to `(expr)^.5`"
    return f"sqrt({expr})"


def f_squish(x) -> str:
    "Compute expression 1/(1 + exp(4*x))."
    return f"squish({x})"


def f_st(idx, expr) -> str:
    """
    Store the value of the expression expr in an internal variable. idx specifies the index of the variable where to store the value, and it is a value ranging from 0 to 9. The function returns the value stored in the internal variable.

    The stored value can be retrieved with ld(var).

    Note: variables are currently not shared between expressions.
    """
    return f"st({idx}, {expr})"


def f_tan(x) -> str:
    "Compute tangent of x."
    return f"tan({x})"


def f_tanh(x) -> str:
    "Compute hyperbolic tangent of x."
    return f"tanh({x})"


def f_taylor(expr, x, idx) -> str:
    """
    Evaluate a Taylor series at x, given an expression representing the ld(idx)-th derivative of a function at 0.

    When the series does not converge the result is undefined.

    ld(idx) is used to represent the derivative order in expr, which means that the given expression will be evaluated multiple times with various input values that the expression can access through ld(idx). If idx is not specified then 0 is assumed.

    Note, when you have the derivatives at y instead of 0, taylor(expr, x-y) can be used.
    """
    return f"taylor({expr}, {x}, {idx})"


def f_time() -> LiteralString:
    "Return the current (wallclock) time in seconds."
    return f"time()"


def f_trunc(expr) -> str:
    "Round the value of expression expr towards zero to the nearest integer. For example, `trunc(-1.5)` is `-1.0`"
    return f"trunc({expr})"


def f_while(cond, expr) -> str:
    """
    Evaluate expression expr while the expression cond is non-zero, and returns the value of the last expr evaluation, or NAN if cond was always false.
    The following constants are available:
    """
    return f"while({cond}, {expr})"


PI = "PI"
"""Area of the unit disc, approximately 3.14"""
E = "E"
"""exp(1) (Euler’s number), approximately 2.718"""

PHI = "PHI"
"""golden ratio (1+sqrt(5))/2, approximately 1.618"""
