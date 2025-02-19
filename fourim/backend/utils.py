from types import SimpleNamespace
from typing import Tuple

import numpy as np


def compare_angles(
    angle1: float | np.ndarray, angle2: float | np.ndarray
) -> np.ndarray:
    """Subtracts two angles and makes sure the are between -np.pi and +np.pi."""
    diff = np.array([angle1 - angle2])
    diff[diff > np.pi] -= 2 * np.pi
    diff[diff < -np.pi] += 2 * np.pi
    return diff


def get_param_value(param: SimpleNamespace):
    return param.value * param.unit


# TODO: Rewrite this with np.dot -> Should be faster
def transform_coordinates(
    x: float | np.ndarray,
    y: float | np.ndarray,
    cinc: float | None = None,
    pa: float | None = None,
    axis: str = "y",
) -> Tuple[float | np.ndarray, float | np.ndarray]:
    """Stretches and rotates the coordinate space depending on the
    cosine of inclination and the positional angle.

    Parameters
    ----------
    x: float or numpy.ndarray or astropy.units.Quantity
        The x-coordinate.
    y: float or numpy.ndarray or astropy.units.Quantity
        The y-coordinate.
    cinc: float, optional
        The cosine of the inclination.
    pa: float, optional
        The positional angle of the object (in degree).
    axis: str, optional
        The axis to stretch the coordinates on.

    Returns
    -------
    xt: float or numpy.ndarray
        Transformed x coordinate.
    yt: float or numpy.ndarray
        Transformed y coordinate.
    """
    if pa is not None:
        pa = np.deg2rad(pa)
        xt = x * np.cos(pa) - y * np.sin(pa)
        yt = x * np.sin(pa) + y * np.cos(pa)
    else:
        xt, yt = x, y

    if cinc is not None:
        if axis == "x":
            xt /= cinc
        elif axis == "y":
            xt *= cinc

    return xt, yt
