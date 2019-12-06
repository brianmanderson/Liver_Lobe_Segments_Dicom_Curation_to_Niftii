__author__ = 'Brian M Anderson'
# Created on 12/6/2019

from Make_Single_Images.Make_Single_Images_Class import main
from Distribute_Patients import distribute_patients_by_folder


distribute_patients_by_folder()  # This will make sure the distribution file exists and break the patients up
main(path=r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\New_Niftii_Arrays\CT')