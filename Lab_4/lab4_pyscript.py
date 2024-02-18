import arcpy

arcpy.env.workspace = "C:\\tmp\ArcGISPython\Lab4"

folder_path = "C:\\tmp\ArcGISPython\Lab4"

#Create a geodatabase 
gdb_path = folder_path + "\\Test.gdb"
arcpy.CreateFileGDB_management(folder_path, "Test.gdb")

#Read in garage location X/Y coords from the provided CSV file.
garages_layer_name = "Garages"
csv_path = "C:\\tmp\ArcGISPython\garages.csv"
garages = arcpy.management.MakeXYEventLayer(csv_path, "x", "y", garages_layer_name)

#add in the input layers
arcpy.FeatureClassToGeodatabase_conversion(garages, gdb_path)
garage_points = gdb_path + '\\' + garages_layer_name

Campus = "C:\\tmp\ArcGISPython\Campus.gdb"
buildings_campus = Campus + "\Structures"
buildings = gdb_path + "\\Buildings"
arcpy.Copy_management(buildings_campus, buildings)

spatial_reference = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points,gdb_path + '\Garage_points_reprojected', spatial_reference) 

#Buffer the garage points
garage_buffered = arcpy.Buffer_analysis(gdb_path + '\Garage_points_reprojected', gdb_path + '\Garage_points_buffered', 150)

#Intersect the buildings layer with the buffered garage points
arcpy.Intersect_analysis([garage_buffered,buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')

#Output the resulting table to a CSV file
arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection', folder_path, 'nearby_buildings.csv')

print(arcpy.GetMessages())