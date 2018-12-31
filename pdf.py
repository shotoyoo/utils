#!python3
# -*- coding:utf-8 -*-

from PyPDF2 import PdfFileMerger
import pyperclip
import glob
import glob
import os

if __name__=="__main__":
    folder = pyperclip.paste()
    # p = pathlib.Path(folder)
    filelist = glob.glob(os.path.join(folder, "*.pdf"))

    merger = PdfFileMerger()

    for file in filelist:
        merger.append(file)

    merger.write(os.path.join(folder, 'merged.pdf'))
    merger.close()