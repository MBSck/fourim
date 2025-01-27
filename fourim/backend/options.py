from pathlib import Path
from types import SimpleNamespace

import astropy.units as u
import toml

files = {}
geometry = SimpleNamespace(width=1024, height=400)
display = SimpleNamespace(one_dimensional=True, output="vis2", coplanar=True)
presets = SimpleNamespace(
    all={"elliptic": True, "diam": 1, "fwhm": 1},
    ring={"rin": 1, "width": 0.1, "thin": False, "asymmetric": True},
)
components = SimpleNamespace(avail=[], current={})
with open(Path(__file__).parent.parent / "config" / "units.toml", "r") as f:
    units = toml.load(f)["params"]

for key, value in units.items():
    if value == "one":
        units[key] = u.one
    else:
        units[key] = u.Unit(value)

params = SimpleNamespace(units=units)
model = SimpleNamespace(
    components=components,
    params=params,
    one_dim=4096,
    two_dim=512,
    pixel_size=0.1 * u.mas,
    wl=[3.2] * u.um,
)

OPTIONS = SimpleNamespace(
    model=model, geometry=geometry, display=display, files=files
)
