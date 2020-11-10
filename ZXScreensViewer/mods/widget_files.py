import os
from typing import Dict, Callable

from PyQt5.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QGroupBox, QTreeWidgetItem

from gui import QTreeWidgetLink


class WidgetFiles(QWidget):


    def __init__(self, callback : Callable[[Dict], None]):

        super(WidgetFiles, self).__init__()

        self.callback = callback

        self.gbox = QGroupBox("Files List")

        self.treewdg = QTreeWidget()
        self.treewdg.setMaximumWidth(180)
        QTreeWidgetLink(self.treewdg, self.on_selected)

        self.setLayout(self.genlayout())


    def genlayout(self):

        laygbox = QVBoxLayout()
        laygbox.addWidget(self.treewdg)
        self.gbox.setLayout(laygbox)

        lay = QVBoxLayout()
        lay.addWidget(self.gbox)
        return lay

    def setFilesList(self, arrfiles : []):
        self.treewdg.setColumnCount(1)
        hdrtxt = "%i files found" % len(arrfiles)
        self.treewdg.setHeaderLabel(hdrtxt)
        for file in arrfiles:
            item = QTreeWidgetItem([os.path.basename(file)])
            self.treewdg.addTopLevelItem(item)

    def on_selected(self, item : QTreeWidgetItem):
        idx = self.treewdg.indexOfTopLevelItem(item)  # currentIndex()
        self.callback({ 'fileidx' : idx })  # item.text(0)
