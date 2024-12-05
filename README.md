# Python Tools for Animation and Material Management in 3D Pipelines

This repository contains Python scripts to streamline workflows between **Blender**, **Maya**, and **Unreal Engine**. These tools simplify exporting animations and materials, importing those assets into Unreal Engine, and maintaining a cohesive pipeline.

## 📂 File Structure

```plaintext
main
├── Blender
│   └── export_animation_to_fbx.py
├── Maya
│   ├── export_animation_to_fbx.py
│   ├── interface_export_animation_to_fbx.py
│   ├── export_material_map.py
│   └── interface_export_material_map.py
├── Unreal
│   ├── import_fbx_animation.py
│   └── import_material_mapping.py
├── examples
│   └── (Example scripts or configurations demonstrating script usage)
└── README.md
```

## 🛠️ Scripts Overview

### Blender
1. **export_animation_to_fbx.py**  
   - Exports animations from Blender to `.fbx` format for integration into Unreal Engine.
   - Exported files are saved using a naming converntion and a version control.
   - Dynamically creates a folder structure on the hard drive.

### Maya
2. **export_animation_to_fbx.py**  
   - Similar to the Blender version, this script exports animations from Maya into `.fbx` format.
   - Exported files are saved using a naming converntion and a version control.
   - Dynamically creates a folder structure on the hard drive.
  
   
3. **interface_export_material_map.py**  
   - opens a GUI to get the users input
   - executes `export_animation_to_fbx.py`
     
4. **export_material_map.py**  
   - Captures the material texture locations from Maya shaders and stores them in a JSON file.
  
5. **interface_export_material_map.py**  
   - opens a GUI to get the users input
   - executes `export_material_map.py`

### Unreal
6. **import_fbx_animation.py**  
   - Imports `.fbx` animations into Unreal Engine, maintaining directory structures and file versions.
   - Uses the prebuilt directory structure created by the `export_animation_to_fbx.py` scripts.

6. **import_material_mapping.py**  
   - Imports material mappings from JSON files into Unreal Engine, reconstructing shaders using the stored data.

### Examples
This folder contains sample JSON files that demonstrate the output format generated by the `export_material_map.py` script.


## 🔧 Purpose and Usage Context

These scripts are custom-built to support internal workflows for a team managing animation and material pipelines across Blender, Maya, and Unreal Engine. They are tailored to meet specific project requirements and are not designed for general use or public distribution.

While the repository is accessible, its scripts assume familiarity with the corresponding tools and are provided without external setup documentation or guarantees of compatibility outside the intended use case.

### Key Goals
- Streamline the export and import of animations and materials.
- Maintain consistency in asset management across tools.
- Simplify directory structures and reduce manual file management.


## License

This project is released into the public domain. You are free to use, modify, and distribute the code in this repository for any purpose, without any restrictions.
