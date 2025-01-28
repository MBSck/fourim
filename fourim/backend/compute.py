from types import SimpleNamespace
from typing import Dict

import astropy.units as u
import numpy as np

from .options import OPTIONS
from .utils import (
    compute_baselines,
    compute_image_grid,
    get_param_value,
    translate_img,
    translate_vis,
)


def compute_complex_vis(
    components: Dict[str, SimpleNamespace], wl: u.um, dim: int
) -> np.ndarray:
    """Computes the complex visibility of the model."""
    ucoord = np.linspace(0, 150, dim) * u.m
    spf, _ = compute_baselines(ucoord, ucoord)

    complex_vis = []
    for component in components.values():
        fr = get_param_value(component.params.fr)
        inc = get_param_value(component.params.cinc)
        pa = get_param_value(component.params.pa)
        spf_comp, psi_comp = compute_baselines(
            ucoord,
            ucoord,
            inc,
            pa,
        )
        spf_comp_wl = (spf_comp / wl.to(u.m)).value / u.rad
        vis = component.vis(spf_comp_wl, psi_comp, component.params).astype(complex)
        vis *= translate_vis(spf_comp_wl, psi_comp, component.params).astype(complex)

        # FIXME: Interpolation does not do what it should
        complex_vis.append(fr * np.interp(spf, spf_comp, vis))

    return spf, np.sum(complex_vis, axis=0)


def compute_amplitude(complex_vis: np.ndarray) -> np.ndarray:
    """Computes the amplitude of the complex visibility."""
    vis = np.abs(complex_vis)
    if OPTIONS.display.output == "vis2":
        return vis**2
    return vis


def compute_phase(complex_vis: np.ndarray) -> np.ndarray:
    """Computes the phase of the complex visibility."""
    return np.angle(complex_vis, deg=True)


def compute_image(
    components: Dict[str, SimpleNamespace], pixel_size: u.rad, dim: int
) -> np.ndarray:
    """Computes the image of the model."""
    xcoord = np.linspace(-0.5, 0.5, dim) * dim * pixel_size

    image = []
    for component in components.values():
        fr = get_param_value(component.params.fr)
        inc = get_param_value(component.params.cinc)
        pa = get_param_value(component.params.pa)
        xx, yy = translate_img(xcoord, xcoord, component.params)
        rho, theta = compute_image_grid(
            *np.meshgrid(xx, yy),
            inc,
            pa,
        )
        img = component.img(rho, theta, component.params)
        image.append(fr * img / img.max())

    return np.sum(image, axis=0)
