from types import SimpleNamespace

import astropy.units as u


files = {}
geometry = SimpleNamespace(width=1024, height=400)
display = SimpleNamespace(one_dimensional=True, output="vis2", coplanar=True)
presets = SimpleNamespace(
    all={"elliptic": True, "diam": 1, "fwhm": 1},
    ring={"rin": 1, "width": 0.1, "thin": False, "asymmetric": True},
)
components = SimpleNamespace(avail=[], current={})
model = SimpleNamespace(
    components=components,
    one_dim=4096,
    two_dim=512,
    pixel_size=0.1 * u.mas,
    wl=[3.2] * u.um,
)

OPTIONS = SimpleNamespace(
    model=model, geometry=geometry, components=components, display=display, files=files
)
