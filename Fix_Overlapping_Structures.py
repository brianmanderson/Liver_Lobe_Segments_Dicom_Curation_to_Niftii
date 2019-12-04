__author__ = 'Brian M Anderson'
# Created on 11/26/2019

from Dicom_RT_and_Images_to_Mask.Image_Array_And_Mask_From_Dicom_RT import Dicom_to_Imagestack, os, plot_scroll_Image, np, plt, copy
from Fill_Missing_Segments.Fill_In_Segments_sitk import Fill_Missing_Segments, remove_non_liver


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
Fill_Missing_Segments_Class = Fill_Missing_Segments()
base_path = r'K:\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Images'
MRNs = os.listdir(base_path)
for MRN in MRNs:
    print(MRN)
    for exam in os.listdir(os.path.join(base_path,MRN)):
        print(exam)
        path = os.path.join(base_path,MRN,exam)
        if 'new_RS' in os.listdir(path):
            continue
        Contour_Names = ['Liver'] + ['Liver_Segment_{}'.format(i) for i in range(1,9)]
        Out_Contour_names = ['Liver_Segment_fixed_{}'.format(i) for i in range(1,9)]
        Dicom_Reader = Dicom_to_Imagestack(arg_max=False,Contour_Names=Contour_Names,delete_previous_rois=True)

        Dicom_Reader.Make_Contour_From_directory(path)
        try:
            ground_truth = Dicom_Reader.mask[..., 1]
        except:
            continue
        annotations = Dicom_Reader.mask[..., (0, 2, 3, 4, 5, 6, 7, 8, 9)]
        overlap = np.sum(annotations,axis=-1)
        annotations[overlap>1] = 0
        annotations[ground_truth==0] = 0
        spacing = Dicom_Reader.annotation_handle.GetSpacing()
        re_organized_spacing = spacing[-1::-1]
        previous_iteration = np.zeros(np.argmax(annotations,axis=-1).shape)
        differences = [0,np.inf]
        index = 0
        while np.abs(differences[-1] - differences[-2]) > 50 and index < 15:
            index += 1
            print('Iterating {}'.format(index))
            previous_iteration = copy.deepcopy(np.argmax(annotations,axis=-1))
            annotations = remove_56_78(annotations)
            for i in range(1, annotations.shape[-1]):
                annotations[..., i] = remove_non_liver(annotations[..., i], do_3D=False, do_2D=True,min_area=10,spacing=re_organized_spacing)
            spacing = Dicom_Reader.annotation_handle.GetSpacing()
            annotations = Fill_Missing_Segments_Class.make_distance_map(annotations, ground_truth,spacing=spacing)
            differences.append(np.abs(np.sum(previous_iteration[ground_truth==1]-np.argmax(annotations,axis=-1)[ground_truth==1])))
        Dicom_Reader.with_annotations(annotations,os.path.join(path,'new_RS'),ROI_Names=Out_Contour_names)
xxx = 1

# case.PatientModel.StructureSets['CT 15'].RoiSurfaceToSurfaceDistanceBasedOnDT(ReferenceRoiName='GTV',TargetRoiName='recurrence')
