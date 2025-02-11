from pathlib import Path
from types import SimpleNamespace

import astropy.units as u
import toml
import yaml

files = {}
display = SimpleNamespace(one_dimensional=True, amplitude="vis2", label=r"V^2 (a.u.)")
settings = SimpleNamespace(display=display)

with open(Path(__file__).parent.parent / "config" / "components.yaml", "r") as f:
    avail = yaml.safe_load(f)

components = SimpleNamespace(
    avail=SimpleNamespace(**avail), current={}, init="background"
)

with open(Path(__file__).parent.parent / "config" / "parameters.toml", "r") as f:
    params = toml.load(f)

for key, value in params.items():
    if value["unit"] == "one":
        params[key]["unit"] = u.one
    else:
        params[key]["unit"] = u.Unit(value["unit"])

    params[key] = SimpleNamespace(**params[key])

params = SimpleNamespace(**params)
model = SimpleNamespace(
    components=components,
    params=params,
    dim=512,
    pixel_size=0.1,
    wl=3.2e-6,
)

OPTIONS = SimpleNamespace(model=model, settings=settings, files=files)
