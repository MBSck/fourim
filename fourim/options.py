from types import SimpleNamespace

import astropy.units as u

geometry = SimpleNamespace(width=1024, height=400)
display = SimpleNamespace(one_dimensional=True)
model = SimpleNamespace(active=None, selected="PointSource",
                        avail=["PointSource", "Ring"],
                        dim=1024, pixel_size=0.1*u.mas, wl=[10]*u.um)

OPTIONS = SimpleNamespace(model=model, geometry=geometry, display=display)
