from pathlib import Path
from types import SimpleNamespace

import astropy.units as u
import toml
import yaml

files = {}
geometry = SimpleNamespace(width=1024, height=400)
display = SimpleNamespace(one_dimensional=True, output="vis2")

with open(Path(__file__).parent.parent / "config" / "components.yaml", "r") as f:
    avail = yaml.safe_load(f)

components = SimpleNamespace(avail=SimpleNamespace(**avail), current={}, init="gauss")

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
    one_dim=4096,
    two_dim=512,
    pixel_size=0.1,
    wl=3.2e-6,
)

OPTIONS = SimpleNamespace(model=model, geometry=geometry, display=display, files=files)
