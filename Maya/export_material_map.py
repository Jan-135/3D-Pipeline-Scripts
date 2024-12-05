# Standard library imports
from pathlib import Path
import json

# Third-party imports
import pymel.core as pc

# Typing imports
from typing import List, Dict, Optional

def get_materials(shape: pc.nodetypes.Mesh) -> List[pc.nodetypes.ShadingEngine]:
    """
    Retrieves all materials connected to the provided shape node.
    
    Args:
        shape (Shape): The shape node to process.

    Returns:
        List[ShadingEngine]: A list of material nodes connected to the shape.
    """
    shading_groups = shape.listConnections(type="shadingEngine")
    materials = []
    for sg in shading_groups:
        materials.extend(sg.surfaceShader.listConnections())
    return materials

def get_file(material: pc.nodetypes.ShadingEngine, channel: str) -> Optional[str]:
    """
    Gets the file path of a texture connected to a specified material channel.

    Args:
        material (ShadingEngine): The material node to check.
        channel (str): The material channel to query (e.g., "baseColor").

    Returns:
        Optional[str]: The file path of the texture if found, otherwise None.
    """
    file_nodes = material.attr(channel).listConnections(type="file")
    if file_nodes:
        return file_nodes[0].attr("fileTextureName").get()
    return None

def get_object_to_material_map(object_list: List[pc.nodetypes.Transform], channel_list: List[str]) -> Dict[str, Dict[str, Optional[str]]]:
    """
    Generates a dictionary mapping objects to their materials and associated textures.
    
    Args:
        object_list (List[Transform]): List of transform nodes representing objects.
        channel_list (List[str]): List of material channels to query.

    Returns:
        Dict[str, Dict[str, Optional[str]]]: A mapping of object names to their materials and texture file paths.
    """
    object_to_material_map: Dict[str, Dict[str, Optional[str]]] = {}
    used_shader = set()

    for obj in object_list:
        shape = obj.getShape()
        if not shape:
            continue

        materials = get_materials(shape)
        if not materials:
            continue

        material = materials[0]
        if material not in used_shader:
            file_map = {
                channel: get_file(material, channel) for channel in channel_list
            }
            object_to_material_map[obj.name()] = file_map
            used_shader.add(material)  

    return object_to_material_map

def get_selected_objects() -> Optional[List[pc.nodetypes.Transform]]:
    """
    Retrieves all visible objects under the selected group in the scene.

    Returns:
        Optional[List[Transform]]: A list of transform nodes for all visible objects in the group.
    """
    sel = pc.selected()
    if not sel:
        pc.warning("Please select a top-level group.")
        return None
        
    output = []
    
    for elem in sel:
        all_transforms = [
            obj.getParent() for obj in elem.getChildren(ad=True, type="mesh") if not obj.intermediateObject.get()
        ]
        filtered_transforms = [obj for obj in all_transforms if obj.visibility.get()]
        output.extend(filtered_transforms)

    return output

def save_to_json(data: Dict[str, Dict[str, Optional[str]]], path: str) -> None:
    """
    Saves the provided data to a JSON file at the specified path.
    
    Args:
        data (Dict[str, Dict[str, Optional[str]]]): The data to save.
        path (str): The file path to save the data to.
    """
    path = Path(path)
    path.write_text(json.dumps(data, indent=4))

def execute(output_path: str) -> bool:
    """
    Main function to execute the script: get selected objects, extract material data, and save it to a JSON file.

    Args:
        output_path (str): Path to save the exported data.

    Returns:
        bool: True if the process was successful, False if an error occurred.
    """
    selected_objects = get_selected_objects()
    if not selected_objects:
        pc.warning("No objects selected. Please select at least one object.")
        return False
    
    channels: List[str] = ["baseColor", "opacity", "normalCamera", "metalness", "specularRoughness"]

    object_to_material_map = get_object_to_material_map(selected_objects, channels)

    save_to_json(object_to_material_map, output_path)
    pc.confirmDialog(title="Success", message=f"Data exported to {output_path}", button=["OK"])

    return True
