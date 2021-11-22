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




class MassCalc(Workbench):

    MenuText = "MassCalc"
    ToolTip = "calculating mass from volume, calculating density, calculating how much heat you need to provide to heat a solid. "

    from os.path import join, dirname
    import my_mod_locator
    mymod_icons_path =  join( dirname(my_mod_locator.__file__), 'Icons')
    Icon = join( mymod_icons_path , 'FNLogo.svg')

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        #import MyModuleA, MyModuleB # import here all the needed files that create your FreeCAD commands

        import VolumeAreaMass
        import Volume
        import Mass
        import Density
        import Heat
        
        #from materialtools.cardutils import import_materials as getmats
        #m, c, i = getmats()


        FreeCADGui.addCommand('MassCalc_VolumeAreaMass',VolumeAreaMass.VolumeAreaMass())
        FreeCADGui.addCommand('MassCalc_Volume',Volume.Volume())
        FreeCADGui.addCommand('MassCalc_Mass',Mass.Mass())
        FreeCADGui.addCommand('MassCalc_Density',Density.Density())
        FreeCADGui.addCommand('MassCalc_Heat',Heat.Heat())
        #FreeCADGui.addCommand('HeatWater',HeatWater.HeatWater())
        
        self.list = ["MassCalc_VolumeAreaMass", "MassCalc_Volume", "MassCalc_Mass", "MassCalc_Density","MassCalc_Heat"]#, "HeatWater"] # A list of command names created in the line above
        self.appendToolbar("ToolbarVolumeAreaMass",self.list) # creates a new toolbar with your commands
        #self.appendMenu("My New Menu",self.list) # creates a new menu
        #self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        "This function is executed when the workbench is activated"
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"

       
Gui.addWorkbench(MassCalc())









