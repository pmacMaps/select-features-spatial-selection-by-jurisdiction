# ---------------------------------------------------------------------------
# Name: Select Features By Spatial Selection By Jurisdiction
#
# Author: Patrick McKinney, Cumberland County GIS (pmckinney@ccpa.net or pnmcartography@gmail.com)
#
# Created on: 1/23/19
#
# Updated on: 1/23/19
#
# Description: [complete this]
#
# Disclaimer: CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.
# Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
# of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
# herein. The user assumes the risk that the information may not be accurate.
# ---------------------------------------------------------------------------

# Import system modules
import arcpy, datetime, os, errorLogger

# function to convert dash or whitespace to underscore
# a more broad regex could be used here
def convertToUnderscore(user_string):
    # dash condition
    if "-" in user_string:
        user_string = user_string.replace("-","_")
    # space condition
    elif " " in user_string:
        user_string = user_string.replace(" ","_")
    # period condition
    elif "." in user_string:
        user_string = user_string.replace(".","_")
    else:
        pass
    return user_string
# end function

# Run geoprocessing tool.
# If there is an error with the tool, it will break and run the code within the except statement
try:
    # 1. ArcGIS Tool User Form Inputs & Other Variables
    # project directory - [data type from tool]
    project_dir = arcpy.GetParameterAsText(0)
    # project geodatabase name - [data type from tool]
    project_gdb_name = arcpy.GetParameterAsText(1)
    # target layer - layer you want to get features for by jurisdiction - [data type from tool]
    target_layer = arcpy.GetParameterAsText(2)
    target_layer_name = arcpy.GetParameterAsText(3)
    # selection layer - layer you want to perform spatial selection against target layer - [data type from tool]
    selection_layer = arcpy.GetParameterAsText(4)
    selection_layer_name = arcpy.GetParameterAsText(5)
    # spatial selection type - [data type from tool]
    spatial_overlap_type = arcpy.GetParameterAsText(6)
    selection_search_distance = float((arcpy.GetParameterAsText(7)))
    # jurisdiction layer - [data type from tool]
    jurisdiction_layer = arcpy.GetParameterAsText(8)
    jurisdiction_layer_name = arcpy.GetParameterAsText(9)
    # name field for jursidiction layer - [data type from tool]
    jurisdiction_layer_name_field = arcpy.GetParameterAsText(10)
    # field list for cursor
    jurisdiction_layer_field = ['{}'.format(jurisdiction_layer_name_field)]
    # Time stamp variables
    currentTime = datetime.datetime.now()
    # Date formatted as month-day-year (1-1-2017)
    dateToday = currentTime.strftime("%m_%d_%Y")
    search_distance_overlap_types = [' WITHIN_A_DISTANCE_GEODESIC', 'WITHIN_A_DISTANCE', 'WITHIN_A_DISTANCE_3D', 'INTERSECT', 'INTERSECT_3D', 'HAVE_THEIR_CENTER_IN', 'CONTAINS', 'WITHIN']

    # 2. Create Project Geodatabase
    arcpy.CreateFileGDB_management(project_dir,project_gdb_name,'10.0')
    arcpy.AddMessage('\nCreated project file geodatabase named "{}" in {}'.format(project_gdb_name,project_dir))
    project_gdb = os.path.join(project_dir,'{}.gdb'.format(project_gdb_name))

    # 3. Create Feature Layers
    # jursidiction layer
    arcpy.MakeFeatureLayer_management(jurisdiction_layer, jurisdiction_layer_name)
    # target layer
    arcpy.MakeFeatureLayer_management(target_layer, target_layer_name)
    # selection layer
    arcpy.MakeFeatureLayer_management(selection_layer, selection_layer_name)
    arcpy.AddMessage('\nCreated feature layers for datasets')

    # 4. Create Search Cursor for Jursidiction Layer
    arcpy.AddMessage('\nCreating search cursor on {} layer'.format(jurisdiction_layer_name))
    # create search cursor
    with arcpy.da.SearchCursor(jurisdiction_layer, jurisdiction_layer_field) as cursor:
        # loop through each record in municipalities layer
        for row in cursor:
            # add message
            arcpy.AddMessage('\nSelecting features from {} that have their centroid in {}'.format(target_layer_name,row[0]))
            # attribute selection on jurisdiction layer
            # SQL query
            where_clause = "{} = '{}'".format(jurisdiction_layer_name_field,row[0])
            arcpy.SelectLayerByAttribute_management(jurisdiction_layer_name, 'NEW_SELECTION',where_clause)
            # select target layer features that have centroid in jurisdiction layer
            arcpy.SelectLayerByLocation_management(target_layer_name, 'HAVE_THEIR_CENTER_IN', jurisdiction_layer_name, selection_type='NEW_SELECTION')
            # get count of target layer features that have centroid in jursidiction layer
            match_count_target = int(arcpy.GetCount_management(target_layer_name)[0])
            # make sure features are selected before moving forward
            if match_count_target > 0:
                # select from selected target layer features that meet spatial selection criteria for selection layer
                if spatial_overlap_type not in search_distance_overlap_types:
                    arcpy.SelectLayerByLocation_management(target_layer_name, spatial_overlap_type, selection_layer_name, selection_type='SUBSET_SELECTION')
                else:
                    arcpy.SelectLayerByLocation_management(target_layer_name, spatial_overlap_type, selection_layer_name, selection_search_distance, selection_type='SUBSET_SELECTION')
                # get count of selected features from target layer
                match_count_target_selection = int(arcpy.GetCount_management(target_layer_name)[0])
                # make sure features are selected before moving forward
                if match_count_target_selection > 0:
                    # add message
                    arcpy.AddMessage('\n\tThere are {} features from {} that {} {} in {}'.format(match_count_target_selection, target_layer_name,spatial_overlap_type,selection_layer_name,row[0]))
                    # remove dashes and spaces from names for output layer
                    target_layer_name_fixed = convertToUnderscore(target_layer_name)
                    selection_layer_name_fixed = convertToUnderscore(selection_layer_name)
                    jurisdiction_layer_name_fixed = convertToUnderscore(row[0])
                    # export layer
                    arcpy.CopyFeatures_management(target_layer_name, os.path.join(project_gdb, '{}_{}_{}_{}'.format(target_layer_name_fixed,spatial_overlap_type,selection_layer_name_fixed,jurisdiction_layer_name_fixed)))
                    arcpy.AddMessage('\n\tExported features from {} for {} to {}'.format(target_layer_name, row[0], project_gdb))
                else:
                    arcpy.AddWarning('\n\tNo features from {} that are within {} {} {}'.format(target_layer_name,row[0],spatial_overlap_type,selection_layer_name))
            else:
                arcpy.AddWarning('\n\tThere were no features from {} that have their centroids in {}\n'.format(target_layer_name,row[0]))
            # end if/else
        # end for
    # end with cursor
# If an error occurs running geoprocessing tool(s) capture error and write message
# handle error outside of Python system
except EnvironmentError as e:
    arcpy.AddError('\nAn error occured running this tool. Please review the following error messages:')
    # call error logger method
    errorLogger.PrintException(e)
# handle exception error
except Exception as e:
    arcpy.AddError('\nAn error occured running this tool. Please review the following error messages:')
    # call error logger method
    errorLogger.PrintException(e)