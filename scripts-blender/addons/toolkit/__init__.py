import importlib
import logging

import bpy

from . import (operators, ui)
from .util.logging import setup_logger

logger = logging.getLogger(f'{__name__}_MAIN')

bl_info = {
    "name": "SRM Toolkit",
    "author": "stuf",
    "version": (0, 0, 1),
    "blender": (5, 0, 0),
    "location": "Everywhere",
    "description": "",
    "category": "Rigging",
    "doc_url": "https://github.com/stuf/srm-toolkit",
    "tracker_url": "https://github.com/stuf/srm-toolkit"
}

modules = [ui, operators]

ModuleType = type(modules[0])


def register_unregister_modules(modules: list[ModuleType], register: bool):
    register_func = bpy.utils.register_class if register else bpy.utils.unregister_class
    un = "un" if not register else ""

    for mod in modules:
        logger.info('registering module {}'.format(mod.__name__))
        if register:
            importlib.reload(mod)

        if hasattr(mod, "registry"):
            for class_to_reg in mod.registry:
                try:
                    register_func(class_to_reg)
                except Exception as e:

                    print(
                        f'Warning: Could not {un}register class: {class_to_reg.__name__}'
                    )
                    print(e)

        if hasattr(mod, "modules"):
            register_unregister_modules(mod.modules, register)

        if register and hasattr(mod, "register"):
            mod.register()
        elif hasattr(mod, "unregister"):
            mod.unregister()


def register():
    setup_logger(logger)
    logger.info('Registering SRM Toolkit')
    register_unregister_modules(modules, True)


def unregister():
    logger.info('Unregistering SRM Toolkit')
    register_unregister_modules(modules, False)
