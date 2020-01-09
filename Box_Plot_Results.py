__author__ = 'Brian M Anderson'
# Created on 11/25/2019

import matplotlib.pyplot as plt
import pickle
import pandas as pd


def load_obj(path):
    if path[-4:] != '.pkl':
        path += '.pkl'
    with open(path, 'rb') as f:
        return pickle.load(f)

def get_data(data):
    output = []
    for pat_name in data:
        output.append(pat_name + ',' + str(data[pat_name]['Overlap_Results']['dice']))
    return output

# 'Abdomen_1k_batch_5_2classes_Liver_3_Layer_256_limited_batch'
path = r'Y:\CNN\For_DGX_Station\Projects\Segmentation\Liver_Lobe_Segments\no_processing.xlsx'

data = pd.read_excel(path)
segment_data = {}
for i in range(1,9):
    segment_data[i] = data[i]


x_ticks = [str(i) for i in range(1,9)]
num_labels = [i for i in range(1,9)]
# 0,.1,.2,.3,.4,.5,.6,.7,
y_ticks = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

# y_tick_distance = [0,10,20,35]
title = 'Lobe Segments DSC'
plt.figure(0)
plt.suptitle(title)
ax = plt.subplot(1,1,1)
metric = 'Overlap_Results'
plt.boxplot([segment_data[i] for i in range(1,9)])
plt.xlabel('Liver Lobe Segments')
plt.ylabel('Dice Simiarlity Coefficient')
plt.xticks(num_labels,x_ticks)
plt.yticks(y_ticks)
plt.show()
