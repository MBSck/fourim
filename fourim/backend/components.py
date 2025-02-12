import copy
import inspect
from types import SimpleNamespace

import astropy.units as u
import numpy as np
from numpy.typing import NDArray
from scipy.special import j0, j1

from ..config.options import OPTIONS
from .utils import compare_angles, convert_coords_to_polar, get_param_value


def make_component(name: str) -> SimpleNamespace:
    """Makes a component from the presets."""
    current_module = inspect.getmodule(inspect.currentframe())
    functions = dict(inspect.getmembers(current_module, inspect.isfunction))
    presets = [
        *OPTIONS.model.components.avail.point,
        *(getattr(OPTIONS.model.components.avail, name) or []),
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


def background_vis(
    spf: NDArray, psi: NDArray, params: SimpleNamespace
) -> complex:
    """A background's complex visibility."""
    complex_vis = np.zeros_like(spf)
    complex_vis[np.where(spf == 0)[0]] = 1
    return complex_vis.astype(complex)


def background_img(
    rho: NDArray, phi: NDArray, params: SimpleNamespace
) -> NDArray:
    """A background's image."""
    return np.ones_like(rho)


def point_vis(spf: NDArray, psi: NDArray, params: SimpleNamespace) -> complex:
    """A point source's complex visibility."""
    return complex(1, 0)


def point_img(rho: NDArray, phi: NDArray, params: SimpleNamespace) -> NDArray:
    """A point source's image."""
    x0, y0 = get_param_value(params.x).value, get_param_value(params.y).value
    img = np.zeros_like(rho)
    rho0, theta0 = convert_coords_to_polar(x0, y0)
    idx = np.argmin(np.hypot(rho - rho0, compare_angles(phi, theta0)))
    img.flat[idx] = 1
    return img


def gauss_vis(spf: NDArray, psi: NDArray, params: SimpleNamespace) -> NDArray:
    """A Gaussian's visibility."""
    fwhm = get_param_value(params.fwhm)
    return np.exp(
        -((np.pi * fwhm.to(u.rad).value * spf) ** 2) / (4 * np.log(2))
    ).astype(complex)


def gauss_img(rho: NDArray, phi: NDArray, params: SimpleNamespace) -> NDArray:
    """A Gaussian's image."""
    fwhm = get_param_value(params.fwhm).value
    return (
        np.exp(-4 * np.log(2) * rho**2 / fwhm**2)
        / np.sqrt(np.pi / (4 * np.log(2)))
        / fwhm
    )


def uniform_disc_vis(
    spf: NDArray, psi: NDArray, params: SimpleNamespace
) -> NDArray:
    """An uniform disc's visibility."""
    diam = get_param_value(params.diam).to(u.rad).value
    complex_vis = 2 * j1(np.pi * diam * spf) / (np.pi * diam * spf)
    return np.nan_to_num(complex_vis.astype(complex), nan=1)


def uniform_disc_img(
    rho: NDArray, phi: NDArray, params: SimpleNamespace
) -> NDArray:
    """A uniform disc's image."""
    diam = get_param_value(params.diam).value
    return np.where(rho < diam / 2, 4 / (np.pi * diam**2), 0)


def Iring_vis(spf: NDArray, psi: NDArray, params: SimpleNamespace) -> NDArray:
    """An infinitesimally thin ring's visibility."""
    rin = get_param_value(params.rin).to(u.rad).value
    return j0(2 * np.pi * rin * spf).astype(complex)


def Iring_img(rho: NDArray, phi: NDArray, params: SimpleNamespace) -> NDArray:
    """An infinitesimally thin ring's image."""
    rin = get_param_value(params.rin).value
    return np.where((rho > rin) & (rho < rin + 0.12), 1 / (2 * np.pi * rin), 0)


# TODO: Implement this
# def asymmetric_ring_vis(spf: 1 / u.rad, psi: u.rad, rin: u.mas, order: int, **kwargs) -> NDArray:
#     """A infinitesimally thin ring visibility function."""
#     return j0(2 * np.pi * rin.to(u.rad) * spf).astype(complex)
