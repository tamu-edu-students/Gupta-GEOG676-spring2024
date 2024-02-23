import arcpy
import time

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GEOG676_MapTools"
        self.alias = "GEOG676_MapTools"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "create a graduated color map based on a specific attribute of a layer"
        self.canRunInBackground = False # Only used in ArcMap
        self.category = "Map Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayerToClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Output Folder",
            name="OutputFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Define our progressor variables
        readTime = 3
        start = 0
        maximum = 100
        step = 33

        # Setup the progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, maximum, step)
        time.sleep(readTime)
        # Add message to the results pane
        arcpy.AddMessage("Validating Project File...")

        #Project file
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)
        campus = project.listMaps('Map')[0]

        # Increment the progressor and change the label; add message to the results pane
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        for layer in campus.listLayers():
            # Check if layer is a feature layer
            if layer.isFeatureLayer:
                # Obtain a copy of the layer's symbology
                symbology = layer.symbology
                # Check if it has a 'renderer' attribute
                if hasattr(symbology, 'renderer'):

                    # Check if the layer's name is 'GarageParking'
                    if layer.name == parameters[1].valueAsText:    
                        # Increment the progressor and change the label; add message to the results pane
                        arcpy.SetProgressorPosition(start + step * 2)
                        arcpy.SetProgressorLabel("Calculating and Classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and Classifying...")      

                        # Update the copy's renderer to be 'GraduatedColorsRenderer'
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        # Tell arcpy which field we want to base our choropleth off of
                        symbology.renderer.classificationField = "Shape_Area"

                        arcpy.SetProgressorPosition(start + step * 2 + 1)
                        arcpy.SetProgressorLabel("Cleaning up...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Cleaning up...") 

                        # Set how many classes we'll have 
                        symbology.renderer.breakCount = 5

                        # Set the color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

                        # Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology # Very important step

                        arcpy.AddMessage("Finish generating layer...")  
                        
                    else:
                        print("Feature layer not found")

        # Increment the progressor and change the label; add message to the results pane
        arcpy.SetProgressorPosition(start + step * 3)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")
        project.saveACopy(parameters[2].valueAsText + '\\' + parameters[3].valueAsText + '.aprx')
        return None
    
    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return