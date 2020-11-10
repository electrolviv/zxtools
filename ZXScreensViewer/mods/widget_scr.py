from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout, QMessageBox, QGraphicsScene

from fsys import ReadBinaryFile
from zxcolors import byte_to_pixels, ZXColors
from zxmem import zxscr_lineaddr


class WidgetScreen(QWidget):

    def __init__(self):
        super(WidgetScreen, self).__init__()
        self.arrbin = bytearray()
        self.gfxview = QGraphicsView()
        self.gfxview.setFixedSize((256*2)+2, (192*2)+2)
        self.zxclrs = ZXColors()
        self.setLayout(self.genlayout())

    def genlayout(self):
        lay = QVBoxLayout()
        lay.addWidget(self.gfxview, alignment=Qt.AlignHCenter)
        return lay

    def loadFile(self, fname) -> bytearray:
        r = ReadBinaryFile(fname)
        if len(r) < 1024:
            QMessageBox.question(
                self, 'File :%s' % fname, "Not valid .scr file",
                QMessageBox.Ok, QMessageBox.Ok)
        return r


    def loadPicture(self, fname):

        self.arrbin = self.loadFile(fname)
        self.renderPicture()


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
