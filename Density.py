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

class Density():
    """My new command"""

    from os.path import join, dirname
    import my_mod_locator
    mymod_icons_path =  join( dirname(my_mod_locator.__file__), 'Icons')
    Icon = join( mymod_icons_path , 'Density.png')

    def GetResources(self):
        return {'Pixmap'  : self.Icon, # the name of a svg file available in the resources
                'Accel' : "Shift+D", 
                'MenuText': "density",
                'ToolTip' : "Calc density"}

    def Activated(self):
        "Do something here"
        
        from PySide import QtGui
        import FreeCAD


        volume = Gui.Selection.getSelectionEx()[0].Object.Shape.Volume

        m = float(str(QtGui.QInputDialog.getText(None, "Get text", "mass, g = ")[0])) # mass, g

        #volume = volume * 1e-9 # m3

        q = m/(volume*1e-6) # density, kg/m3

        QtGui.QMessageBox.information(QtGui.QWidget(), "Message", "q = %.3f kg/m3" % q)

        
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


