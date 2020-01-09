__author__ = 'Brian M Anderson'
# Created on 11/26/2019

'''
This module contains code to prep from the AW into Raystation as well as iterate over any created contours
to try and make them as correct as possible
'''
# from AW_Liver_Lobes_To_Raystation.Main_Function import *
'''
Now, we have the images in Raystation, we need to export them to 
path = '\\mymdafiles\di_data1\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Images'
Do this by running Raystation_Code -> Export_RT
'''
from Fix_Overlapping_Structures import Fix_Missing_Segments_Class
'''
Next, we need to correct them
'''