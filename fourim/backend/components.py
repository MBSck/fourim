import copy
import inspect
from types import SimpleNamespace

import astropy.units as u
import numpy as np
from scipy.special import j0, j1, jv

from .options import OPTIONS
from .utils import get_param_value


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


# TODO: Implement this point source
# def point_img(rho, theta, params: SimpleNamespace) -> np.ndarray:
#     img = np.zeros_like(rho)
#     img[centre] = 1 * u.mas
#     return img
#
#
# def point_vis(spf, psi, params: SimpleNamespace) -> float:
#     """A point source visibility function."""
#     return 1


def gauss_img(rho, theta, params: SimpleNamespace) -> np.ndarray:
    fwhm = get_param_value(params.fwhm)
    return (
        np.exp(-4 * np.log(2) * rho**2 / fwhm**2)
        / np.sqrt(np.pi / (4 * np.log(2)))
        / fwhm
    )


def gauss_vis(spf, psi, params: SimpleNamespace) -> np.ndarray:
    """A Gaussian disk visibility function."""
    fwhm = get_param_value(params.fwhm)
    return np.exp(-((np.pi * fwhm.to(u.rad) * spf) ** 2) / (4 * np.log(2)))


# def uniform_disk_vis(spf, psi, **kwargs) -> np.ndarray:
#     """An uniform disk visibility function."""
#     return 2 * j1(np.pi * diam.to(u.rad) * spf) / (np.pi * diam.to(u.rad) * spf)
#


# def ring_img(rho, theta, params: SimpleNamespace) -> np.ndarray:
#     rin = get_param_value(params.rin)
#     return np.where((rho > rin) & (rho < rin + np.diff(rho)[0]), 1, 0)
#
#
# def ring_vis(spf, psi, params: SimpleNamespace) -> np.ndarray:
#     """A infinitesimally thin ring visibility function."""
#     return j0(2 * np.pi * get_param_value(params.rin).to(u.rad) * spf)


# TODO: Finish this
# def asymmetric_ring_vis(spf: 1 / u.rad, psi: u.rad, rin: u.mas, order: int, **kwargs) -> np.ndarray:
#     """A infinitesimally thin ring visibility function."""
#     return j0(2 * np.pi * rin.to(u.rad) * spf).astype(complex)
