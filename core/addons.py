import json
import os
from pathlib import Path

from fishbase.fish_logger import logger
from pydantic import BaseModel, Field


class AddonsError(Exception):
    pass


class AddonsInfo(BaseModel):
    identifier: str = Field(...)
    name: str = Field(default='', title='', description='')
    title: str = Field(...)
    version: str = Field('1.0')
    author: str
    intro: str
    installed: bool = Field(False)


class Addons(object):
    """Every addons should implement this class. It handles the registration
    for the addons hooks, creates or modifies additional relations or
    registers addons specific thinks
    """

    def __init__(self,):
        pass

    def install(self):  # pragma: no cover
        """Installs the things that must be installed in order to
        have a fully and correctly working addons. For example, something that
        needs to be installed can be a relation and/or modify a existing
        relation.
        """
        pass

    def uninstall(self):  # pragma: no cover
        """Uninstalls all the things which were previously
        installed by `install()`. A Plugin must override this method.
        """
        pass


class AddonsManager:
    def __init__(self, addons_folder, **kwargs):
        """Initializes the PluginManager. It is also possible to initialize the
        PluginManager via a factory. For example::
            addons_manager = PluginManager()
        :param addons_folder: The addons folder where the addons resides.
        :param base_app_folder: The base folder for the application. It is used
                                to build the addons package name.
        """
        # All installed addons
        self._installed_addons = None

        # All addons - including the disabled ones
        self._all_addons = None

        self.addons_folder = addons_folder

    @property
    def all_addons(self):
        """Returns all addons including disabled ones."""
        if self._all_addons is None:
            self.load_addons()
        return self._all_addons

    @property
    def installed_addons(self):
        """Returns all enabled addons as a dictionary. You still need to
        call the setup method to fully enable them."""
        if self._installed_addons is None:
            self.load_addons()
        return self._installed_addons

    def load_addons(self):
        """Loads all addons. They are still disabled.
        Returns a list with all loaded addons. They should now be accessible
        via self.addons.
        """
        self._installed_addons = {}
        self._all_addons = {}
        for item in os.listdir(self.addons_folder):
            _addons_path = Path(self.addons_folder).joinpath(item)
            _addons_info_file = _addons_path.joinpath('info.json')
            if _addons_info_file.is_file():
                try:
                    _addons_info = json.load(open(_addons_info_file, encoding='utf-8'))
                    addons_info = AddonsInfo(identifier=item, **_addons_info)
                    if _addons_path.joinpath('INSTALLED').is_file():
                        addons_info.installed = True
                        self._installed_addons[item] = addons_info
                    self._all_addons[item] = addons_info
                except Exception as e:
                    logger.error(f'load addons faild: {e}')


if __name__ == '__main__':
    addons = AddonsManager('addons', 'C:\\python_project\\knightops\\')
    print(addons.addons_folder)
    print(addons.all_addons)
