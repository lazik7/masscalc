# -*- coding: utf-8 -*-
###################################################################################
#
#  MassCalc.py
#  A calculator utility to calculate needed hole sizes for selected fasteners
#  
#  Copyright Tomasz Kamiński lazik711@gmail.com
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
###################################################################################

from PySide import QtCore, QtGui
import csv


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DockWidget(object):
    def setupUi(self, DockWidget, setRowCount=3, setColumnCount=7):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(267, 136)
        DockWidget.setFloating(True)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))


        self.table = QtGui.QTableWidget()
        self.table.setRowCount(setRowCount)
        self.table.setColumnCount(setColumnCount)

        button_calc = QtGui.QPushButton('calc')
        button_calc.clicked.connect(self.calc)

        button_savecsv = QtGui.QPushButton('Save to CSV')
        button_savecsv.clicked.connect(self.savecsv)

        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.addWidget(self.table)
        self.vLayout.addWidget(button_calc)
        self.vLayout.addWidget(button_savecsv)
        
        
        self.gridLayout.addLayout(self.vLayout, 1, 0, 1, 1)

        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "Mass calculator", None))


    def put_in_table(self, list_name, list_volume):
    
    	#----------------------------------------------------------------------
    
        from materialtools.cardutils import import_materials as getmats
        m, c, i = getmats()
        
        self.dict_mat = {"out of the list":0}
                
        for mat in m.keys():
                try:
                        kgpm3 = m[mat]["Density"].find("kg/m^3")
                        if kgpm3:
                                self.dict_mat[m[mat]["Name"]] = float(m[mat]["Density"][:kgpm3])
	        		
                        gpcm3 = m[mat]["Density"].find("g/cm^3")
                        if gpcm3:
                                self.dict_mat[m[mat]["Name"]] = 1e3*float(m[mat]["Density"][:gpcm3])
                except:
                        pass
	        	
	#----------------------------------------------------------------------

        volume_sum = 0
        for i in list_volume:
            volume_sum += i

        self.n = len(list_volume)
        
        self.table.setItem(0, 0, QtGui.QTableWidgetItem("Oject name"))
        self.table.setRowCount(self.n+2)
        self.table.setItem(0, 1, QtGui.QTableWidgetItem("V[mm3]"))
        self.table.setItem(0, 2, QtGui.QTableWidgetItem("V[m3]"))
        self.table.setItem(0, 3, QtGui.QTableWidgetItem("q[kg/m3]"))
        self.table.setItem(0, 4, QtGui.QTableWidgetItem("m[kg]"))
        self.table.setItem(0, 5, QtGui.QTableWidgetItem("m[g]"))

        
        self.list_combox = []

        for i in range(0, self.n):
                self.table.setItem(i+1, 0, QtGui.QTableWidgetItem(list_name[i]))
                self.table.setItem(i+1, 1, QtGui.QTableWidgetItem("%.3f" % list_volume[i]))
                self.table.setItem(i+1, 2, QtGui.QTableWidgetItem("%.3f" % (list_volume[i]*1e-9)))
                
                self.list_combox.append( QtGui.QComboBox() )
                self.list_combox[i].addItems( list(self.dict_mat.keys()) )
                self.table.setCellWidget(i+1, 6, self.list_combox[i])
                

        self.table.setItem(self.n+1, 0, QtGui.QTableWidgetItem("sum"))
        self.table.setItem(self.n+1, 1, QtGui.QTableWidgetItem("%.3f" % volume_sum))
        self.table.setItem(self.n+1, 2, QtGui.QTableWidgetItem("%.3f" % (volume_sum*1e-9)))
        
        

        
        
        

        
    def calc(self):

        self.data = []
        self.data.append(["Oject name","V[mm3]","V[m3]","q[kg/m3]","m[kg]","m[g]"])

        m_sum = 0 # kg
        volume_sum = 0 # m3
        
        for i in range(0, self.n):
        
                q = self.dict_mat[self.list_combox[i].currentText()]
                if q!=0:
                	self.table.setItem(i+1, 3, QtGui.QTableWidgetItem("%.2f" % q))
        
                name = self.table.item(i+1, 0).text()
                V = float(self.table.item(i+1, 1).text())*1e-9 # mm3 to m3
                volume_sum = volume_sum + V
                q = float( self.table.item(i+1, 3).text() ) # kg/m3
                m = q*V # kg
                m_sum = m_sum + m
                self.table.setItem(i+1,4, QtGui.QTableWidgetItem("%.3f" % (m)))
                self.table.setItem(i+1,5, QtGui.QTableWidgetItem("%.3f" % (m*1e3)))

                self.data.append([name, V*1e9, V, q, m, m*1e3])

        self.table.setItem(self.n+1, 4, QtGui.QTableWidgetItem("%.3f" % (m_sum)))
        self.table.setItem(self.n+1, 5, QtGui.QTableWidgetItem("%.3f" % (m_sum*1e3)))
        self.data.append(["sum","%.3f" % (volume_sum*1e9),"%.3f" % volume_sum," ", "%.3f" % (m_sum),"%.3f" % (m_sum*1e3)])


  
        
    def savecsv(self):

        if self.data:
                fname = QtGui.QFileDialog.getSaveFileName(None, 'Save file', '.',"pliki csv(*.csv)")[0]

                with open(fname,"w") as csvfile:
                        s = csv.writer(csvfile)
                        s.writerows(self.data)

        
        ###################################################################################
        # End position for generated code from pyuic4
        ###################################################################################

    
    
from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD, FreeCADGui, Part, os, math
__dir__ = os.path.dirname(__file__)
iconPath = os.path.join( __dir__, 'Icons' )



       
dlg = QtGui.QDockWidget()
dlg.ui = Ui_DockWidget()
dlg.ui.setupUi(dlg)
Gui.getMainWindow().addDockWidget(QtCore.Qt.RightDockWidgetArea, dlg)
dlg.setFloating(True)
dlg.hide()
   

class Mass:
  """Display a calculator for needed screw holes"""

  def GetResources(self):
    FreeCAD.Console.PrintLog("Getting resources\n")
    icon = os.path.join( iconPath , 'Mass.png')
    return {'Pixmap'  : icon , # the name of a svg file available in the resources
            'MenuText': "Mass calculator" ,
            'Accel' : "Shift+M",
            'ToolTip' : "Calc mass"}
 
  def Activated(self):
    if dlg.isHidden():
      dlg.show()
    else:
      dlg.hide()

    list_name = []
    list_volume = []

    for i,j in zip(Gui.Selection.getSelection(), Gui.Selection.getSelectionEx()):
        try:
            list_volume.append( j.Object.Shape.Volume )
            list_name.append( i.Label )
        except:
            QtGui.QMessageBox.information(QtGui.QWidget(), "Message", "err Object: %s" % i.Label)

    dlg.ui.put_in_table(list_name, list_volume)
    
      
    return
   
  def IsActive(self):
    return True


