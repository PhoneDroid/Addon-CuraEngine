# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2014 cblt2l
# SPDX-FileNotice: Part of the CuraEngine addon.

from .Commands import registerCommands
from FreeCAD import Gui


class CuraEngineWorkbench ( Gui.Workbench ):

    MenuText = '3D Printing'
    ToolTip = 'Workbench for 3D Printing'

    Icon = '''
        /* XPM */
        static const char *test_icon[]={
        "16 16 2 1",
        "a c #000000",
        ". c None",
        "................",
        "..############..",
        "..############..",
        "..###......###..",
        "..###......###..",
        "..###......###..",
        "..############..",
        "..############..",
        "..####..........",
        "..####..........",
        "..####..........",
        "..####..........",
        "..####..........",
        "..####..........",
        "................",
        "................"};
    '''

    def GetClassName ( self ):
        return 'Gui::PythonWorkbench'

    def Initialize ( self ):

        registerCommands()

        list = [
            'createMachineDef' ,
            'sliceCuraEngine'
        ]

        self.appendToolbar('3D Printing',list)
        self.appendMenu('3D Printing',list)
        self.appendCommandbar('PyModuleCommands',list)

        print('Loading MyModule... done\n')

    def Activated ( self ):
        print('MyWorkbench.Activated()\n')

    def Deactivated ( self ):
        print('MyWorkbench.Deactivated()\n')

Gui.addWorkbench(CuraEngineWorkbench)
