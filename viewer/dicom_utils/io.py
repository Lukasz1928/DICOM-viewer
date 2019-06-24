import os
from tkinter import filedialog

import pydicom


def read_dicom(path=None):
    if path is None:
        path = filedialog.askopenfilename(initialdir=".", title="Select file",
                                        filetypes=(("DICOM files", "*.dcm"),))
    dcm = None
    if path != '':
        dcm = pydicom.dcmread(path)
    return dcm, path


def list_dicoms_from_dir(path):
    return list(map(lambda name: path + name, filter(lambda file: file.endswith(".dcm"), os.listdir(path))))
