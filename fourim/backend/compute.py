from types import SimpleNamespace

import numpy as np
from numpy.typing import NDArray

from ..config.options import OPTIONS
from .utils import (
    convert_coords_to_polar,
    get_param_value,
    translate_img,
    translate_vis,
)


def compute_complex_vis(
    components: SimpleNamespace, ucoord: NDArray, wl: NDArray
) -> NDArray:
    """Computes the complex visibility of the model."""
    complex_vis = []
    for component in components.values():
        fr = get_param_value(component.params.fr).value
        cinc = get_param_value(component.params.cinc).value
        pa = get_param_value(component.params.pa).value
        spf, psi = convert_coords_to_polar(ucoord, ucoord, cinc, pa)
        spf /= wl
        vis = component.vis(spf, psi, component.params)
        vis *= translate_vis(spf, psi, component.params).astype(complex)
        complex_vis.append(fr * vis)

    complex_vis = np.sum(complex_vis, axis=0)
    return complex_vis / complex_vis[0]


def compute_amplitude(complex_vis: NDArray) -> NDArray:
    """Computes the amplitude of the complex visibility."""
    vis = np.abs(complex_vis)
    return vis**2 if OPTIONS.settings.display.amplitude == "vis2" else vis


def compute_phase(complex_vis: NDArray) -> NDArray:
    """Computes the phase of the complex visibility."""
    return np.angle(complex_vis, deg=True)


def compute_image(components: SimpleNamespace, xx: NDArray, yy: NDArray) -> NDArray:
    """Computes the image of the model."""
    image = []
    for component in components.values():
        fr = get_param_value(component.params.fr).value
        xs, ys = translate_img(xx, yy, component.params)
        if component.name in ["point", "background"]:
            cinc, pa = 1, 0
        else:
            cinc = get_param_value(component.params.cinc).value
            pa = get_param_value(component.params.pa).value

        rho, phi = convert_coords_to_polar(xs, ys, cinc, pa)
        img = component.img(rho, phi, component.params)
        image.append(fr * img / img.max())

    return np.sum(image, axis=0)
