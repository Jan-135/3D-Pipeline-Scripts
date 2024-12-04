import unreal
import os
import re

def extract_version(filename):
    """
    Extracts the version number in the format 'v<number>' from the filename.
    
    Args:
        filename (str): The name of the file to extract the version from.
        
    Returns:
        int: The version number if found, otherwise -1.
    """
    match = re.search(r"v(\d+)(?=\.\w+$)", filename)
    return int(match.group(1)) if match else -1

def find_latest_version(files):
    """
    Finds the file with the highest version number from a list of files.
    
    Args:
        files (list): List of file names to check for the latest version.
        
    Returns:
        str or None: The file name of the latest version, or None if no versioned files are found.
    """
    latest_file = None
    highest_version = -1
    for file in files:
        version = extract_version(file)
        if version > highest_version:
            highest_version = version
            latest_file = file
    return latest_file

def create_unreal_folders(source_path, unreal_base_path):
    """
    Creates the same folder structure in Unreal as on the disk and imports only the latest version of files, 
    if not already imported.
    
    Args:
        source_path (str): The root folder on the disk containing the assets.
        unreal_base_path (str): The base folder path in Unreal where assets will be imported.
    """
    for character_folder in os.listdir(source_path):
        character_path = os.path.join(source_path, character_folder)
        if os.path.isdir(character_path):
            character_unreal_path = f"{unreal_base_path}/{character_folder}"
            create_folder_if_not_exists(character_unreal_path)
            
            for scene_folder in os.listdir(character_path):
                scene_path = os.path.join(character_path, scene_folder)
                if os.path.isdir(scene_path):
                    scene_unreal_path = f"{character_unreal_path}/{scene_folder}"
                    create_folder_if_not_exists(scene_unreal_path)

                    animation_files = [f for f in os.listdir(scene_path) if f.endswith(".fbx")]
                    latest_file = find_latest_version(animation_files)
                    if latest_file:
                        animation_path = os.path.join(scene_path, latest_file)
                        unreal_asset_path = f"{scene_unreal_path}/{latest_file[:-4]}"
                        if not unreal.EditorAssetLibrary.does_asset_exist(unreal_asset_path):
                            import_fbx_to_unreal(scene_unreal_path, latest_file, animation_path)
                        else:
                            print(f"Latest version already imported: {latest_file}")

def create_folder_if_not_exists(folder_path):
    """
    Creates the specified folder in Unreal if it does not already exist.
    
    Args:
        folder_path (str): The path of the folder to create in Unreal.
    """
    if not unreal.EditorAssetLibrary.does_directory_exist(folder_path):
        unreal.EditorAssetLibrary.make_directory(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

def import_fbx_to_unreal(unreal_asset_path, animation_file, fbx_file_path):
    """
    Imports the specified FBX file into Unreal and removes the versioning from the asset name.
    
    Args:
        unreal_asset_path (str): The path in Unreal where the asset should be imported.
        animation_file (str): The name of the FBX file to import.
        fbx_file_path (str): The file path to the FBX file on disk.
    """
    base_name = re.sub(r"_v\d+$", "", animation_file[:-4]) 

    task = unreal.AssetImportTask()
    task.filename = fbx_file_path  
    task.destination_path = unreal_asset_path
    task.destination_name = f"anim_{base_name}"  
    task.replace_existing = True 

    import_ui = unreal.FbxImportUI()
    import_ui.set_editor_property("import_as_skeletal", False)
    import_ui.set_editor_property("import_materials", True)
    import_ui.set_editor_property("import_textures", True)
    import_ui.set_editor_property("import_mesh", True)

    task.options = import_ui

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])

    print(f"Import complete: {fbx_file_path} as {task.destination_name} into {unreal_asset_path}")

if __name__ == "__main__":
    source_path = "N:/GOLEMS_FATE/animations"
    unreal_base_path = "/Game/ASSETS/Animations"

    create_unreal_folders(source_path, unreal_base_path)
    print("Completed successfully!")
