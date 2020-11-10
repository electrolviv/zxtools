from PyQt5.QtWidgets import QPushButton, QTreeWidget


def QButtonLink(wdg : QPushButton, func=None):
    wdg.clicked.connect(func)


def QTreeWidgetLink(wdg : QTreeWidget, func=None):
    wdg.itemClicked.connect(func)
