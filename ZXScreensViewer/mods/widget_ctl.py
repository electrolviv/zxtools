import os
from typing import Callable, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout

from gui import QButtonLink


class WidgetCtrl(QWidget):

    def __init__(self, callback : Callable[[Dict], None]):
        super().__init__()

        self.callback = callback

        # Left / Right buttons
        self.widget_btn_left  = QPushButton("<< Prev")
        self.labelfile        = QLabel("filename.scr")
        self.widget_btn_right = QPushButton(">> Next")
        QButtonLink(self.widget_btn_left, self.event_click_left)
        QButtonLink(self.widget_btn_right, self.event_click_right)

        self.setLayout(self.genlayout())


    def genlayout(self) -> QHBoxLayout:
        lay = QHBoxLayout()
        lay.addWidget(self.widget_btn_left)
        lay.addWidget(self.labelfile, alignment=Qt.AlignHCenter)
        lay.addWidget(self.widget_btn_right)
        return lay

    def event_click_left(self):
        self.callback({ 'cmd' : 'left'})

    def event_click_right(self):
        self.callback({ 'cmd' : 'right' })

    def EnableKeyLeft(self, flag : bool):
        self.widget_btn_left.setEnabled(flag)

    def EnableKeyRight(self, flag : bool):
        self.widget_btn_right.setEnabled(flag)

    def SetFileName(self, fname : str):
        self.labelfile.setText(os.path.basename(fname))
