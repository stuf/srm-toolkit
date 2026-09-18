from bpy.types import Operator


class SRM_OT_toggle_pose_mode(Operator):
    """Toggle armature between Pose/Rest position"""
    bl_idname = "srm.toggle_pose_mode"
    bl_label = "Toggle Pose Mode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            return context.active_object.type == 'ARMATURE'
        except:
            return False

    def execute(self, context):
        obj = context.active_object

        obj.data.pose_position = 'REST' if obj.data.pose_position == 'POSE' else 'POSE'

        return {'FINISHED'}


registry = [SRM_OT_toggle_pose_mode]
