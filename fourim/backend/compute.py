from types import SimpleNamespace
from typing import Dict

import astropy.units as u
import numpy as np

from ..config.options import OPTIONS
from .utils import (
    convert_coords_to_polar,
    get_param_value,
    translate_img,
    translate_vis,
)


def compute_complex_vis(
    components: SimpleNamespace, ucoord: np.ndarray, wl: np.ndarray
) -> np.ndarray:
    """Computes the complex visibility of the model."""
    complex_vis = []
    for component in components.values():
        fr = get_param_value(component.params.fr).value
        inc = get_param_value(component.params.cinc).value
        pa = get_param_value(component.params.pa).value
        spf, psi = convert_coords_to_polar(
            ucoord,
            ucoord,
            inc,
            pa,
        )
        spf /= wl
        vis = component.vis(spf, psi, component.params)
        vis *= translate_vis(spf, psi, component.params).astype(complex)
        complex_vis.append(fr * vis)

    return np.sum(complex_vis, axis=0)


def compute_amplitude(complex_vis: np.ndarray) -> np.ndarray:
    """Computes the amplitude of the complex visibility."""
    vis = np.abs(complex_vis)
    return vis**2 if OPTIONS.display.output == "vis2" else vis


def compute_phase(complex_vis: np.ndarray) -> np.ndarray:
    """Computes the phase of the complex visibility."""
    return np.angle(complex_vis, deg=True)


def compute_image(
    components: Dict[str, SimpleNamespace], pixel_size: float, dim: int
) -> np.ndarray:
    """Computes the image of the model."""
    x = np.linspace(-0.5, 0.5, dim) * dim * pixel_size
    image = []
    for component in components.values():
        fr = get_param_value(component.params.fr).value
        inc = get_param_value(component.params.cinc).value
        pa = get_param_value(component.params.pa).value
        xx, yy = translate_img(*np.meshgrid(x, x), component.params)
        rho, phi = convert_coords_to_polar(xx, yy, inc, pa)
        img = component.img(rho, phi, component.params)
        image.append(fr * img / img.max())

    return np.sum(image, axis=0)
