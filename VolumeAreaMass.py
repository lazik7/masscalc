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


from FreeCAD import Gui

class VolumeAreaMass():
    """My new command"""
    
    from os.path import join, dirname
    import my_mod_locator
    mymod_icons_path =  join( dirname(my_mod_locator.__file__), 'Icons')
    Icon = join( mymod_icons_path , 'VolumeAreaMass.png')
    
    def GetResources(self):
        return {'Pixmap'  : self.Icon, # the name of a svg file available in the resources
                'Accel' : "Shift+A", # a default shortcut (optional)
                'MenuText': "VolumeAreaMass",
                'ToolTip' : "Calc Volume, Area, Mass"}

    def Activated(self):
        "Do something here"
        
        from PySide import QtGui
        #import FreeCAD
        
        from materialtools.cardutils import import_materials as getmats
        m, c, i = getmats()
        
        dict_mat = {"out of the list":0}
                
        for mat in m.keys():
        	try:
        		kgpm3 = m[mat]["Density"].find("kg/m^3")
        		if kgpm3:
	        		dict_mat[m[mat]["Name"]] = float(m[mat]["Density"][:kgpm3])
	        		
	        	gpcm3 = m[mat]["Density"].find("g/cm^3")
        		if gpcm3:
	        		dict_mat[m[mat]["Name"]] = 1e3*float(m[mat]["Density"][:gpcm3])
	        except:
	        	pass


        volume = Gui.Selection.getSelectionEx()[0].Object.Shape.Volume
        A = Gui.Selection.getSelectionEx()[0].Object.Shape.Area
        
        q = dict_mat[QtGui.QInputDialog.getItem(None, "choose the material", "density, kg/m3 = ", list(dict_mat.keys()) )[0]]

        if q==0:
        	q = float(str(QtGui.QInputDialog.getText(None, "Get text", "density, kg/m3 = ")[0]))

        volume = volume * 1e-9 # mm3 -> m3
        #print( "Volume, m3 = ", volume )

        mass = volume*q
        #print( "mass, kg = ", mass)
        #print( "mass, g = ", (mass*1e3))

        #FreeCAD.Console.PrintMessage("Volume[m3] = %.2f, Volume[mm] = %.2f, mass[kg] = %.2f, mass[g] = %.2f" % (volume, volume*1e9, mass, mass*1e3) )
        wynik = "Volume[m3] = %.2f, Volume[mm3] = %.2f, mass[kg] = %.2f, mass[g] = %.2f, Area=%.2fmm2, Area=%.2fm2" % (volume, volume*1e9, mass, mass*1e3,A, A*1e-6)
        #Gui.doCommand("%s" % wynik)
        #FreeCAD.Console.PrintMessage("%s" % wynik)

        QtGui.QMessageBox.information(QtGui.QWidget(), "Message", "%s" % wynik)
        
        #return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


