# -*- coding: utf-8 -*-

import arcpy

folder_path = input("Please enter a gdb path: ")
gdb_name = input("Please enter a gdb name: ")
garages_csv = input("Please enter garages csv file path: ")
garages_layer_name = input("Please enter garages layer name: ")
campus_gdb = input("Please enter campus gdb path: ")
bufferSize_input = int(input("Please enter a buffer size: "))

folder_path = folder_path
gdb_name = gdb_name
#Create a geodatabase 
gdb_path = folder_path + "\\" + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

#Read in garage location X/Y coords from the provided CSV file.
csv_path = garages_csv
garages_layer_name = garages_layer_name
garages = arcpy.management.MakeXYEventLayer(csv_path, "x", "y", garages_layer_name)

#add in the input layers
input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + "\\" + garages_layer_name

campus = campus_gdb
buildings_campus = campus + "\Structures"
buildings = gdb_path + "\\Buildings"
arcpy.Copy_management(buildings_campus, buildings)

spatial_reference = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_points_reprojected', spatial_reference) 

#Buffer the garage points
buffer_distance = bufferSize_input
garage_buffered = arcpy.Buffer_analysis(gdb_path+'\Garage_points_reprojected', gdb_path+'\Garage_points_buffered', buffer_distance)

#Intersect the buildings layer with the buffered garage points
arcpy.Intersect_analysis([garage_buffered, buildings], gdb_path + '\Garage_Building_Intersection','ALL')

#Output the resulting table to a CSV file
arcpy.TableToTable_conversion( gdb_path + '\Garage_Building_Intersection.dbf', folder_path, 'nearby_buildings.csv')