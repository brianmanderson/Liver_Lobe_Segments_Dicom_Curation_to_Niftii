__author__ = 'Brian M Anderson'
# Created on 11/26/2019
import pandas as pd
import os


data_dict = {}
path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Images'
for MRN in os.listdir(path):
    exams = os.listdir(os.path.join(path,MRN))
    data_dict[MRN] = exams

fid = open(os.path.join('.','exam_check_list.txt'),'w+')
for MRN in data_dict:
    fid.write(MRN + ',')
    for exam in data_dict[MRN]:
        fid.write(exam + ',')
    fid.write('\n')
fid.close()
# df = pd.DataFrame(data_dict).T
# df.to_excel(os.path.join('.','output.xlsx'))