from types import SimpleNamespace
from typing import Tuple

import astropy.units as u
import numpy as np
from numpy.typing import NDArray

from ..config.options import OPTIONS
from .utils import (
    transform_coordinates,
    get_param_value,
)


def translate_vis(
    ucoord: np.ndarray, vcoord: np.ndarray, params: SimpleNamespace
) -> np.ndarray:
    """Translation in Fourier space."""
    x = get_param_value(params.x).to(u.rad).value
    y = get_param_value(params.y).to(u.rad).value

    condition = [
        comp.params.fr.value != 0 for comp in OPTIONS.model.components.current.values()
    ]
    if len(OPTIONS.model.components.current) <= 1 or np.sum(condition) <= 1:
        return np.ones_like(ucoord).astype(complex)

    return np.exp(-2j * np.pi * (x * ucoord + y * vcoord))


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

        utb, vtb = map(
            lambda x: x / wl, transform_coordinates(ucoord, ucoord, cinc, pa)
        )
        shift = translate_vis(utb, vtb, component.params)
        vis = component.vis(np.hypot(utb, vtb), np.arctan2(utb, vtb), component.params)
        complex_vis.append(fr * vis * shift)

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

        xt, yt = transform_coordinates(xs, ys, cinc, pa, axis="x")
        img = component.img(np.hypot(xt, yt), np.arctan2(xt, yt), component.params)
        image.append(fr * img / img.max())

    return np.sum(image, axis=0)
