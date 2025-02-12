from types import SimpleNamespace
from typing import Tuple

import astropy.units as u
import numpy as np
from numpy.typing import NDArray

from ..config.options import OPTIONS
from .utils import (
    convert_coords_to_polar,
    get_param_value,
)


def translate_vis(
    spf: np.ndarray, psi: np.ndarray, params: SimpleNamespace
) -> np.ndarray:
    """Translation in Fourier space."""
    x = get_param_value(params.x).to(u.rad).value
    y = get_param_value(params.y).to(u.rad).value
    uv = np.exp(1j * x * np.cos(psi)) * np.exp(1j * y * np.sin(psi))
    condition = [
        comp.params.fr.value != 0 for comp in OPTIONS.model.components.current.values()
    ]
    if len(OPTIONS.model.components.current) <= 1 or np.sum(condition) <= 1:
        return np.ones_like(spf).astype(complex)

    return np.exp(2j * np.pi * spf * np.angle(uv)).astype(complex)


def compute_complex_vis(
    components: SimpleNamespace, ucoord: NDArray, wl: NDArray
) -> Tuple[NDArray, NDArray]:
    """Computes the complex visibility of the model."""
    complex_vis = []
    for component in components.values():
        fr = get_param_value(component.params.fr).value
        if component.name in ["point", "background"]:
            cinc, pa = None, None
        else:
            cinc = get_param_value(component.params.cinc).value
            pa = get_param_value(component.params.pa).value

        spf, psi = convert_coords_to_polar(ucoord, ucoord, cinc, pa)
        spf /= wl
        vis = component.vis(spf, psi, component.params)
        vis *= translate_vis(spf, psi, component.params)
        complex_vis.append(fr * vis)

    complex_vis = np.sum(complex_vis, axis=0)
    complex_vis /= complex_vis[0]
    vis = np.abs(complex_vis)
    vis = vis**2 if OPTIONS.settings.display.amplitude == "vis2" else vis
    return vis, np.angle(complex_vis, deg=True)


def translate_img(x: np.ndarray, y: np.ndarray, params: SimpleNamespace) -> Tuple:
    """Shifts the coordinates in image space according to an offset."""
    x0 = get_param_value(params.x).value
    y0 = get_param_value(params.y).value
    return x - x0, y - y0


def compute_image(components: SimpleNamespace, xx: NDArray, yy: NDArray) -> NDArray:
    """Computes the image of the model."""
    image = []
    for component in components.values():
        fr = get_param_value(component.params.fr).value
        xs, ys = translate_img(xx, yy, component.params)
        if component.name in ["point", "background"]:
            cinc, pa = None, None
        else:
            cinc = get_param_value(component.params.cinc).value
            pa = get_param_value(component.params.pa).value

        rho, phi = convert_coords_to_polar(xs, ys, cinc, pa)
        img = component.img(rho, phi, component.params)
        image.append(fr * img / img.max())

    return np.sum(image, axis=0)
