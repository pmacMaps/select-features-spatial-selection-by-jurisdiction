# Select Features Meeting a Spatial Selection Test By Jurisdiction

This repository contains a sample ArcGIS geoprocessing tool, and the Python scripts that power it.  This tool works well whenever you need to get all of the features from Dataset A (i.e., building structures) that intersect Dataset B (i.e., floodplains), for each feature in Dataset C (i.e., municipalities).

There are two Python scripts used in the tool:

1. **select_features_by_jurisdiction.py** - Runs the logic of the tool, including processing the user form inputs.
2. **errorLogger.py** - Handles any errors that occur in the Except statements.  I use this module in many of my custom geoprocessing tools.  Feel free to use this as needed. 

There are eleven user inputs for the tool's form:

1. **Project Directory** (directory): The file system directory (folder) where the project file geodatabase will be created.

2. **Project Geodatabase Name** (string): The name for the file geodatabase that is created to store the output datasets of the tool.

3. **Target Layer** (feature class): The layer that you want to perform the spatial analysis and features by jurisdiction on (i.e., Building Structures). 

4. **Target Layer Name** (string): The name of the layer that you want to perform the spatial analysis and features by jurisdiction on (i.e., Building Structures). This will be used in the tool's system message and the naming of the output datasets.

5. **Selection Layer** (feature class): The spatial analysis layer that the Target Layer will be tested against (i.e., Floodplains). A Select By Location analysis will be performed.

6. **Selection Layer Name** (string): The name of the spatial analysis layer. This will be used in the tool's system message and the naming of the output datasets.

7. **Spatial Selection Type** (drop-down list): The Overlap Type for the Select By Location Analysis  tool.  See the [Esri help reference](http://desktop.arcgis.com/en/arcmap/10.5/tools/data-management-toolbox/select-layer-by-location.htm).

8. **Search Distance** (double; optional input): The optional search distance. Some spatial selection types support this.  From the help: the "tool evaluates a spatial relationship in the coordinate system of the Input Feature Layer data source (the feature class on disk)."  It is possible to set the output coordinate system to evaluate the spatial relationship in.  This is a modification you would need to make to the tool.  See the [Esri help](http://desktop.arcgis.com/en/arcmap/10.5/tools/environments/output-coordinate-system.htm) for more details. 

9. **Jurisdiction Layer** (feature class): The layer that will be cycled over to perform the spatial analysis (i.e. Municipalities).

10. **Jurisdiction Layer Name** (string): The name of jurisdictional layer. This will be used in the tool's system message and the naming of the output datasets.

11. **Jurisdiction Layer Name Field** (string): The name of the field (case-sensitive) in the Jurisdiction layer that represents the name of each feature. For a Municipalities layer, the field may be "MUNI" or "NAME".

I also added a function that converts periods ("."), spaces (" "), or dashed ("-") to underscores in the output file name.  An improvement could be a broader regex that replaces "bad characters" with an underscore.