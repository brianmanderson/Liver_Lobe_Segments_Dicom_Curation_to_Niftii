from connect import *
import os, copy


class Change_Patient_Class(object):
    def __init__(self):
        self.patient_db = get_current("PatientDB")
    def ChangePatient(self, MRN):
        info_all = self.patient_db.QueryPatientInfo(Filter={"PatientID": MRN}, UseIndexService=False)
        if not info_all:
            info_all = self.patient_db.QueryPatientInfo(Filter={"PatientID": MRN}, UseIndexService=True)
        for info in info_all:
            if info['PatientID'] == MRN:
                break
        patient = self.patient_db.LoadPatient(PatientInfo=info, AllowPatientUpgrade=True)
        return patient

def import_organ_stl(case, exam, roi_list, import_path):
    rois_in_case = []
    color_list = ['blue','green','yellow','orange','red','pink','teal','brown']
    temp_color_list = []
    for name in case.PatientModel.RegionsOfInterest:
        rois_in_case.append(name.Name)
    if os.path.exists(import_path):
        for roi in roi_list:
            file_path = import_path + '\\' + roi + '.stl'
            print("looking for " + file_path)

            if os.path.isfile(file_path):
                if not temp_color_list:
                    temp_color_list = copy.deepcopy(color_list)
                if roi in rois_in_case:
                    case.PatientModel.RegionsOfInterest[roi].DeleteRoi()
                case.PatientModel.CreateRoi(Name=roi, Color=temp_color_list[0], Type='Organ', TissueName=None,
                                            RbeCellTypeName=None, RoiMaterial=None)
                rois_in_case.append(roi)
                del temp_color_list[0]
                if not case.PatientModel.StructureSets[exam.Name].RoiGeometries[roi].HasContours():
                    case.PatientModel.StructureSets[exam.Name].RoiGeometries[roi].ImportRoiGeometryFromSTL(
                        FileName=file_path,
                        UnitInFile='Millimeter', TransformationMatrix=None)
                else:
                    print("ROI has already a contour, from 'export_organs_as_stl'")
            else:
                print("file does not exist, from 'export_organs_as_stl'")
    else:
        print("path does not exist, from 'export_organs_as_stl'")
    return None

segment_names = ['Liver_Segment_' + str(i) for i in range(1,9)]
segment_names = ['Liver'] + segment_names
new_names = [i + '_BMA_STL' for i in segment_names]
path = r'\\mymdafiles\di_data1\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Images'
pat_class = Change_Patient_Class()
for MRN in os.listdir(path):
    for exam in os.listdir(os.path.join(path,MRN)):
        stl_path = os.path.join(path, MRN, exam, 'stl')
        if os.path.exists(stl_path):
            if os.path.exists(os.path.join(stl_path,'uploaded.txt')):
                continue
            new_names = [i.strip('.stl') for i in os.listdir(stl_path) if i.find('.stl') != -1]
            try:
                patient = pat_class.ChangePatient(MRN)
            except:
                continue
            for case in patient.Cases:
                break
            # case.SetCurrent()
            exam = case.Examinations[exam]
            import_organ_stl(case, exam, new_names, stl_path)
            patient.Save()
            fid = open(os.path.join(stl_path,'uploaded.txt'),'w+')
            fid.close()