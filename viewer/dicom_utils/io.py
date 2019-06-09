from tkinter import filedialog

import pydicom


def read_dicom():
    path = filedialog.askopenfilename(initialdir=".", title="Select file",
                                      filetypes=(("DICOM files", "*.dcm"),))
    dcm = None
    if path != '':
        dcm = pydicom.dcmread(path)
    return dcm, path
