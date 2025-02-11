from types import SimpleNamespace
from typing import Tuple

import astropy.units as u
import numpy as np


def compare_angles(angle1: float | np.ndarray, angle2: float | np.ndarray) -> np.ndarray:
    """Subtracts two angles and makes sure the are between -np.pi and +np.pi."""
    diff = np.array([angle1 - angle2])
    diff[diff > np.pi] -= 2 * np.pi
    diff[diff < -np.pi] += 2 * np.pi
    return diff


def get_param_value(param: SimpleNamespace):
    return param.value * param.unit


# TODO: Rewrite this with np.dot -> Should be faster
def convert_coords_to_polar(
    x: float | np.ndarray,
    y: float | np.ndarray,
    cinc: float | None = None,
    pa: float | None = None,
    deg: bool = False,
) -> Tuple[float | np.ndarray, float | np.ndarray]:
    """Calculates the effective baselines from the projected baselines
    in mega lambda.

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
    deg : bool, optional
        If True, the angle will be returned in degree.

    Returns
    -------
    distance : float or numpy.ndarray
        Returns the distance to the point.
    angle : float or numpy.ndarray
        Returns the angle of the point (radians or degree
        if "deg=True").
    """
    if pa is not None:
        pa = np.deg2rad(pa)
        xr = x * np.cos(pa) - y * np.sin(pa)
        yr = x * np.sin(pa) + y * np.cos(pa)
    else:
        xr, yr = x, y

    if cinc is not None:
        xr *= cinc

    theta = np.arctan2(xr, yr)
    return np.hypot(xr, yr), np.rad2deg(theta) if deg else theta


def translate_vis(
    spf: np.ndarray, psi: np.ndarray, params: SimpleNamespace
) -> np.ndarray:
    """Translation in Fourier space."""
    x = get_param_value(params.x).to(u.rad).value
    y = get_param_value(params.y).to(u.rad).value
    uv = np.exp(1j * x * np.cos(psi)) * np.exp(1j * y * np.sin(psi))
    return np.exp(2j * np.pi * spf * np.angle(uv))


def translate_img(x: np.ndarray, y: np.ndarray, params: SimpleNamespace) -> Tuple:
    """Shifts the coordinates in image space according to an offset."""
    x0 = get_param_value(params.x).value
    y0 = get_param_value(params.y).value
    return x - x0, y - y0
