from ppdmod.component import Component
from ppdmod import basic_components

from .options import OPTIONS


def set_active_model() -> Component:
    """Returns the active model."""
    if OPTIONS.model.active is None\
        or OPTIONS.model.selected != OPTIONS.model.active.name:
        params = {"elliptic": True, "asymmetric": True}
        if hasattr(OPTIONS.model.presets, OPTIONS.model.selected.lower()):
            params = {**getattr(OPTIONS.model.presets, OPTIONS.model.selected.lower()), **params}
        OPTIONS.model.active = getattr(basic_components, OPTIONS.model.selected)(**params)
    return OPTIONS.model.active
