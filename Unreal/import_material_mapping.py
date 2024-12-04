import json
import os
from pathlib import Path

import unreal

from tkinter import Tk, Label, Button, filedialog, simpledialog
from tkinter.ttk import *


def get_material_map(path):
    """
    Loads the material mapping from a JSON file.
    
    Args:
        path (Path): Path to the JSON file containing the material map.

    Returns:
        dict: The material map loaded from the JSON file.
    """
    return json.load(path.open())

def get_file_location(object, channel, object_to_material_map):
    """
    Retrieves the file path for a specific object and channel from the material map.

    Args:
        object (str): The object name.
        channel (str): The channel name (e.g., baseColor, normalCamera).
        object_to_material_map (dict): A dictionary mapping objects to channels and file paths.

    Returns:
        str: The file path corresponding to the object and channel, or None if not found.
    """
    for obj, channel_map in object_to_material_map.items():
        if object == obj:
            for chan, file in channel_map.items():
                if channel == chan:
                    return file

def create_material(asset_name, package_path):
    """
    Creates a new material asset in the specified package path.

    Args:
        asset_name (str): The name of the new material.
        package_path (str): The Unreal Engine content path for the material.

    Returns:
        unreal.Material: The created material asset, or None if creation failed.
    """
    material_factory = unreal.MaterialFactoryNew()
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    new_material = asset_tools.create_asset(
        asset_name=asset_name,
        package_path=package_path,
        asset_class=unreal.Material,
        factory=material_factory
    )

    if new_material:
        new_material.set_editor_property("two_sided", True)
        unreal.EditorAssetLibrary.save_loaded_asset(new_material)
        return new_material
    else:
        print("Error: Material creation failed.")
        return None

def import_texture(file_path, destination_path):
    """
    Imports a texture from the specified file path into Unreal Engine.

    Args:
        file_path (Path): The file path of the texture to import.
        destination_path (str): The Unreal Engine content path for the texture.

    Returns:
        unreal.Texture: The imported texture asset, or None if import failed.
    """
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(file_path))
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("automated", True)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    imported_asset = task.get_editor_property("imported_object_paths")
    if imported_asset:
        imported_texture = unreal.EditorAssetLibrary.load_asset(imported_asset[0])
        return imported_texture
    else:
        print(f"Error: Texture '{file_path}' import failed.")
        return None

def add_one_texture_to_material(material, texture, channel):
    """
    Adds a single texture to a material at the specified channel.

    Args:
        material (unreal.Material): The material to which the texture will be added.
        texture (unreal.Texture): The texture to add.
        channel (unreal.MaterialProperty): The material property to which the texture will be connected.
    """
    editor_subsystem = unreal.MaterialEditingLibrary
    texture_sample = editor_subsystem.create_material_expression(
        material,
        unreal.MaterialExpressionTextureSample,
    )
    texture_sample.texture = texture

    if channel == unreal.MaterialProperty.MP_NORMAL:
        texture_sample.sampler_type = unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
    editor_subsystem.connect_material_property(texture_sample, "RGB", channel)

def remap_channels(data, remap_dict):
    """
    Remaps the channels in the material map based on a provided dictionary.

    Args:
        data (dict): The material map to be remapped.
        remap_dict (dict): A dictionary defining the remapping of channels.

    Returns:
        dict: The updated material map with remapped channels.
    """
    updated_data = {}
    for obj, channels in data.items():
        updated_channels = {}
        for old_channel, texture_path in channels.items():
            new_channel = remap_dict.get(old_channel)
            if new_channel:
                updated_channels[new_channel] = texture_path
        updated_data[obj] = updated_channels
    return updated_data

def add_all_textures_to_material(material, material_map):
    """
    Adds all textures from the material map to the material.

    Args:
        material (unreal.Material): The material to which textures will be added.
        material_map (dict): A mapping of channels to texture file paths.
    """
    for channel, origin in material_map.items():
        if origin:
            destination = unreal.EditorAssetLibrary.get_path_name(material)
            texture = import_texture(origin, destination)
            if texture:
                add_one_texture_to_material(material, texture, channel)

def select_json_file():
    """Prompts the user to select a JSON file."""
    json_file_path = filedialog.askopenfilename(
        initialdir="N:/GOLEMS_FATE/character",
        title="Select a JSON file",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if json_file_path:
        print("Selected JSON file:", json_file_path)
        return json_file_path
    else:
        print("No file selected.")
        return None



def get_user_input(object_to_material_map):
    """
    Prompts the user for asset names based on the number of objects in the JSON file.
    Returns a list of asset names corresponding to each object.
    """
    selected_paths = unreal.EditorUtilityLibrary.get_selected_folder_paths()

    if not selected_paths:
        raise ValueError("No folder selected in the Content Browser.")
    else:
        content_path = selected_paths[0]
        
        if content_path.startswith("/All/"):
            content_path = content_path.replace("/All", "", 1)
        
        unreal.log(f"Using selected folder: {content_path}")

    json_file_path = select_json_file()

    object_to_material_map = get_material_map(Path(json_file_path))

    asset_names = {}
    for obj in object_to_material_map.keys():
        asset_name = simpledialog.askstring(
            "Asset Name", f"Enter the name for the material of object '{obj}':"
        )
        if not asset_name:
            raise ValueError(f"No asset name provided for object '{obj}'.")
        asset_names[obj] = asset_name

    return Path(json_file_path), asset_names, content_path


def show_start_dialog():
    """
    Displays a dialog asking the user if they want to proceed.
    Returns True if the user agrees, False if they cancel.
    """
    # Initialize Tkinter window
    root = Tk()
    root.title("Choose a JSON File")
    root.geometry("300x100")
    user_choice = {"continue": False}

    def on_continue():
        user_choice["continue"] = True
        root.destroy()

    def on_cancel():
        user_choice["continue"] = False
        root.destroy()

    Label(root, text="Please select a JSON file").pack(pady=10)
    Button(root, text="Select File", command=on_continue).pack(side="left", padx=20)
    Button(root, text="Cancel", command=on_cancel).pack(side="right", padx=20)

    root.mainloop()
    return user_choice["continue"]


def start_script():
    """Main function that orchestrates the process of material creation and texture import."""
    try:
        if not show_start_dialog():
            unreal.log_warning("Script was canceled by the user.")
            return

        json_path, asset_names, package_path = get_user_input({})

        unreal.log(f"JSON Path: {json_path}")
        unreal.log(f"Asset Names: {asset_names}")
        unreal.log(f"Package Path: {package_path}")

        channel_remap = {
            "baseColor": unreal.MaterialProperty.MP_BASE_COLOR,
            "opacity": unreal.MaterialProperty.MP_OPACITY,
            "normalCamera": unreal.MaterialProperty.MP_NORMAL,
            "metalness": unreal.MaterialProperty.MP_METALLIC,
            "specularRoughness": unreal.MaterialProperty.MP_ROUGHNESS
        }

        object_to_material_map = get_material_map(json_path)
        mapped_data = remap_channels(object_to_material_map, channel_remap)
        print("*** Here is the new map:", mapped_data, "***")

        for obj, material_map in mapped_data.items():
            material = create_material(asset_names[obj], package_path)
            if material:
                print(f"Material {asset_names[obj]} created for {obj}.")
                add_all_textures_to_material(material, material_map)

    except ValueError as e:
        unreal.log_error(f"Script aborted: {e}")
    except Exception as e:
        unreal.log_error(f"Error in script: {e}")

if __name__ == "__main__":
    start_script()