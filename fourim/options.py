from types import SimpleNamespace

import astropy.units as u

geometry = SimpleNamespace(width=1024, height=400)
display = SimpleNamespace(one_dimensional=True, output="vis2", coplanar=True)
presets = SimpleNamespace(all={"elliptic": True},
                          ring={"rin": 1, "width": 0.1,
                                "thin": False, "asymmetric": True})
components = SimpleNamespace(avail=["PointSource", "Star", "Ring", "UniformDisk",
                                    "Gaussian", "Lorentzian", "GaussLorentzian"],
                             presets=presets)
model = SimpleNamespace(components=components, one_dim=4096, two_dim=512,
                        pixel_size=0.1*u.mas, wl=[3.5]*u.um)

OPTIONS = SimpleNamespace(model=model, geometry=geometry, display=display)
