__author__ = 'Brian M Anderson'
# Created on 11/26/2019

from Dicom_RT_and_Images_to_Mask.Image_Array_And_Mask_From_Dicom_RT import Dicom_to_Imagestack, os, plot_scroll_Image, np, plt, copy
from Fill_Missing_Segments.Fill_In_Segments_sitk import Fill_Missing_Segments, remove_non_liver
import SimpleITK as sitk
import pandas as pd


def remove_56_78(annotations):
    amounts = np.sum(annotations, axis=(1, 2))
    indexes = np.where((np.max(amounts[:, (5, 6)], axis=-1) > 0) & (np.max(amounts[:, (7, 8)], axis=-1) > 0))
    if indexes:
        indexes = indexes[0]
        for i in indexes:
            if amounts[i, 5] < amounts[i, 8]:
                annotations[i, ..., 5] = 0
            else:
                annotations[i, ..., 8] = 0
            if amounts[i, 6] < amounts[i, 7]:
                annotations[i, ..., 6] = 0
            else:
                annotations[i, ..., 7] = 0
    return annotations


def write_csv(csv_path,dictionary):
    fid = open(csv_path,'w+')
    fid.write('MRN,Exam,Iteration\n')
    for MRN in dictionary.keys():
        for exam in dictionary[MRN]:
            iteration = dictionary[MRN][exam]
            fid.write('{},{},{}\n'.format(MRN,exam,iteration))
    fid.close()
    return None


class Fix_Missing_Segments_Class(object):
    def __init__(self):
        self.Fill_Missing_Segments_Class = Fill_Missing_Segments()
        self.Contour_Names = ['Liver'] + ['Liver_Segment_{}'.format(i) for i in range(1,9)]
        self.Out_Contour_names = ['Liver_Segment_fixed_{}'.format(i) for i in range(1,9)]
        self.Dicom_Reader = Dicom_to_Imagestack(arg_max=False,Contour_Names=self.Contour_Names,delete_previous_rois=True)

    def run_on_path(self, path):
        self.path = path
        self.Dicom_Reader.Make_Contour_From_directory(self.path)

    def write_output_as_RT(self, annotations=None):
        if annotations is None:
            annotations = self.final_annotations
        self.Dicom_Reader.with_annotations(annotations,os.path.join(self.path,'new_RS'),ROI_Names=self.Out_Contour_names)

    def iterate_mask(self):
        try:
            ground_truth = self.Dicom_Reader.mask[..., 1]
        except:
            return None
        annotations = self.Dicom_Reader.mask[..., (0, 2, 3, 4, 5, 6, 7, 8, 9)]
        overlap = np.sum(annotations,axis=-1)
        annotations[overlap>1] = 0
        self.final_annotations = self.Fill_Missing_Segments_Class.iterate_annotations(annotations,ground_truth,
                                                                                      spacing=self.Dicom_Reader.annotation_handle.GetSpacing())
        # annotations[ground_truth==0] = 0
        # spacing = self.Dicom_Reader.annotation_handle.GetSpacing()
        # re_organized_spacing = spacing[-1::-1]
        # differences = [0,np.inf]
        # index = 0
        # while np.abs(differences[-1] - differences[-2]) > 50 and index < 15:
        #     index += 1
        #     print('Iterating {}'.format(index))
        #     previous_iteration = copy.deepcopy(np.argmax(annotations,axis=-1))
        #     annotations = remove_56_78(annotations)
        #     for i in range(1, annotations.shape[-1]):
        #         annotations[..., i] = remove_non_liver(annotations[..., i], do_3D=False, do_2D=True,min_area=10,spacing=re_organized_spacing)
        #     spacing = self.Dicom_Reader.annotation_handle.GetSpacing()
        #     annotations = self.Fill_Missing_Segments_Class.make_distance_map(annotations, ground_truth,spacing=spacing)
        #     differences.append(np.abs(np.sum(previous_iteration[ground_truth==1]-np.argmax(annotations,axis=-1)[ground_truth==1])))
        # self.final_annotations = annotations

    def write_output_as_nifti(self, out_path, images_desc, iteration):
        new_annotations = sitk.GetImageFromArray(np.argmax(self.final_annotations, axis=-1).astype('int8'))
        new_annotations.SetSpacing(self.Dicom_Reader.dicom_handle.GetSpacing())
        new_annotations.SetOrigin(self.Dicom_Reader.dicom_handle.GetOrigin())
        new_annotations.SetDirection(self.Dicom_Reader.dicom_handle.GetDirection())
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        image_path = os.path.join(out_path,'Overall_Data_' + images_desc + '_' + str(iteration) + '.nii.gz')
        sitk.WriteImage(self.Dicom_Reader.dicom_handle, image_path)
        annotation_path = os.path.join(out_path,
                                       'Overall_mask_' + images_desc + '_y' + str(iteration) + '.nii.gz')
        sitk.WriteImage(new_annotations, annotation_path)


def turn_pandas_into_dictionary(pandas_file):
    out_dict = {}
    for i in range(len(pandas_file.columns)):
        header_name = pandas_file.columns[i]
        out_dict[header_name] = list(pandas_file[header_name])
    return out_dict

def Fill_Segments(base_path, data_path, images_desc, excel_file_path, write_data=False):
    Fill_Missing_Segments_Class = Fix_Missing_Segments_Class()
    excel_file = pd.read_excel(excel_file_path)
    excel_file = turn_pandas_into_dictionary(excel_file)
    add = 'CT'
    MRNs = os.listdir(base_path)
    for MRN in MRNs:
        print(MRN)
        for exam in os.listdir(os.path.join(base_path,MRN)):
            print(exam)
            path = os.path.join(base_path,MRN,exam)
            text_files = [i for i in os.listdir(path) if i.find('Iteration') != -1]
            if text_files:
                iteration = int(text_files[0].split('Iteration_')[-1][:-4])
            elif int(MRN) in excel_file['MRN']:
                indexes = np.where(np.asarray(excel_file['MRN'])==int(MRN))[0]
                for index in indexes:
                    if excel_file['Exam'][index] == exam:
                        iteration = excel_file['Iteration'][index]
                        break
            else:
                iteration = excel_file['Iteration'][-1]+1
                excel_file['MRN'].append(int(MRN))
                excel_file['Exam'].append(exam)
                excel_file['Iteration'].append(iteration)
                excel_file['Folder'].append('')
                excel_file['Comments'].append(np.nan)
            iteration_index = excel_file['Iteration'].index(iteration)
            folder = excel_file['Folder'][iteration_index]
            if folder == 'Deleted':
                continue
            write_out_path = os.path.join(data_path, add)
            if folder in ['Train','Test','Validation']:
                write_out_path = os.path.join(write_out_path, folder)
                image_path = os.path.join(write_out_path,
                                          'Overall_Data_' + images_desc + '_' + str(iteration) + '.nii.gz')
            else:
                image_path = os.path.join(write_out_path,
                                          'Overall_Data_' + images_desc + '_' + str(iteration) + '.nii.gz')
            if os.path.exists(image_path):
                continue
            Fill_Missing_Segments_Class.run_on_path(path)
            Fill_Missing_Segments_Class.iterate_mask()
            Fill_Missing_Segments_Class.write_output_as_RT()
            if 'new_RS' in os.listdir(path): # Created the RT, time to write it out
                Fill_Missing_Segments_Class.write_output_as_nifti(write_out_path,images_desc,iteration)
                df = pd.DataFrame(excel_file)
                df.to_excel(excel_file_path,index=False)


if __name__ == '__main__':
    pass
