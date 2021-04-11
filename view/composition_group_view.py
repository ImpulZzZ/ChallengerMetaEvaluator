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
        compositionGroupView.resize(1222, 525)
        self.tableWidget = QtWidgets.QTableWidget(compositionGroupView)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 1171, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

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
