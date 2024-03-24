from types import SimpleNamespace

import astropy.units as u

geometry = SimpleNamespace(width=1024, height=400)
display = SimpleNamespace(one_dimensional=True)
presets = SimpleNamespace(ring={"rin": 20, "thin": False, "width": 0.1})
model = SimpleNamespace(active=None, selected="PointSource",
                        avail=["PointSource", "Star", "Ring", "UniformDisk",
                               "Gaussian", "Lorentzian", "GaussLorentzian"],
                        presets=presets, one_dim=4096, two_dim=512,
                        pixel_size=0.1*u.mas, wl=[10]*u.um)

OPTIONS = SimpleNamespace(model=model, geometry=geometry, display=display)
