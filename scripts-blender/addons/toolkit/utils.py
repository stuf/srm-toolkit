import bpy
from bpy.types import Bone

from . import __package__ as base_package


def get_addon_prefs(context=None):
    if not context:
        context = bpy.context
