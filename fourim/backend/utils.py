from types import SimpleNamespace
from typing import Tuple

import astropy.units as u
import numpy as np


def get_param_value(param: SimpleNamespace):
    return param.value * param.unit


def compute_image_grid(
    xcoord: u.mas,
    ycoord: u.mas,
    inclination: u.Quantity[u.one] | None = None,
    pos_angle: u.Quantity[u.deg] | None = None,
) -> Tuple[u.Quantity[u.mas], u.Quantity[u.mas]]:
    if pos_angle is not None:
        pos_angle = pos_angle.to(u.rad)
        xcoord_rot = xcoord * np.cos(pos_angle) - ycoord * np.sin(pos_angle)
        ycoord_rot = xcoord * np.sin(pos_angle) + ycoord * np.cos(pos_angle)
    else:
        xcoord_rot, ycoord_rot = xcoord, ycoord

    if inclination is not None:
        xcoord_rot *= inclination

    rho = np.hypot(xcoord_rot, ycoord_rot)
    theta = np.arctan2(ycoord_rot, xcoord_rot)
    return rho.squeeze(), theta.squeeze()


def translate_img(x: u.mas, y: u.mas, params: SimpleNamespace) -> Tuple:
    """Shifts the coordinates in image space according to an offset."""
    x0, y0 = get_param_value(params.x), get_param_value(params.y)
    return x - x0.to(u.rad), y - y0.to(u.rad)


def compute_baselines(
    ucoord: u.m,
    vcoord: u.m,
    inclination: u.Quantity[u.one] | None = None,
    pos_angle: u.Quantity[u.deg] | None = None,
    longest: bool | None = False,
) -> Tuple[u.Quantity[u.m], u.Quantity[u.one]]:
    """Calculates the effective baselines from the projected baselines
    in mega lambda.

    Parameters
    ----------
    ucoord: astropy.units.m
        The u coordinate.
    vcoord: astropy.units.m
        The v coordinate.
    inclination: astropy.units.one
        The inclinatin induced compression of the x-axis.
    pos_angle: astropy.units.deg
        The positional angle of the object
    longest : bool, optional
        If True, the longest baselines are returned.

    Returns
    -------
    baselines : astropy.units.m
        Returns the effective baselines.
    baselines_angles : astropy.units.rad
        Returns the effective baseline angles.
    """
    if pos_angle is not None:
        pos_angle = pos_angle.to(u.rad)
        ucoord_rot = ucoord * np.cos(pos_angle) - vcoord * np.sin(pos_angle)
        vcoord_rot = ucoord * np.sin(pos_angle) + vcoord * np.cos(pos_angle)
    else:
        ucoord_rot, vcoord_rot = ucoord, vcoord

    if inclination is not None:
        ucoord_rot *= inclination

    spf = np.hypot(ucoord_rot, vcoord_rot)
    psi = np.arctan2(vcoord_rot, ucoord_rot)

    if longest:
        indices = spf.argmax(0)
        iteration = np.arange(spf.shape[1])
        spf = spf[indices, iteration]
        psi = psi[indices, iteration]

    return spf.squeeze(), psi.squeeze()


def translate_vis(spf: 1 / u.rad, psi: u.rad, params: SimpleNamespace) -> np.ndarray:
    """Translation in Fourier space."""
    x, y = get_param_value(params.x).to(u.rad), get_param_value(params.y).to(u.rad)
    uv = np.exp(1j * x.value * np.cos(psi)) * np.exp(1j * y.value * np.sin(psi))
    return np.exp(2j * np.pi * spf * np.angle(uv))


