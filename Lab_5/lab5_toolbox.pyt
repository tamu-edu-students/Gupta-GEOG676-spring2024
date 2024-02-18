# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"
        # List of tool classes associated with this toolbox
        self.tools = [tool]

class tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRunInBackground = False # Only used in ArcMap
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="CampusGDB",
            datatype="DEType",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1,param2,param3,param4, param5]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        #Create a geodatabase 
        gdb_path = folder_path + "\\" + gdb_name
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        #Read in garage location X/Y coords from the provided CSV file.
        csv_path = parameters[2].valueAsText
        garages_layer_name = parameters[3].valueAsText
        garages = arcpy.management.MakeXYEventLayer(csv_path, "x", "y", garages_layer_name)

        #add in the input layers
        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + "\\" + garages_layer_name

        campus = parameters[4].valueAsText
        buildings_campus = campus + "\Structures"
        buildings = gdb_path + "\\Buildings"
        arcpy.Copy_management(buildings_campus,buildings)

        spatial_reference = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path+'\Garage_points_reprojected', spatial_reference) 

        #Buffer the garage points
        buffer_distance = int(parameters[5].valueAsText)
        garage_buffered = arcpy.Buffer_analysis(gdb_path+'\Garage_points_reprojected', gdb_path+'\Garage_points_buffered', buffer_distance)

        #Intersect the buildings layer with the buffered garage points
        arcpy.Intersect_analysis([garage_buffered, buildings], gdb_path+'\Garage_Building_Intersection','ALL')

        #Output the resulting table to a CSV file
        arcpy.TableToTable_conversion(gdb_path+ '\Garage_Building_Intersection.dbf', folder_path, 'nearby_buildings.csv')
        
        return None

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
