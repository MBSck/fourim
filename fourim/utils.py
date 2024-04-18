import inspect
from pathlib import Path
from typing import List

from ppdmod import basic_components
from ppdmod.component import Component
from ppdmod.data import ReadoutFits

from .options import OPTIONS


def get_available_components() -> List[str]:
    """Returns a list of available components."""
    components = []
    for name, obj in inspect.getmembers(basic_components):
        if inspect.isclass(obj) and obj.__module__ == basic_components.__name__:
            components.append(name)
    return components


# TODO: Test if this also works when models are removed and new ones added
# or if it looses the count of the models
class ComponentManager:
    """A manager for the components in the application."""

    def __init__(self):
        self.current_id = 0
        self.components = {}

    @property
    def next_id(self) -> int:
        """Returns the next id."""
        return self.current_id + 1

    def add_component(self, component_name: str) -> int:
        """Adds a component to the manager and returns its id."""
        presets = OPTIONS.model.components.presets

        params = presets.all
        if hasattr(presets, component_name.lower()):
            params = {**getattr(presets, component_name.lower()), **params}

        self.components[self.current_id] = getattr(basic_components, component_name)(**params)
        self.current_id += 1
        return self.current_id

    def get_component(self, component_id: int) -> Component:
        """Returns the component with the given id."""
        return self.components.get(component_id)

    def remove_component(self, component_id: int) -> None:
        """Removes the component with the given id."""
        if component_id in self.components:
            del self.components[component_id]

    def get_all_components(self) -> List[Component]:
        """Returns all components in a list."""
        return list(self.components.values())


class FileManager:
    """A manager for the files in the application."""

    def __init__(self):
        self.files = {}

    def add_file(self, file_path: str) -> None:
        """Adds a file to the manager."""
        file_path = Path(file_path)
        self.files[file_path.name] = ReadoutFits(file_path)

    def remove_file(self, file_path: str) -> None:
        """Removes the file with the given path."""
        if file_path in self.files:
            del self.files[file_path]
