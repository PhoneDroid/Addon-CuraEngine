# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2014 cblt2l
# SPDX-FileNotice: Part of the CuraEngine addon.

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
