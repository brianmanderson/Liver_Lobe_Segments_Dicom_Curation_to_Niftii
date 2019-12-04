__author__ = 'Brian M Anderson'
# Created on 11/26/2019

from connect import *
import os

case = get_current("Case")
exam = get_current("Examination")
patient = get_current("Patient")
patient.Save()
path = r'\\mymdafiles\di_data1\Morfeus\BMAnderson\CNN\Data\Data_Liver\Liver_Segments\Images'
export_path = os.path.join(path,patient.PatientID,exam.Name)
case.ScriptableDicomExport(ExportFolderPath=export_path, Examinations=[],
                           RtStructureSetsForExaminations=[exam.Name])