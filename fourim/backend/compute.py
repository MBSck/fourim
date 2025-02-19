from types import SimpleNamespace
from typing import Tuple

import astropy.units as u
import numpy as np
from juliacall import Main as jl
from numpy.typing import NDArray

from ..config.options import OPTIONS

jl.include("fourim/backend/utils.jl")


def complex_vis(
    components: SimpleNamespace, ucoord: NDArray, wl: NDArray
) -> Tuple[NDArray, NDArray]:
    """Computes the complex visibility of the model."""
    complex_vis = []
    for component in components.values():
        fr = component.params.fr.value
        if component.name in ["point", "background"]:
            cinc, pa = 1, 0
        else:
            cinc = component.params.cinc.value
            pa = component.params.pa.value

        x = component.params.x.value * component.params.x.unit.to(u.rad)
        y = component.params.y.value * component.params.y.unit.to(u.rad)
        utb, vtb = map(
            lambda x: x / wl, np.array(jl.transform(ucoord, ucoord, pa, cinc)).T
        )
        shift = np.array(jl.convolve(x, y, utb, vtb)).T
        vis = component.vis(np.hypot(utb, vtb), np.arctan2(utb, vtb), component.params)
        complex_vis.append(fr * vis * shift)

    complex_vis = np.sum(complex_vis, axis=0)
    complex_vis /= complex_vis[0]
    vis = np.abs(complex_vis)
    vis = vis**2 if OPTIONS.settings.display.amplitude == "vis2" else vis
    return vis, np.angle(complex_vis, deg=True)


def image(components: SimpleNamespace, xx: NDArray, yy: NDArray) -> NDArray:
    """Computes the image of the model."""
    image = []
    for component in components.values():
        fr = component.params.fr.value
        x, y = component.params.x.value, component.params.y.value
        xs, ys = np.array(jl.translate(xx, yy, x, y)).T
        if component.name in ["point", "background"]:
            cinc, pa = 1, 0
        else:
            cinc = component.params.cinc.value
            pa = component.params.pa.value

        xt, yt = np.array(jl.transform(xs, ys, pa, 1, cinc)).T
        img = component.img(np.hypot(xt, yt), np.arctan2(xt, yt), component.params)
        image.append(fr * img / img.max())

    return np.sum(image, axis=0)
