import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pc
import os

def export_fbx(export_path, file_name):
    """
    Exports the selected objects as an FBX file to the specified path.
    
    Args:
        export_path (str): The directory where the FBX file will be saved.
        file_name (str): The name of the FBX file to be created.
    """
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    full_path = os.path.join(export_path, file_name)

    mel.eval('FBXExportAnimationOnly -v true;') 
    mel.eval('FBXExportBakeComplexAnimation -v true;')

    try:
        pc.system.exportSelected(full_path, type="FBX export")
        print(f"Animation successfully exported as FBX to: {full_path}")
    except RuntimeError as e:
        print(f"Failed to export FBX: {e}")


def get_next_version(export_path, base_name):
    """
    Determines the next version number for an export file based on existing files in the directory.
    
    Args:
        export_path (str): The directory to check for existing files.
        base_name (str): The base name of the file, e.g., character_scene.
    
    Returns:
        int: The next available version number.
    """
    files = [f for f in os.listdir(export_path) if f.startswith(base_name) and f.endswith(".fbx")]
    version_numbers = []

    for file in files:
        parts = file.split("_")
        if len(parts) > 1 and parts[-1].startswith("v"):
            version = int(parts[-1][1:].split(".")[0])
            version_numbers.append(version)


    return max(version_numbers, default=0) + 1


def create_export_ui():
    """
    Creates a simple UI in Maya to select a character and scene, and export the animation as an FBX file.
    """
    if cmds.window("ExportUI", exists=True):
        cmds.deleteUI("ExportUI", window=True)

    window = cmds.window("ExportUI", title="Export FBX for Unreal", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)

    cmds.optionMenu("character_menu", label="Character")
    cmds.menuItem(label="Maurice")
    cmds.menuItem(label="Mother_Golem")
    cmds.menuItem(label="Bird")
    cmds.menuItem(label="Testosteron")

    cmds.optionMenu("scene_menu", label="Scene")
    for i in range(1, 21):  
        scene_label = f"Scene {i:03}" 
        cmds.menuItem(label=scene_label)

    cmds.button(label="Export FBX", command=lambda x: on_export_clicked())

    cmds.showWindow(window)


def on_export_clicked():
    """
    Callback function triggered when the 'Export FBX' button is clicked.
    It retrieves user selections, prepares the export path, and calls the export function.
    """
    character = cmds.optionMenu("character_menu", query=True, value=True)
    scene = cmds.optionMenu("scene_menu", query=True, value=True)

    base_path = "N:/GOLEMS_FATE/animations"
    export_path = os.path.join(base_path, character, scene)

    print(f"Attempting to export to: {export_path}")

    try:
        os.makedirs(export_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    version = get_next_version(export_path, f"{character}_{scene}")
    file_name = f"{character}_{scene}_v{version}.fbx"

    export_fbx(export_path, file_name)

if __name__ == "__main__":
    create_export_ui()
