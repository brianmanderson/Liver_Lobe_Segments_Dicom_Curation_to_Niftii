__author__ = 'Brian M Anderson'
# Created on 12/6/2019

from Make_Excel_About_Image_Distribution import make_distribution_file, os, load_obj, pd


def distribute_patients_by_folder():
    distribution_excel_path = os.path.join('..','train_test_validation_distribution.xlsx')
    if not os.path.exists(distribution_excel_path):
        make_distribution_file()
    distribution_data = pd.read_excel(distribution_excel_path)
    iterations = list(distribution_data['Iteration'])
    exts = list(distribution_data['Folder'])

    data_path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\New_Niftii_Arrays\CT'

    for file in os.listdir(data_path):
        if file.find('.nii') == -1:
            continue
        iteration = file.split('_')[-1]
        iteration = iteration.split('.')[0]
        if iteration[0] == 'y':
            iteration = iteration[1:]
        ext = exts[iterations.index(int(iteration))]
        out_path = os.path.join(data_path,ext)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        os.rename(os.path.join(data_path,file),os.path.join(out_path,file))
    return None


if __name__ == '__main__':
    pass
