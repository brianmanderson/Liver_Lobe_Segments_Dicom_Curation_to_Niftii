__author__ = 'Brian M Anderson'
# Created on 12/6/2019
import os, pickle
import pandas as pd


def save_obj(path, obj): # Save almost anything.. dictionary, list, etc.
    if path.find('.pkl') == -1:
        path += '.pkl'
    with open(path, 'wb') as f:
        pickle.dump(obj, f, 3)
    return None


def load_obj(path):
    if path.find('.pkl') == -1:
        path += '.pkl'
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    else:
        out = {}
        return out


path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Niftii_Arrays\CT'

data_dict = {}
for ext in ['Train','Test','Validation']:
    files = os.listdir(os.path.join(path,ext))
    iterations = [i.split('_')[-1].split('.')[0] for i in files if i.find('Overall_Data') == 0]
    for iteration in iterations:
        data_dict[int(iteration)] = ext
data_dict = {'Folder':data_dict}
save_obj(os.path.join('..','train_test_validation_distribution.pkl'),data_dict)
data_frame = pd.DataFrame(data_dict)
data_frame.to_excel(os.path.join('..','train_test_validation_distribution.xlsx'))