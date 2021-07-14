# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from BuilderMain import BuilderMain
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(933, 671)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 400, 75, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(10, 350, 91, 16))
        self.label_15.setObjectName("label_15")
        self.OutputLocation = QtWidgets.QLineEdit(self.centralwidget)
        self.OutputLocation.setGeometry(QtCore.QRect(10, 370, 291, 20))
        self.OutputLocation.setObjectName("OutputLocation")
        self.ProgressOutput = QtWidgets.QLineEdit(self.centralwidget)
        self.ProgressOutput.setGeometry(QtCore.QRect(100, 400, 221, 31))
        self.ProgressOutput.setObjectName("ProgressOutput")
        self.OutputLocButton = QtWidgets.QToolButton(self.centralwidget)
        self.OutputLocButton.setGeometry(QtCore.QRect(310, 370, 25, 19))
        self.OutputLocButton.setObjectName("OutputLocButton")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 301, 311))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.Parameters = QtWidgets.QLineEdit(self.widget)
        self.Parameters.setObjectName("Parameters")
        self.verticalLayout.addWidget(self.Parameters)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.LayoutCoordinates = QtWidgets.QLineEdit(self.widget)
        self.LayoutCoordinates.setObjectName("LayoutCoordinates")
        self.verticalLayout.addWidget(self.LayoutCoordinates)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Plant = QtWidgets.QLineEdit(self.widget)
        self.Plant.setObjectName("Plant")
        self.verticalLayout.addWidget(self.Plant)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.LandConstants = QtWidgets.QLineEdit(self.widget)
        self.LandConstants.setObjectName("LandConstants")
        self.verticalLayout.addWidget(self.LandConstants)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.LandSedDelivCoeff = QtWidgets.QLineEdit(self.widget)
        self.LandSedDelivCoeff.setObjectName("LandSedDelivCoeff")
        self.verticalLayout.addWidget(self.LandSedDelivCoeff)
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.Soil = QtWidgets.QLineEdit(self.widget)
        self.Soil.setObjectName("Soil")
        self.verticalLayout.addWidget(self.Soil)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.Lakes = QtWidgets.QLineEdit(self.widget)
        self.Lakes.setObjectName("Lakes")
        self.verticalLayout.addWidget(self.Lakes)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(320, 10, 27, 331))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ParametersButton = QtWidgets.QToolButton(self.widget1)
        self.ParametersButton.setObjectName("ParametersButton")
        self.verticalLayout_2.addWidget(self.ParametersButton)
        self.LayoutCoordinatesButton_3 = QtWidgets.QToolButton(self.widget1)
        self.LayoutCoordinatesButton_3.setObjectName("LayoutCoordinatesButton_3")
        self.verticalLayout_2.addWidget(self.LayoutCoordinatesButton_3)
        self.PlantButton_5 = QtWidgets.QToolButton(self.widget1)
        self.PlantButton_5.setObjectName("PlantButton_5")
        self.verticalLayout_2.addWidget(self.PlantButton_5)
        self.LandConstantsButton_7 = QtWidgets.QToolButton(self.widget1)
        self.LandConstantsButton_7.setObjectName("LandConstantsButton_7")
        self.verticalLayout_2.addWidget(self.LandConstantsButton_7)
        self.LandSedDelivCoeffButton_9 = QtWidgets.QToolButton(self.widget1)
        self.LandSedDelivCoeffButton_9.setObjectName("LandSedDelivCoeffButton_9")
        self.verticalLayout_2.addWidget(self.LandSedDelivCoeffButton_9)
        self.SoilButton_11 = QtWidgets.QToolButton(self.widget1)
        self.SoilButton_11.setObjectName("SoilButton_11")
        self.verticalLayout_2.addWidget(self.SoilButton_11)
        self.LakesButton_13 = QtWidgets.QToolButton(self.widget1)
        self.LakesButton_13.setObjectName("LakesButton_13")
        self.verticalLayout_2.addWidget(self.LakesButton_13)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(370, 10, 321, 311))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.LayoutParcel = QtWidgets.QLineEdit(self.widget2)
        self.LayoutParcel.setObjectName("LayoutParcel")
        self.verticalLayout_3.addWidget(self.LayoutParcel)
        self.label_5 = QtWidgets.QLabel(self.widget2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.LayoutEmissSources = QtWidgets.QLineEdit(self.widget2)
        self.LayoutEmissSources.setObjectName("LayoutEmissSources")
        self.verticalLayout_3.addWidget(self.LayoutEmissSources)
        self.label_6 = QtWidgets.QLabel(self.widget2)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.USLECalc = QtWidgets.QLineEdit(self.widget2)
        self.USLECalc.setObjectName("USLECalc")
        self.verticalLayout_3.addWidget(self.USLECalc)
        self.label_8 = QtWidgets.QLabel(self.widget2)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.LandErosionPara = QtWidgets.QLineEdit(self.widget2)
        self.LandErosionPara.setObjectName("LandErosionPara")
        self.verticalLayout_3.addWidget(self.LandErosionPara)
        self.label_10 = QtWidgets.QLabel(self.widget2)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        self.LandSedDeliv = QtWidgets.QLineEdit(self.widget2)
        self.LandSedDeliv.setObjectName("LandSedDeliv")
        self.verticalLayout_3.addWidget(self.LandSedDeliv)
        self.label_12 = QtWidgets.QLabel(self.widget2)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.Watersheds = QtWidgets.QLineEdit(self.widget2)
        self.Watersheds.setObjectName("Watersheds")
        self.verticalLayout_3.addWidget(self.Watersheds)
        self.label_14 = QtWidgets.QLabel(self.widget2)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_3.addWidget(self.label_14)
        self.Fish = QtWidgets.QLineEdit(self.widget2)
        self.Fish.setObjectName("Fish")
        self.verticalLayout_3.addWidget(self.Fish)
        self.widget3 = QtWidgets.QWidget(self.centralwidget)
        self.widget3.setGeometry(QtCore.QRect(710, 10, 27, 331))
        self.widget3.setObjectName("widget3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.LayoutParcelButton_2 = QtWidgets.QToolButton(self.widget3)
        self.LayoutParcelButton_2.setObjectName("LayoutParcelButton_2")
        self.verticalLayout_4.addWidget(self.LayoutParcelButton_2)
        self.LayoutEmisSourcesButton_4 = QtWidgets.QToolButton(self.widget3)
        self.LayoutEmisSourcesButton_4.setObjectName("LayoutEmisSourcesButton_4")
        self.verticalLayout_4.addWidget(self.LayoutEmisSourcesButton_4)
        self.USLECalcButton_6 = QtWidgets.QToolButton(self.widget3)
        self.USLECalcButton_6.setObjectName("USLECalcButton_6")
        self.verticalLayout_4.addWidget(self.USLECalcButton_6)
        self.LandErosionParaButton_8 = QtWidgets.QToolButton(self.widget3)
        self.LandErosionParaButton_8.setObjectName("LandErosionParaButton_8")
        self.verticalLayout_4.addWidget(self.LandErosionParaButton_8)
        self.LandSedDelivButton_10 = QtWidgets.QToolButton(self.widget3)
        self.LandSedDelivButton_10.setObjectName("LandSedDelivButton_10")
        self.verticalLayout_4.addWidget(self.LandSedDelivButton_10)
        self.WatershedsButton_12 = QtWidgets.QToolButton(self.widget3)
        self.WatershedsButton_12.setObjectName("WatershedsButton_12")
        self.verticalLayout_4.addWidget(self.WatershedsButton_12)
        self.FishButton_14 = QtWidgets.QToolButton(self.widget3)
        self.FishButton_14.setObjectName("FishButton_14")
        self.verticalLayout_4.addWidget(self.FishButton_14)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 933, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        
        #connect slots/callbacks and signals
        self.ParametersButton.clicked.connect(self.onParameterButtonClicked)
        self.LayoutCoordinatesButton_3.clicked.connect(self.onLayoutCoordinatesButtonClicked)
        self.PlantButton_5.clicked.connect(self.onPlantButton_5)
        self.LandConstantsButton_7.clicked.connect(self.onLandConstantsButton_7)
        self.LandSedDelivCoeffButton_9.clicked.connect(self.onLandSedDelivCoeffButton_9)
        self.SoilButton_11.clicked.connect(self.onSoilButton_11)
        self.LakesButton_13.clicked.connect(self.onLakesButton_13)
        self.LayoutParcelButton_2.clicked.connect(self.onLayoutParcelButton_2)
        self.LayoutEmisSourcesButton_4.clicked.connect(self.onLayoutEmisSourcesButton_4)
        self.USLECalcButton_6.clicked.connect(self.onUSLECalcButton_6)
        self.LandErosionParaButton_8.clicked.connect(self.onLandErosionParaButton_8)
        self.LandSedDelivButton_10.clicked.connect(self.onLandSedDelivButton_10)
        self.WatershedsButton_12.clicked.connect(self.onWatershedsButton_12)
        self.FishButton_14.clicked.connect(self.onFishButton_14)
        
        self.OutputLocButton.clicked.connect(self.onOutputLocButton)
    

        self.pushButton.clicked.connect(self.onPushButtonclicked)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Create Files"))
        self.label_15.setText(_translate("MainWindow", "Output Location"))
        self.OutputLocButton.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "Parameters"))
        self.label_4.setText(_translate("MainWindow", "Layout Coordinates"))
        self.label.setText(_translate("MainWindow", "Plant"))
        self.label_7.setText(_translate("MainWindow", "Land Constants"))
        self.label_9.setText(_translate("MainWindow", "Land SedDelivCoeff"))
        self.label_11.setText(_translate("MainWindow", "Soil"))
        self.label_13.setText(_translate("MainWindow", "Lakes"))
        self.ParametersButton.setText(_translate("MainWindow", "..."))
        self.LayoutCoordinatesButton_3.setText(_translate("MainWindow", "..."))
        self.PlantButton_5.setText(_translate("MainWindow", "..."))
        self.LandConstantsButton_7.setText(_translate("MainWindow", "..."))
        self.LandSedDelivCoeffButton_9.setText(_translate("MainWindow", "..."))
        self.SoilButton_11.setText(_translate("MainWindow", "..."))
        self.LakesButton_13.setText(_translate("MainWindow", "..."))
        self.label_3.setText(_translate("MainWindow", "Layout Parcel"))
        self.label_5.setText(_translate("MainWindow", "Layout Emission Sources"))
        self.label_6.setText(_translate("MainWindow", "USLE Calcs"))
        self.label_8.setText(_translate("MainWindow", "Land Erosion Parameters"))
        self.label_10.setText(_translate("MainWindow", "Land SedDeliv"))
        self.label_12.setText(_translate("MainWindow", "Watersheds"))
        self.label_14.setText(_translate("MainWindow", "Fish"))
        self.LayoutParcelButton_2.setText(_translate("MainWindow", "..."))
        self.LayoutEmisSourcesButton_4.setText(_translate("MainWindow", "..."))
        self.USLECalcButton_6.setText(_translate("MainWindow", "..."))
        self.LandErosionParaButton_8.setText(_translate("MainWindow", "..."))
        self.LandSedDelivButton_10.setText(_translate("MainWindow", "..."))
        self.WatershedsButton_12.setText(_translate("MainWindow", "..."))
        self.FishButton_14.setText(_translate("MainWindow", "..."))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionOpen.setText(_translate("MainWindow", "Quit"))


    #defs
    def onParameterButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.Parameters.setText(filename)
            #print(self.Parameters.text())

    def onLayoutCoordinatesButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.LayoutCoordinates.setText(filename)

    def onPlantButton_5(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.Plant.setText(filename)
        
    def onLandConstantsButton_7(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.LandConstants.setText(filename)
               
    def onLandSedDelivCoeffButton_9(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.LandSedDelivCoeff.setText(filename)
               
    def onSoilButton_11(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.Soil.setText(filename)
               
    def onLakesButton_13(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.Lakes.setText(filename)
               
    def onLayoutParcelButton_2(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.LayoutParcel.setText(filename)
               
    def onLayoutEmisSourcesButton_4(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.LayoutEmissSources.setText(filename)
               
    def onUSLECalcButton_6(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.USLECalc.setText(filename)       
        
    def onLandErosionParaButton_8(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.LandErosionPara.setText(filename)
               
    def onLandSedDelivButton_10(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.LandSedDeliv.setText(filename)
               
    def onWatershedsButton_12(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.Watersheds.setText(filename)
               
    def onFishButton_14(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)")
        
        if filename:
            self.Fish.setText(filename)       
        
    def onOutputLocButton(self):      
        self.OutputLocation.setText("C:/Users/39492/Desktop/pyBuilderOutput/")


#==========================
    def onPushButtonclicked(self):
        #self.ProgressOutput.setText("Generating files ...")
        BuilderMain(self.Parameters.text(), 
                    self.LayoutParcel.text(), 
                    self.LayoutCoordinates.text(), 
                    self.LayoutEmissSources.text(), 
                    self.Plant.text(),
                    self.USLECalc.text(),
                    self.LandConstants.text(),
                    self.LandErosionPara.text(),
                    self.LandSedDelivCoeff.text(),
                    self.LandSedDeliv.text(),
                    self.Soil.text(),
                    self.Watersheds.text(),
                    self.Lakes.text(),
                    self.Fish.text(),
                    self.OutputLocation.text())        
        self.ProgressOutput.setText("Done.")
        #pass












if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

