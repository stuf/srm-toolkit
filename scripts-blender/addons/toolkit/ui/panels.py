import bpy

from ..operators import toggle_pose_mode


class SRM_PT_ArmatureUtils(bpy.types.Panel):
    """Armature utility panel"""

    bl_label = "Armature"
    bl_idname = "SRM_PT_ArmatureUtils"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SRM"

    @classmethod
    def poll(self, context: bpy.types.Context):
        try:
            return context.active_object.type == 'ARMATURE'
        except:
            return False

    def draw(self, context):
        layout = self.layout

        pose_position = context.active_object.data.pose_position == 'POSE'

        row = layout.column()
        row.operator("srm.toggle_pose_mode",
                     text="Pose Position",
                     depress=pose_position)


registry = [SRM_PT_ArmatureUtils]
