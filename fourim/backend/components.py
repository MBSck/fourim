import copy
import inspect
from types import SimpleNamespace

import astropy.units as u
import numpy as np
from scipy.special import j0, j1, jv

from ..config.options import OPTIONS
from .utils import compare_angles, get_param_value


def make_component(name: str) -> SimpleNamespace:
    """Makes a component from the presets."""
    current_module = inspect.getmodule(inspect.currentframe())
    functions = dict(inspect.getmembers(current_module, inspect.isfunction))
    available_components = OPTIONS.model.components.avail

    presets = [
        *available_components.point,
        *getattr(available_components, name),
    ]
    params = {}
    for param in presets:
        params[param] = copy.deepcopy(getattr(OPTIONS.model.params, param))

    component = SimpleNamespace(
        name=name,
        vis=functions[f"{name}_vis"],
        img=functions[f"{name}_img"],
        params=SimpleNamespace(**params),
    )
    return component


# def point_img(rho, theta, params: SimpleNamespace) -> np.ndarray:
#     img = np.zeros_like(rho)
#     x0, y0 = get_param_value(params.x), get_param_value(params.y)
#     rho0, theta0 = np.hypot(x0, y0), np.arctan2(y0, x0)
#     idx = np.argmin(np.hypot(rho - rho0, compare_angles(theta, theta0)))
#     img.flat[idx] = 1 * u.mas
#     return img
#
#
# def point_vis(spf, psi, params: SimpleNamespace) -> complex:
#     """A point source visibility function."""
#     return complex(1, 0)


def gauss_vis(spf: np.ndarray, psi: np.ndarray, params: SimpleNamespace) -> np.ndarray:
    """A Gaussian disk visibility function."""
    fwhm = get_param_value(params.fwhm)
    return np.exp(
        -((np.pi * fwhm.to(u.rad).value * spf) ** 2) / (4 * np.log(2))
    ).astype(complex)


def gauss_img(rho: np.ndarray, phi: np.ndarray, params: SimpleNamespace) -> np.ndarray:
    fwhm = get_param_value(params.fwhm).value
    return (
        np.exp(-4 * np.log(2) * rho**2 / fwhm**2)
        / np.sqrt(np.pi / (4 * np.log(2)))
        / fwhm
    )


def uniform_disc_vis(
    spf: np.ndarray, psi: np.ndarray, params: SimpleNamespace
) -> np.ndarray:
    """An uniform disk visibility function."""
    diam = get_param_value(params.diam).to(u.rad).value
    complex_vis = (2 * j1(np.pi * diam * spf) / (np.pi * diam * spf))
    return np.nan_to_num(complex_vis.astype(complex), nan=1)


def uniform_disc_img(
    rho: np.ndarray, phi: np.ndarray, params: SimpleNamespace
) -> np.ndarray:
    diam = get_param_value(params.diam).value
    return np.where(rho < diam / 2, 4 / (np.pi * diam**2), 0)


def ring_vis(spf: np.ndarray, psi: np.ndarray, params: SimpleNamespace) -> np.ndarray:
    """A infinitesimally thin ring visibility function."""
    rin = get_param_value(params.rin).to(u.rad).value
    return j0(2 * np.pi * rin * spf).astype(complex)


def ring_img(rho: np.ndarray, phi: np.ndarray, params: SimpleNamespace) -> np.ndarray:
    rin = get_param_value(params.rin).value
    return np.where((rho > rin) & (rho < rin + 0.1), 1 / (2 * np.pi * rin), 0)


# TODO: Finish this
# def asymmetric_ring_vis(spf: 1 / u.rad, psi: u.rad, rin: u.mas, order: int, **kwargs) -> np.ndarray:
#     """A infinitesimally thin ring visibility function."""
#     return j0(2 * np.pi * rin.to(u.rad) * spf).astype(complex)
