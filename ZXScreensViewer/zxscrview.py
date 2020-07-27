#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Depends: Qt5

import sys
import os
import glob

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QMessageBox
from PyQt5 import QtWidgets


def ReadBinaryFile(fname):
    r = bytearray()
    if os.path.isfile(fname):
        with open(fname, "rb") as binaryfile:
            r = bytearray(binaryfile.read())
    return r


class ZXColors:

    def __init__(self):

        r = []
        h, f = 0xD7, 0xFF

        r.append(bytearray([0, 0, 0, 0]))
        r.append(bytearray([h, 0, 0, 0]))
        r.append(bytearray([0, 0, h, 0]))
        r.append(bytearray([h, 0, h, 0]))
        r.append(bytearray([0, h, 0, 0]))
        r.append(bytearray([h, h, 0, 0]))
        r.append(bytearray([0, h, h, 0]))
        r.append(bytearray([h, h, h, 0]))

        r.append(bytearray([0, 0, 0, 0]))
        r.append(bytearray([f, 0, 0, 0]))
        r.append(bytearray([0, 0, f, 0]))
        r.append(bytearray([f, 0, f, 0]))
        r.append(bytearray([0, f, 0, 0]))
        r.append(bytearray([f, f, 0, 0]))
        r.append(bytearray([0, f, f, 0]))
        r.append(bytearray([f, f, f, 0]))

        self.colors = r

    def getcolor(self, idx):
        return self.colors[idx]


def zxscr_lineaddr(linen):

    n = linen >> 6
    linen &= 0x3F
    d = linen % 8
    addr = (n * 2048) + ((linen >> 3) * 32) + (d * 8 * 32)

    return addr


def QButtonLink(wdg : "QPushButton", func=None):
    wdg.clicked.connect(func)


class GFXolon(QtWidgets.QMainWindow):

    def __init__(self, initfilename=""):

        super().__init__(None, flags=Qt.Window)
        self.setWindowTitle("ZX Video RAM Viewer")
        self.setFixedSize(680, 520)

        self.show()

        self.gfxview = QGraphicsView()
        self.gfxview.setFixedSize((256*2)+2, (192*2)+2)

        layout = QVBoxLayout()
        layout.addWidget(self.gfxview, alignment=Qt.AlignHCenter)
        self.wdg_central = QWidget(self)
        self.wdg_central.setLayout(layout)
        self.setCentralWidget(self.wdg_central)

        laybuttons = QHBoxLayout()

        self.widget_btn_left  = QPushButton("<< Prev")
        self.labelfile        = QLabel("filename.scr")
        self.widget_btn_right = QPushButton(">> Next")

        QButtonLink(self.widget_btn_left,  self.event_click_left)
        QButtonLink(self.widget_btn_right, self.event_click_right)

        laybuttons.addWidget(self.widget_btn_left)
        laybuttons.addWidget(self.labelfile, alignment=Qt.AlignHCenter)
        laybuttons.addWidget(self.widget_btn_right)
        layout.addLayout(laybuttons)

        self.zxclrs = ZXColors()

        # Files list
        self.fileslist  = glob.glob("scr/*.scr")
        self.filesixd   = 0
        self.arrbin     = bytearray()
        self.filearg    = initfilename

        self.loadpicture()


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
        self.render()
        self.widget_btn_left.setEnabled(self.filesixd > 0)
        self.labelfile.setText(fname)
        self.widget_btn_right.setEnabled(self.filesixd < (len(self.fileslist)-1))



    def byte_to_pixels(self, b, attr):
        r = bytearray()
        mask = 0x80

        hattr = 8 if (attr >> 6) & 1 else 0
        idx1 = hattr + (attr & 7)
        idx2 = hattr + ((attr >> 3) & 7)

        c1 = self.zxclrs.getcolor(idx1)
        c2 = self.zxclrs.getcolor(idx2)

        for i in range(8):
            r.extend(c1 if b & mask else c2)
            mask >>= 1
        return r


    def event_click_left(self):
        if self.filesixd:
            self.filesixd -= 1
        self.loadpicture()


    def event_click_right(self):
        if self.filesixd < (len(self.fileslist)-1):
            self.filesixd += 1
        self.loadpicture()


    def render(self):

        w, h = 256, 192
        arrsrc = bytearray()

        # render lines
        for j in range(h):
            offs_line = zxscr_lineaddr(j)
            offs_attr = (2048 * 3) + ((j>>3) * 32)

            for i in range(32):
                b = self.arrbin[offs_line+i]
                a = self.arrbin[offs_attr+i]
                arrsrc.extend(self.byte_to_pixels(b, a))

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



if __name__ != '__main__':
    exit(0)

app = QApplication(sys.argv)
wdgMainForm = GFXolon(sys.argv[1] if len(sys.argv) > 1 else "")
app.exec()

# if len(sys.argv) < 2:
#     print("\nZX Spectrum Video Memory visualization\nUsage: \tzxscrview [file.scr]\n")
#     exit(1)
