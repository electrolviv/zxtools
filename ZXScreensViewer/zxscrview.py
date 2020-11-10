#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Depends: Qt5

import sys
import glob
from typing import Dict

sys.path.append("mods")

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QMessageBox

from widget_scr import WidgetScreen
from widget_ctl import WidgetCtrl
from widget_files import WidgetFiles

from fsys import ReadBinaryFile
from gui import QButtonLink
from zxcolors import ZXColors, byte_to_pixels
from zxmem import zxscr_lineaddr


class WidgetZXScr(QWidget):

    def __init__(self, initfilename=""):

        super().__init__(None, flags=Qt.Window)

        self.setWindowTitle("ZX Video RAM Viewer")
        # self.setFixedSize(680, 520)

        self.wdgScr  = WidgetScreen()
        self.wdgCtrl = WidgetCtrl(self.on_ctrl)
        self.wdgFilesList = WidgetFiles(self.on_fileselect)

        # Files list
        self.fileslist  = glob.glob("scr/*.scr")
        self.filesixd   = 0
        self.filearg    = initfilename

        self.wdgFilesList.setFilesList(self.fileslist)

        self.reload()

        # Create widget UI layout
        self.setLayout(self.genlayout())


    def genlayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.wdgScr)
        layout.addWidget(self.wdgCtrl)

        lay = QHBoxLayout()
        lay.addLayout(layout)
        lay.addWidget(self.wdgFilesList)
        return lay


    def reload(self):
        fname = self.fileslist[self.filesixd] if not self.filearg else self.filearg
        self.wdgScr.loadPicture(fname)

        self.wdgCtrl.EnableKeyLeft(self.filesixd > 0)
        self.wdgCtrl.SetFileName(fname)
        self.wdgCtrl.EnableKeyRight(self.filesixd < (len(self.fileslist)-1))



    def on_ctrl(self, jcmd : Dict) -> None:
        if jcmd['cmd'] == 'left':
            if self.filesixd:
                self.filesixd -= 1
            self.reload()
        elif jcmd['cmd'] == 'right':
            if self.filesixd < (len(self.fileslist)-1):
                self.filesixd += 1
            self.reload()

    def on_fileselect(self, jcmd : Dict) -> None:
        self.filesixd = jcmd['fileidx']
        self.reload()



if __name__ == '__main__':

    app = QApplication(sys.argv)

    # if len(sys.argv) < 2:
    #     print("\nZX Spectrum Video Memory visualization\nUsage: \tzxscrview [file.scr]\n")
    #     exit(1)

    wdgScrViewer = WidgetZXScr(sys.argv[1] if len(sys.argv) > 1 else "")
    wdgScrViewer.show()
    app.exec()
    exit(0)

