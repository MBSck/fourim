import inspect
from pathlib import Path
from types import SimpleNamespace
from typing import Callable, Dict

import astropy.units as u
import numpy as np
import toml
from scipy.special import j0, j1, jv


def get_available_components() -> Dict[str, Callable]:
    """Returns a list of available components."""
    with open(Path(__file__).parent.parent / "config" / "components.toml", "r") as f:
        toml_data = toml.load(f)

    components = {}
    current_module = inspect.getmodule(inspect.currentframe())
    for name, obj in inspect.getmembers(current_module, inspect.isfunction):
        if not "vis" in name:
            continue

        component_name = name.split("_vis")[0]
        params = SimpleNamespace(**toml_data[component_name], **toml_data["default"])
        preset = SimpleNamespace(name=component_name, vis=obj, params=params)
        # TODO: Add here the image function
        components[component_name] = preset

    return components


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
    return np.exp(-((np.pi * fwhm.to(u.rad) * spf) ** 2) / (4 * np.log(2)))


# def uniform_disk_vis(spf, psi, **kwargs) -> np.ndarray:
#     """An uniform disk visibility function."""
#     return 2 * j1(np.pi * diam.to(u.rad) * spf) / (np.pi * diam.to(u.rad) * spf)
#

def ring_vis(spf, ps, **kwargsi) -> np.ndarray:
    """A infinitesimally thin ring visibility function."""
    return j0(2 * np.pi * rin.to(u.rad) * spf)


# TODO: Finish this
# def asymmetric_ring_vis(spf: 1 / u.rad, psi: u.rad, rin: u.mas, order: int, **kwargs) -> np.ndarray:
#     """A infinitesimally thin ring visibility function."""
#     return j0(2 * np.pi * rin.to(u.rad) * spf).astype(complex)
