# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the CuraEngine addon.

################################################################################
#                                                                              #
#   Copyright (c) 2014 cblt2l                                                  #
#                                                                              #
#   This library is free software; you can redistribute it and/or modify it    #
#   under the terms of the GNU Lesser General Public License as published      #
#   by the Free Software Foundation; either version 2.1 of the License, or     #
#   (at your option) any later version.                                        #
#                                                                              #
#   This library is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                       #
#                                                                              #
#   See the GNU Lesser General Public License for more details.                #
#                                                                              #
#   You should have received a copy of the GNU Lesser General Public License   #
#   along with this library; if not, write to the Free Software Foundation,    #
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA           #
#                                                                              #
################################################################################

class TDPrinting ( Workbench ):
	"Workbench for 3D Printers"
	Icon = """
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
			"""
	MenuText = "3D Printing"
	ToolTip = "Workbench for 3D Printing"

        def GetClassName(self):
               return "Gui::PythonWorkbench"

	def Initialize(self):
		#import myModule1, myModule2
		import Commands
		list = ["createMachineDef", "sliceCuraEngine"]
		self.appendToolbar("3D Printing", list)
		self.appendMenu("3D Printing", list)
		self.appendCommandbar("PyModuleCommands",list)
		Log ("Loading MyModule... done\n")

	def Activated(self):
               # do something here if needed...
		Msg ("MyWorkbench.Activated()\n")

	def Deactivated(self):
               # do something here if needed...
		Msg ("MyWorkbench.Deactivated()\n")

FreeCADGui.addWorkbench(TDPrinting)
