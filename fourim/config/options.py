from pathlib import Path
from types import SimpleNamespace
from typing import Tuple

import astropy.units as u
import numpy as np
import toml
import yaml
from numpy.typing import NDArray
from juliacall import Main as jl

jl.include("fourim/backend/utils.jl")

def compute_fourier_grid(model: SimpleNamespace) -> Tuple[NDArray, NDArray]:
    ucoord = np.linspace(0, 150, model.dim * 2)
    return ucoord, np.hypot(*np.array(jl.transform(ucoord, ucoord)).T)


def compute_image_grid(model: SimpleNamespace) -> Tuple[NDArray, NDArray]:
    """Computes the image grid."""
    if model.xx is not None and model.dim == model.xx.shape[0]:
        return model.xx, model.yy

    x = np.linspace(-0.5, 0.5, model.dim, endpoint=False) * model.max_im * 2
    return np.meshgrid(x, x)


with open(Path(__file__).parent.parent / "config" / "components.yaml", "r") as f:
    avail = yaml.safe_load(f)

components = SimpleNamespace(avail=SimpleNamespace(**avail), current={}, init="point")

with open(Path(__file__).parent.parent / "config" / "parameters.toml", "r") as f:
    params = toml.load(f)

for key, value in params.items():
    if value["unit"] == "one":
        params[key]["unit"] = u.one
    else:
        params[key]["unit"] = u.Unit(value["unit"])

    params[key] = SimpleNamespace(**params[key])

params = SimpleNamespace(**params)
# TODO: Compute the things that are computable at the first time if the dim is not updated
model = SimpleNamespace(
    components=components,
    params=params,
    dim=512,
    pixel_size=0.1,
    wl=3.2e-6,
    u=None,
    spf=None,
    max_im=None,
    xx=None,
    yy=None,
    results={},
)

model.max_im = model.dim / 2 * model.pixel_size
model.u, model.spf = compute_fourier_grid(model)
model.xx, model.yy = compute_image_grid(model)
OPTIONS = SimpleNamespace(model=model, settings=settings, files=files)
