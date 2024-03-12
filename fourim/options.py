from types import SimpleNamespace

geometry = SimpleNamespace(width=400, height=300)

model = SimpleNamespace(avail=["Point Source", "Gaussian"])

OPTIONS = SimpleNamespace(model=model, geometry=geometry)
