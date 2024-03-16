from types import SimpleNamespace

geometry = SimpleNamespace(width=1024, height=400)
display = SimpleNamespace(one_dimensional=False)
model = SimpleNamespace(avail=["Point Source", "Gaussian"])

OPTIONS = SimpleNamespace(model=model, geometry=geometry, display=display)
