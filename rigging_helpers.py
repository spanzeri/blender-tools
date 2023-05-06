import bpy

class SRT_PT_RiggingHelperPanel(bpy.types.Panel):
    bl_label = "Rigging Helpers"
    bl_idname = "SRT_PT_RiggingHelper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        if context.mode != "EDIT_ARMATURE":
            row.label(text = "Not in armature edit mode", icon = "QUESTION")
            return

        row.operator("armature.create_target_bones")


def dump(data):
    for attr in dir(data):
        print("%s = %r" % (attr, getattr(data, attr)))


def make_tgt_name(bone_name):
    if bone_name.upper().startswith("DEF-"):
        bone_name = bone_name[4:]
    return "TGT-" + bone_name


bone_readonly_attr = [
    "__doc__", "__module__", "__slots__",
    "align_orientation", "align_roll",
    "bl_rna", "children", "rna_type",
    "transform", "translate",
    "bl_rna_get_subclass", "bl_rna_get_subclass_py"]


class SRT_OT_CreateTargetBone(bpy.types.Operator):
    """ Create a target bone, which is a non-deform bone with the same name prefixed by TGT and add a copy transform constraint
    from the original to the newly create target"""
    bl_idname = "armature.create_target_bones"
    bl_label = "Create TGT bones"

    def execute(self, context):
        if context.mode != "EDIT_ARMATURE":
            self.report({"ERROR"}, "Not in armature edit mode")
            return {"CANCELLED"}

        # Remove existing selection
        bpy.ops.armature.select_all(action = "DESELECT")

        armature = context.object
        if armature.type != "ARMATURE":
            return {"CANCELLED"}

        armature_data = armature.data
        pose = armature.pose
        if not armature_data or not pose:
            return {"CANCELLED"}

        root_names = ["ROOT", "Root", "root"]
        for rname in root_names:
            root = armature_data.edit_bones.get(rname)
            if root:
                break
        if not root:
            self.report({"ERROR"}, "Need a root bone for the armature called ROOT")
            return {"CANCELLED"}

        new_bones = []
        constraint_map = []
        layers = [False] * 32
        layers[31] = True

        # Make duplicate bones with the correct name
        for bone in armature_data.edit_bones:
            if not bone.use_deform or bone.name.upper().startswith("TGT-"):
                continue
            tgt_bone_name = make_tgt_name(bone.name)

            if armature_data.edit_bones.get(tgt_bone_name):
                # Bone already exists
                continue

            tgt_bone = armature_data.edit_bones.new(tgt_bone_name)
            for attr in dir(tgt_bone):
                if attr.find("") != -1 and attr not in bone_readonly_attr:
                    if attr == "name" or attr == "layers":
                        pass
                    else:
                        setattr(tgt_bone, attr, getattr(bone, attr))

            tgt_bone.use_connect = False
            tgt_bone.use_deform = False
            tgt_bone.layers = layers

            new_bones.append(tgt_bone)
            constraint_map.append({"name": bone.name, "target": tgt_bone_name})

        # Re-create the hyerarchy on the target bones
        for bone in new_bones:
            if not bone.parent or bone.parent == root:
                continue

            parent_name = make_tgt_name(bone.parent.name)
            new_parent = armature_data.edit_bones.get(parent_name)
            if not new_parent:
                new_parent = root

            bone.parent = new_parent

        # Switch to pose mode to create constraints
        bpy.ops.object.mode_set(mode='POSE')
        for item in constraint_map:
            cst = pose.bones[item["name"]].constraints.new("COPY_TRANSFORMS")
            cst.target = armature
            cst.subtarget = item["target"]

        return  {"FINISHED"}


    def invoke(self, context, _event):
        return self.execute(context)
