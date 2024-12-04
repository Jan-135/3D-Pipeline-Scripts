bl_info = {
    "name": "Export to FBX for Unreal Engine",
    "author": "Jan Ferber",
    "version": (1, 2),
    "blender": (4, 2, 2),
    "location": "View3d > Tool",
    "warning": "",
    "wiki_url": "",
    "category": "Export Animation",
}

import os
import bpy

CHARACTER_OPTIONS: list[tuple[str, str, str]] = [
    ("Maurice", "Maurice", ""),
    ("Mother_Golem", "Golem Mutter", ""),
    ("Bird", "Vogel", ""),
    ("Test", "Test", ""),
]

SCENE_OPTIONS: list[tuple[str, str, str]] = [
    (f"Szene {i:03d}", f"scene{i:03d}", "") for i in range(2, 20)
]
SCENE_OPTIONS.append(("Test", "Test", ""))

bpy.types.Scene.character_selector = bpy.props.EnumProperty(
    name="Select Character",
    description="Choose the character for the animation export",
    items=CHARACTER_OPTIONS,
)

bpy.types.Scene.scene_selector = bpy.props.EnumProperty(
    name="Select Scene",
    description="Choose the scene for the animation export",
    items=SCENE_OPTIONS,
)

def get_next_version(export_path: str, character: str, scene: str) -> int:
    """
    Determines the next available version number for the export file.

    Args:
        export_path (str): The base directory for exports.
        character (str): The selected character.
        scene (str): The selected scene.

    Returns:
        int: The next available version number for the export file.
    """
    existing_files = [
        f for f in os.listdir(export_path)
        if f.startswith(f"{character}_{scene}_v")
    ]
    version_numbers = [
        int(file.split("_")[2][1:]) for file in existing_files if "_v" in file
    ]
    return max(version_numbers, default=0) + 1

class ExportToFBXOperator(bpy.types.Operator):
    """
    Operator to export selected animations to FBX for Unreal Engine.

    This operator handles the export process for selected objects in the 
    Blender scene. It saves the exported file in a structured directory 
    based on the character and scene selected by the user.
    """
    bl_idname = "export_scene.fbx_unreal"
    bl_label = "Export to FBX for Unreal"

    def execute(self, context: bpy.types.Context) -> set[str]:
        """
        Executes the export process.
        
        Args:
            context (bpy.context): Blender's context object.

        Returns:
            set: A set containing 'FINISHED' if the operation succeeds.
        """
        selected_character: str = context.scene.character_selector
        selected_scene: str = context.scene.scene_selector

        base_path: str = "N:/GOLEMS_FATE/animations"
        export_path: str = os.path.join(base_path, selected_character, selected_scene)

        if not os.path.exists(export_path):
            os.makedirs(export_path)

        version: int = get_next_version(export_path, selected_character, selected_scene)
        export_file_name: str = f"{selected_character}_{selected_scene}_v{version}.fbx"
        export_file_path: str = os.path.join(export_path, export_file_name)

        bpy.ops.export_scene.fbx(
            filepath=export_file_path,
            use_selection=True,
            apply_scale_options="FBX_SCALE_NONE",
            bake_anim=True,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            object_types={"ARMATURE"},
            mesh_smooth_type="OFF",
            use_armature_deform_only=False,
            add_leaf_bones=False,
            axis_forward="X",
            axis_up="Z",
            global_scale=1.0,
        )

        self.report(
            {"INFO"},
            f"Exported {selected_character} animation in {selected_scene} to FBX successfully!",
        )
        return {"FINISHED"}

class ExportFBXPanel(bpy.types.Panel):
    """
    UI Panel for exporting animations to FBX.

    This panel provides a user interface for selecting the character and
    scene, and triggering the export process via a button.
    """
    bl_label = "Export to FBX for Unreal"
    bl_idname = "PT_ExportFBXPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Export to FBX"

    def draw(self, context: bpy.types.Context) -> None:
        """
        Draws the UI elements in the panel.

        Args:
            context (bpy.context): Blender's context object.
        """
        layout = self.layout
        layout.label(text="Export Animations to FBX", icon="EXPORT")
        layout.prop(context.scene, "character_selector", text="Character")
        layout.prop(context.scene, "scene_selector", text="Scene")
        layout.operator("export_scene.fbx_unreal", text="Export to FBX")

def register() -> None:
    """
    Registers the operator and panel with Blender.
    """
    bpy.utils.register_class(ExportToFBXOperator)
    bpy.utils.register_class(ExportFBXPanel)
    bpy.types.Scene.character_selector = bpy.props.EnumProperty(items=CHARACTER_OPTIONS)
    bpy.types.Scene.scene_selector = bpy.props.EnumProperty(items=SCENE_OPTIONS)

def unregister() -> None:
    """
    Unregisters the operator and panel from Blender.
    """
    bpy.utils.unregister_class(ExportToFBXOperator)
    bpy.utils.unregister_class(ExportFBXPanel)
    del bpy.types.Scene.character_selector
    del bpy.types.Scene.scene_selector

if __name__ == "__main__":
    register()
