#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Depends: Qt5

import sys
import glob


sys.path.append("mods")

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QMessageBox

from fsys import ReadBinaryFile
from gui import QButtonLink
from zxcolors import ZXColors, byte_to_pixels
from zxmem import zxscr_lineaddr


class WidgetZXScr(QWidget):

    def __init__(self, initfilename=""):

        super().__init__(None, flags=Qt.Window)

        self.setWindowTitle("ZX Video RAM Viewer")
        self.setFixedSize(680, 520)

        self.gfxview = QGraphicsView()
        self.gfxview.setFixedSize((256*2)+2, (192*2)+2)
        self.zxclrs = ZXColors()

        # Left / Right buttons
        self.widget_btn_left  = QPushButton("<< Prev")
        self.labelfile        = QLabel("filename.scr")
        self.widget_btn_right = QPushButton(">> Next")
        QButtonLink(self.widget_btn_left, self.event_click_left)
        QButtonLink(self.widget_btn_right, self.event_click_right)


        # Files list
        self.fileslist  = glob.glob("scr/*.scr")
        self.filesixd   = 0
        self.arrbin     = bytearray()
        self.filearg    = initfilename
        self.loadpicture()

        # Create widget UI layout
        self.setLayout(self.genlayout())


    def genlayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.gfxview, alignment=Qt.AlignHCenter)
        layout.addLayout(self.genlayout_buttons())
        return layout

    def genlayout_buttons(self) -> QHBoxLayout:
        laybuttons = QHBoxLayout()
        laybuttons.addWidget(self.widget_btn_left)
        laybuttons.addWidget(self.labelfile, alignment=Qt.AlignHCenter)
        laybuttons.addWidget(self.widget_btn_right)
        return laybuttons


    def initFromFile(self, fname):
        self.arrbin = ReadBinaryFile(fname)
        if len(self.arrbin) < 1024:
            buttonReply = QMessageBox.question(
                self, 'File :%s' % fname, "Not valid .scr file",
                QMessageBox.Ok, QMessageBox.Ok)
            exit(1)

    def loadpicture(self):
        fname = self.fileslist[self.filesixd] if not self.filearg else self.filearg
        self.initFromFile(fname)
        self.renderPicture()
        self.widget_btn_left.setEnabled(self.filesixd > 0)
        self.labelfile.setText(fname)
        self.widget_btn_right.setEnabled(self.filesixd < (len(self.fileslist)-1))


    def event_click_left(self):
        if self.filesixd:
            self.filesixd -= 1
        self.loadpicture()


    def event_click_right(self):
        if self.filesixd < (len(self.fileslist)-1):
            self.filesixd += 1
        self.loadpicture()


    def renderPicture(self):

        w, h = 256, 192
        arrsrc = bytearray()

        # render lines
        for j in range(h):
            offs_line = zxscr_lineaddr(j)
            offs_attr = (2048 * 3) + ((j >> 3) * 32)

            for i in range(32):
                b = self.arrbin[offs_line+i]
                a = self.arrbin[offs_attr+i]
                arrsrc.extend(byte_to_pixels(b, a, self.zxclrs))

                # v = 255 if (i & 1) ^ ( j & 1) else 0
                # binarr.append(0)    # B
                # binarr.append(0)    # G
                # binarr.append(v)    # R
                # binarr.append(0)

        img = QImage(arrsrc, w, h, QImage.Format_RGB32)

        pixmap = QPixmap(w, h)
        pixmap.convertFromImage(img, Qt.AutoColor)

        scene = QGraphicsScene()
        scene.addPixmap(pixmap.scaled(w * 2, h * 2))
        self.gfxview.setScene(scene)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    # if len(sys.argv) < 2:
    #     print("\nZX Spectrum Video Memory visualization\nUsage: \tzxscrview [file.scr]\n")
    #     exit(1)

    wdgScrViewer = WidgetZXScr(sys.argv[1] if len(sys.argv) > 1 else "")
    wdgScrViewer.show()
    app.exec()
    exit(0)

