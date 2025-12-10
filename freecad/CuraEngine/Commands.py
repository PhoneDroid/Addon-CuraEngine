# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2014 cblt2l
# SPDX-FileNotice: Part of the CuraEngine addon.

from .SlicerPanel import SlicerPanel
from .MachineDef import PrintBedTaskPanel

from FreeCAD import Console , Gui
from inspect import getsourcelines

# helper -------------------------------------------------------------------

def addCommand(name,cmdObject):
    (list,num) = getsourcelines(cmdObject.Activated)
    pos = 0
    # check for indentation
    while(list[1][pos] == ' ' or list[1][pos] == '\t'):
        pos += 1
    source = ""
    for i in range(len(list)-1):
        source += list[i+1][pos:]
    Gui.addCommand(name,cmdObject,source)


#---------------------------------------------------------------------------
# The command classes
#---------------------------------------------------------------------------

class createMachineDef:
    "Create a 3D Printer Definition"
    def Activated(self):
        panel = PrintBedTaskPanel()
        Gui.Control.showDialog(panel)
        Console.PrintMessage("Activated Machine Definition Command \n")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool1', 'MenuText': 'Create 3D Printer Definition', 'ToolTip': 'Define a 3D Printer'}

class sliceCuraEngine:
    "Run the CuraEngine Slicer Tool"
    def Activated(self):
        panel = SlicerPanel()
        Gui.Control.showDialog(panel)
        Console.PrintMessage("Activated CuraEngine Tool \n")

    def GetResources(self):
        return {'Pixmap'  : 'Std_Tool2', 'MenuText': 'Slice With CuraEngine', 'ToolTip': 'Run the CuraEngine Slicer Tool'}


def registerCommands ():
    Gui.addCommand('createMachineDef',createMachineDef())
    Gui.addCommand('sliceCuraEngine',sliceCuraEngine())
