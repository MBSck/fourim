import inspect
from types import SimpleNamespace

import astropy.units as u
import numpy as np
from scipy.special import j0, j1, jv

from .options import OPTIONS


def make_component(name: str) -> SimpleNamespace:
    """Makes a component from the presets."""
    current_module = inspect.getmodule(inspect.currentframe())
    functions = dict(inspect.getmembers(current_module, inspect.isfunction))
    available_components = OPTIONS.model.components.avail

    presets = [
        *available_components.default,
        *getattr(available_components, name),
    ]
    params = {}
    for param in presets:
        params[param] = getattr(OPTIONS.model.params, param)

    component = SimpleNamespace(
        name=name, vis=functions[f"{name}_vis"], params=SimpleNamespace(**params)
    )
    return component


# def point_vis(spf, psi, **kwargs) -> np.ndarray:
#     """A point source visibility function."""
#     uv = np.exp(1j * x.to(u.rad) * np.cos(psi)) * np.exp(1j * y.to(u.rad) * np.sin(psi))
#     return np.exp(2j * np.pi * spf * np.angle(uv) * u.rad)


# def binary_vis(spf: 1 / u.rad, psi: u.rad, flux1: u.Jy | u.one, flux2: u.Jy | u.one) -> np.ndarray:
#     flux_ratio = flux1 / flux2
#     numerator = (1 + flux_ratio**2 + 2 * flux_ratio * np.cos(2 * np.pi * spf * np.cos(psi)))
#     denominator = 1 + flux_ratio**2
#     return np.sqrt(numerator / denominator)


def gaus_vis(spf, psi, **kwargs) -> np.ndarray:
    """A Gaussian disk visibility function."""
    return kwargs["fr"] * np.exp(
        -((np.pi * kwargs["fwhm"].to(u.rad) * spf) ** 2) / (4 * np.log(2))
    )


# def uniform_disk_vis(spf, psi, **kwargs) -> np.ndarray:
#     """An uniform disk visibility function."""
#     return 2 * j1(np.pi * diam.to(u.rad) * spf) / (np.pi * diam.to(u.rad) * spf)
#


def ring_vis(spf, ps, **kwargs) -> np.ndarray:
    """A infinitesimally thin ring visibility function."""
    return kwargs["fr"] * j0(2 * np.pi * kwargs["rin"].to(u.rad) * spf)


# TODO: Finish this
# def asymmetric_ring_vis(spf: 1 / u.rad, psi: u.rad, rin: u.mas, order: int, **kwargs) -> np.ndarray:
#     """A infinitesimally thin ring visibility function."""
#     return j0(2 * np.pi * rin.to(u.rad) * spf).astype(complex)
