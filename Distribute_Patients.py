__author__ = 'Brian M Anderson'
# Created on 12/6/2019

from Breakdown_Train_Test_Validation_Iteration import make_distribution_file, os, save_obj, load_obj


def distribute_patients_by_folder():
    distribution_pickle_path = os.path.join('..','train_test_validation_distribution.pkl')
    if not os.path.exists(distribution_pickle_path):
        make_distribution_file()
    distribution_pickle = load_obj(distribution_pickle_path)
    data_dict = distribution_pickle['Folder']

    data_path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\New_Niftii_Arrays\CT'

    for file in os.listdir(data_path):
        if file.find('.nii') == -1:
            continue
        iteration = file.split('_')[-1]
        iteration = iteration.split('.')[0]
        if iteration[0] == 'y':
            iteration = iteration[1:]
        ext = data_dict[int(iteration)]
        out_path = os.path.join(data_path,ext)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        os.rename(os.path.join(data_path,file),os.path.join(out_path,file))
    return None


if __name__ == '__main__':
    pass
