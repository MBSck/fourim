from typing import Tuple

import astropy.units as u
import numpy as np


def compute_effective_baselines(
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
        ucoord_eff = ucoord * np.cos(pos_angle) - vcoord * np.sin(pos_angle)
        vcoord_eff = ucoord * np.sin(pos_angle) + vcoord * np.cos(pos_angle)
    else:
        ucoord_eff, vcoord_eff = ucoord, vcoord

    if inclination is not None:
        ucoord_eff *= inclination

    baselines_eff = np.hypot(ucoord_eff, vcoord_eff)
    baseline_angles_eff = np.arctan2(vcoord_eff, ucoord_eff)

    if longest:
        indices = baselines_eff.argmax(0)
        iteration = np.arange(baselines_eff.shape[1])
        baselines_eff = baselines_eff[indices, iteration]
        baseline_angles_eff = baseline_angles_eff[indices, iteration]

    return baselines_eff.squeeze(), baseline_angles_eff.squeeze()
