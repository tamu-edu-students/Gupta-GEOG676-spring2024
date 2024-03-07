import arcpy

source = "C:\\tmp\ArcGISPython\Lab7"
band1 = arcpy.sa.Raster(source + r'\band1.TIF')
band2 = arcpy.sa.Raster(source + r'\band2.TIF')
band3 = arcpy.sa.Raster(source + r'\band3.TIF')
band4=arcpy.sa.Raster(source + r'\band4.TIF')

combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + "\output_combined.TIF")

#Hillshade
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.ddd.HillShade(source + "\DEM.TIF", source + "\output_hillshade.TIF", azimuth, altitude, shadows, z_factor)

#Slope
output_measurement = "DEGREE"
z_factor = 1
# method = "PLANAR"
# z_unit = "METER"
arcpy.ddd.Slope(source + "\DEM.TIF", source + "\output_slope.TIF",output_measurement, z_factor)

print("Success!")