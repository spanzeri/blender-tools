import bpy

root_names = (
	"Root", "root", "ROOT",
	"Props", "props", "PROPS",
	"Properties", "properties", "PROPERTIES"
)

class SRT_PT_RootProperties(bpy.types.Panel):
	bl_category = "Bone Layers"
	bl_label = "Root Properties"
	bl_idname = "SRT_PT_RootProperties"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'

	@classmethod
	def poll(self, context):
		if getattr(context.active_object, 'pose', None):
			return True
		if so in context.selected_objects:
			if so.type == 'ARMATURE':
				return True

	def draw(self, context):
		layout = self.layout

		if context.mode == 'POSE' or context.mode == 'EDIT_ARMATURE':
			if context.object.type == 'ARMATURE':
				armature = context.object

		if armature:
			bones = [b for b in armature.pose.bones if b.name in root_names]

		rna_properties = {
			prop.identifier for prop in bpy.types.PoseBone.bl_rna.properties
			if prop.is_runtime
		}

		for bone in bones:
			items = tuple((
				(k, v) for (k, v) in sorted(bone.items())
				if k not in {'_RNA_UI', 'constraint_active_index'} and k not in rna_properties
			))

			if items:
				row = layout.row()
				row.label(icon = 'BONE_DATA', text = bone.name)
				box = layout.box()

			for (k, v) in items:
				print("%s = %s" % (k, v))
				row = box.row(align = True)
				row.label(text = k)
				row.prop(bone, f'["{k}"]', slider = True, text = "")
