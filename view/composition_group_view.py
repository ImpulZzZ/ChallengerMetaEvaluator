# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'composition_group_view.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_compositionGroupView(object):
    def setupUi(self, compositionGroupView):
        compositionGroupView.setObjectName("compositionGroupView")
        compositionGroupView.resize(1271, 701)
        self.tableWidget = QtWidgets.QTableWidget(compositionGroupView)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 1231, 661))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setIconSize(QtCore.QSize(0, 0))
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.retranslateUi(compositionGroupView)
        QtCore.QMetaObject.connectSlotsByName(compositionGroupView)

    def retranslateUi(self, compositionGroupView):
        _translate = QtCore.QCoreApplication.translate
        compositionGroupView.setWindowTitle(_translate("compositionGroupView", "Compisition View"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    compositionGroupView = QtWidgets.QWidget()
    ui = Ui_compositionGroupView()
    ui.setupUi(compositionGroupView)
    compositionGroupView.show()
    sys.exit(app.exec_())
