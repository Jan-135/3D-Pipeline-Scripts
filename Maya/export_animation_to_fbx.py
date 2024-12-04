import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pc
import os

def export_fbx(export_path: str, file_name: str) -> None:
    """
    Exports the selected objects as an FBX file to the specified path.
    
    Args:
        export_path (str): The directory where the FBX file will be saved.
        file_name (str): The name of the FBX file to be created.
    """
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    full_path: str = os.path.join(export_path, file_name)

    mel.eval('FBXExportAnimationOnly -v true;') 
    mel.eval('FBXExportBakeComplexAnimation -v true;')

    try:
        pc.system.exportSelected(full_path, type="FBX export")
        print(f"Animation successfully exported as FBX to: {full_path}")
    except RuntimeError as e:
        print(f"Failed to export FBX: {e}")


def get_next_version(export_path: str, base_name: str) -> int:
    """
    Determines the next version number for an export file based on existing files in the directory.
    
    Args:
        export_path (str): The directory to check for existing files.
        base_name (str): The base name of the file, e.g., character_scene.
    
    Returns:
        int: The next available version number.
    """
    files: list[str] = [
        f for f in os.listdir(export_path)
        if f.startswith(base_name) and f.endswith(".fbx")
    ]
    version_numbers: list[int] = []

    for file in files:
        parts: list[str] = file.split("_")
        if len(parts) > 1 and parts[-1].startswith("v"):
            version: int = int(parts[-1][1:].split(".")[0])
            version_numbers.append(version)

    return max(version_numbers, default=0) + 1


def create_export_ui() -> None:
    """
    Creates a simple UI in Maya to select a character and scene, and export the animation as an FBX file.
    """
    if cmds.window("ExportUI", exists=True):
        cmds.deleteUI("ExportUI", window=True)

    window: str = cmds.window("ExportUI", title="Export FBX for Unreal", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)

    cmds.optionMenu("character_menu", label="Character")
    cmds.menuItem(label="Maurice")
    cmds.menuItem(label="Mother_Golem")
    cmds.menuItem(label="Bird")
    cmds.menuItem(label="Testosteron")

    cmds.optionMenu("scene_menu", label="Scene")
    for i in range(1, 21):  
        scene_label: str = f"Scene {i:03}" 
        cmds.menuItem(label=scene_label)

    cmds.button(label="Export FBX", command=lambda x: on_export_clicked())

    cmds.showWindow(window)


def on_export_clicked() -> None:
    """
    Callback function triggered when the 'Export FBX' button is clicked.
    It retrieves user selections, prepares the export path, and calls the export function.
    """
    character: str = cmds.optionMenu("character_menu", query=True, value=True)
    scene: str = cmds.optionMenu("scene_menu", query=True, value=True)

    base_path: str = "N:/GOLEMS_FATE/animations"
    export_path: str = os.path.join(base_path, character, scene)

    print(f"Attempting to export to: {export_path}")

    try:
        os.makedirs(export_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    version: int = get_next_version(export_path, f"{character}_{scene}")
    file_name: str = f"{character}_{scene}_v{version}.fbx"

    export_fbx(export_path, file_name)

if __name__ == "__main__":
    create_export_ui()
