import logging
from bpy.types import Operator, Object

logger = logging.getLogger(__name__)


class SRM_OT_rename_weights(Operator):
    bl_idname = 'srm.rename_weights'
    bl_label = 'Rename weights'
    bl_description = 'Rename weights on selected meshes based on lookups'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            return any(obj.type == 'MESH' for obj in context.selected_object)
        except:
            return False

    def rename_weights(self, obj: Object):
        logger.info('rename weights on mesh {}', obj.name)

        try:
            pass
        except:
            pass

    def execute(self, context):
        meshes = [
            obj for obj in context.selected_objects if obj.type == 'MESH'
        ]

        for mesh in meshes:
            self.rename_weights(mesh)

        return {'CANCELLED'}


registry = [SRM_OT_rename_weights]
