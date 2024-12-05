# Standard library imports
import os

# Third-party imports
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pc


def export_fbx(export_path: str, file_name: str) -> bool:
    """
    Exports the selected objects as an FBX file to the specified path.
    
    Args:
        export_path (str): The directory where the FBX file will be saved.
        file_name (str): The name of the FBX file to be created.
    
    Returns:
        bool: True if the export was successful, False otherwise.
    """
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    full_path: str = os.path.join(export_path, file_name)


    mel.eval('FBXExportAnimationOnly -v true;') 
    mel.eval('FBXExportBakeComplexAnimation -v true;')

    try:
        pc.system.exportSelected(full_path, type="FBX export")
        print(f"Animation successfully exported as FBX to: {full_path}")
        return True
    except RuntimeError as e:
        print(f"Failed to export FBX: {e}")
        return False


def get_next_version(export_path: str, base_name: str) -> int:
    """
    Determines the next version number for an export file based on existing files in the directory.
    
    Args:
        export_path (str): The directory to check for existing files.
        base_name (str): The base name of the file (e.g., character_scene).
    
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
            try:
                version: int = int(parts[-1][1:].split(".")[0])
                version_numbers.append(version)
            except ValueError:
                print(f"It exists an invalid version format")
                continue

    return max(version_numbers, default=0) + 1


def execute(scene: str, character: str) -> bool:
    """
    Executes the export process for the specified scene and character.
    Creates the necessary directories and determines the next available version number.

    Args:
        scene (str): The name of the scene to export.
        character (str): The name of the character to export.
    
    Returns:
        bool: True if the export was successful, False otherwise.
    """
    base_path: str = "N:/GOLEMS_FATE/animations"
    export_path: str = os.path.join(base_path, character, scene)
    print(f"Attempting to export to: {export_path}")

    try:
        os.makedirs(export_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory: {e}")
        return False

    version: int = get_next_version(export_path, f"{character}_{scene}")
    file_name: str = f"{character}_{scene}_v{version}.fbx"

    return export_fbx(export_path, file_name)
