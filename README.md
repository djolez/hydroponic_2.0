# hydroponic_2.0

This is a continuation of the project from the course of ***"Pervasive Systems 2016"*** that will be used as a Master thesis topic within the MSc in Computer Science at the ***Sapienza University of Rome***. Previous project can be found here: https://github.com/djolez/hydroponic.

Basic idea is to upgrade the old system in a way that is going to provide support for growing plants that require different growing conditions (nutrient strength, watering schedule, etc.) and automate the operation as much as possible (regulating pH and Electrical Conductivity levels, topping off nutrient solution and mixing nutrients). This will be achieved by making a multi site ebb and flow system, pictured below.

![alt tag](https://s3.amazonaws.com/media.hydroponics.net/images/MultiFlow-med.jpg)

Plants are organised in lines, where each line is used for plants that require the same watering schedule and nutrient strength, since there can be multiple nutrient containers (light blue) with different mix of nutrients that pump water into the control bucket, the one next to it. 

![alt tag](http://i.imgur.com/oSVWamJ.jpg)

During the flooding period as the water level rises in the control bucket it also rises in the lines that are currently open. There are float switches that regulate min and max level of water in the control bucket, pumps for filling/draining and a solenoid valve for controlling each line.

System will consist of multiple independent modules connected to a server that is going to be responsible for collecting and monitoring the data from sensors and controlling actuators located in these modules.

This is the outline of the basic system functionality and this document will be updated as the project evolves.
