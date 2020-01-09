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
from Fix_Overlapping_Structures import Fill_Segments, os
Fill_Segments(base_path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Images',
              data_path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\New_Niftii_Arrays',
              images_desc='Redone_Liver_Segments',
              excel_file_path=os.path.join('..','train_test_validation_distribution.xlsx'),
              write_data=True)
'''
Next, we need to correct them
'''