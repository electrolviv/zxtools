def QButtonLink(wdg : "QPushButton", func=None):
    wdg.clicked.connect(func)