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
#Hier ist ein Test

import bpy
import os

# List of characters for the dropdown menu
character_options = [
    ("Maurice", "Maurice", ""),
    ("Mother_Golem", "Golem Mutter", ""),
    ("Bird", "Vogel", ""),
    # One test folder for each character
    ("Test", "Test", ""),
]

# List of scenes for the dropdown menu
# Dynamische Erstellung der Szenen-Optionen mit einer Schleife
scene_options = [(f"Szene {i:03d}", f"scene{i:03d}", "") for i in range(2, 20)]
# One test folder for each scene
scene_options.append(("Test", "Test", ""))


# EnumProperty for character selection in the UI
bpy.types.Scene.character_selector = bpy.props.EnumProperty(
    name="Select Character",
    description="Choose the character for the animation export",
    items=character_options,
)

# EnumProperty for scene selection in the UI
bpy.types.Scene.scene_selector = bpy.props.EnumProperty(
    name="Select Scene",
    description="Choose the scene for the animation export",
    items=scene_options,
)

def get_next_version(export_path, character, scene):
    """
    Determines the next available version number for the export file.
    
    Args:
        export_path (str): The base directory for exports.
        character (str): The selected character.
        scene (str): The selected scene.

    Returns:
        int: The next version number.
    """
    
    # Gather existing files that match the naming pattern
    existing_files = [f for f in os.listdir(export_path) if f.startswith(f"{character}_{scene}_v")]
    version_numbers = []

    # Extract version numbers from filenames
    for file in existing_files:
        parts = file.split('_')
        if len(parts) > 2 and parts[2].startswith('v'):
            try:
                version_numbers.append(int(parts[2][1:]))  # Nummer nach 'v' extrahieren
            except ValueError:
                continue

    # Return 1 if no versions exist, otherwise increment the highest version
    return max(version_numbers, default=0) + 1


class ExportToFBXOperator(bpy.types.Operator):
    """
    Operator to export selected animations to FBX for Unreal Engine.
    """
    bl_idname = "export_scene.fbx_unreal"
    bl_label = "Export to FBX for Unreal"

    def execute(self, context):
        # Get selected character and scene from dropdown menus
        selected_character = context.scene.character_selector
        selected_scene = context.scene.scene_selector

        # Define base path and create subdirectories for character and scene
        base_path = "N:/GOLEMS_FATE/animations"

        export_path = os.path.join(base_path, selected_character, selected_scene)
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        # Determine the next version for the file
        version = get_next_version(export_path, selected_character, selected_scene)

        # Construct the full export file path with versioning
        export_file_name = f"{selected_character}_{selected_scene}_v{version}.fbx"
        export_file_path = os.path.join(export_path, export_file_name)

       # Ensure file does not overwrite an existing one
        while os.path.exists(export_file_path):
            version += 1  # Version um 1 erhöhen
            export_file_name = f"{selected_character}_{selected_scene}_v{version}.fbx"
            export_file_path = os.path.join(export_path, export_file_name)

        # Perform FBX export with specified settings
        bpy.ops.export_scene.fbx(
            filepath=export_file_path,           # Exportpfad
            use_selection=True,                  # Nur ausgewählte Objekte exportieren
            apply_scale_options='FBX_SCALE_NONE', # Skalierungsoption
            bake_anim=True,                      # Animationen backen
            bake_anim_use_all_bones=True,        # Alle Bones in der Animation verwenden
            bake_anim_use_nla_strips=False,      # NLA-Strips ignorieren
            bake_anim_use_all_actions=False,     # Alle Actions backen
            bake_anim_force_startend_keying=True,# Keyframes am Anfang und Ende setzen
            object_types={'ARMATURE'},           # Nur Armatures exportieren
            mesh_smooth_type='OFF',              # Smoothing-Option
            use_armature_deform_only=False,      # Nur deformierende Bones exportieren
            add_leaf_bones=False,                # Leaf-Bones weglassen
            axis_forward='X',                    # Achsen-Konfiguration
            axis_up='Z',                          # Achsen-Konfiguration
            global_scale=1.0                     # Setze den globalen Skalierungsfaktor auf 1.0
        )
        
        self.report({'INFO'}, f"Export nach FBX für {selected_character} in {selected_scene} erfolgreich!")
        return {'FINISHED'}


class ExportFBXPanel(bpy.types.Panel):
    """
    UI Panel for exporting animations to FBX.
    """
    
    bl_label = "Export to FBX for Unreal"
    bl_idname = "PT_ExportFBXPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Export to FBX'
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Sei glücklich mit dem was du hast.", icon='FUND')
        
        # Dropdown menus for character and scene selection
        layout.prop(context.scene, "character_selector", text="Character")  # Dropdown für Charakterauswahl
        layout.prop(context.scene, "scene_selector", text="Szene:")      # Dropdown für Szenenauswahl
        
        # Button to trigger the export
        row = layout.row()
        row.operator("export_scene.fbx_unreal", text="Exportiere Animation als FBX für Unreal")  # Export-Button

def register():
    bpy.utils.register_class(ExportToFBXOperator)
    bpy.utils.register_class(ExportFBXPanel)
    bpy.types.Scene.character_selector = bpy.props.EnumProperty(items=character_options)
    bpy.types.Scene.scene_selector = bpy.props.EnumProperty(items=scene_options)

def unregister():
    bpy.utils.unregister_class(ExportToFBXOperator)
    bpy.utils.unregister_class(ExportFBXPanel)
    del bpy.types.Scene.character_selector
    del bpy.types.Scene.scene_selector

if __name__ == "__main__":
    register()
