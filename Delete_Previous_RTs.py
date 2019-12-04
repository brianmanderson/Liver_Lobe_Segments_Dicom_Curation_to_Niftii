__author__ = 'Brian M Anderson'
# Created on 12/2/2019
import os

def down_folder(path):
    files = []
    dirs = []
    for root, dirs, files in os.walk(path):
        break
    for file in files:
        if file.find('RS') == 0:
            os.remove(os.path.join(path,file))
    for dir in dirs:
        down_folder(os.path.join(path,dir))

base_path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Images'
down_folder(base_path)