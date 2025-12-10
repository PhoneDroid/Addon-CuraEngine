# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2014 cblt2l
# SPDX-FileNotice: Part of the CuraEngine addon.

from .PySide import QtWidgets
from FreeCAD import activeDocument , Console , ParamGet , Gui
from pivy import coin
from os import path


# Default Values
defaultVals = {"machinex":100, "machiney":100, "machinez":100, "offsetx":20, "offsety":20, "bedx":100, "bedy":100}
#-------------------------------------------------

def makePrintBedGrp():

    grp = activeDocument().addObject("App::DocumentObjectGroup","PrintBedGroup")
    PrintBedGroup(grp)
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")
#    PrintBed(obj)
#    ViewProviderPrintBed(obj.ViewObject)


class PrintBedGroup:
    def __init__(self, grp):
        # Create objects for the printbed and print volume

        document = activeDocument()

        pbed = document.addObject("App::FeaturePython","PrintBed")
        pvol = document.addObject("App::FeaturePython","PrintVolume")

        # Create an object & view provider for the print bed
        PrintBed(pbed)
        ViewProviderPrintBed(pbed.ViewObject)

        # Create an object & view provider for the print volume
        PrintVolume(pvol)
        ViewProviderPrintVolume(pvol.ViewObject)

        # Add the PrintBed and PrintVolume objects to the group
        grp.addObject(pbed)
        grp.addObject(pvol)

class PrintBed:
    'The PrintBed Object'
    def __init__(self, obj):
        obj.addProperty("App::PropertyDistance", "XSize", "PrintBed", "The X Dimension of the Bed").XSize=readSetting("bedx")
        obj.addProperty("App::PropertyDistance", "YSize", "PrintBed", "The Y Dimension of the Bed").YSize=readSetting("bedy")
        obj.addProperty("App::PropertyDistance", "XOffset", "PrintBed", "The X Offset of the Bed").XOffset=readSetting("offsetx")
        obj.addProperty("App::PropertyDistance", "YOffset", "PrintBed", "The Y Offset of the Bed").YOffset=readSetting("offsety")
        obj.Proxy = self
        self.Type = "PrintBed"

    def onChanged(self, fp, prop):
        Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        Console.PrintMessage("Recompute PrintBed feature\n")

class ViewProviderPrintBed:
    'The PrintBed View Provider Object'
    def __init__(self, obj):
        obj.addProperty("App::PropertyColor","Color","PrintBed","Color of the box").Color=(1.0,0.0,0.0)
        obj.Proxy = self

    def attach(self, obj):
        "'''Setup the scene sub-graph of the view provider, this method is mandatory'''"
        self.shaded = coin.SoGroup()
        self.wireframe = coin.SoGroup()
        self.scale = coin.SoScale()
        self.color = coin.SoBaseColor()
        self.trans = coin.SoTranslation()

        self.data=coin.SoCube()
        # Top of print bed is X-Y plane
        self.trans.translation.setValue([0,0,-0.5])
        self.shaded.addChild(self.trans)
        self.shaded.addChild(self.scale)
        self.shaded.addChild(self.color)
        self.shaded.addChild(self.data)
        obj.addDisplayMode(self.shaded,"Shaded")
        style=coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        self.wireframe.addChild(style)
        self.wireframe.addChild(self.scale)
        self.wireframe.addChild(self.color)
        self.wireframe.addChild(self.data)
        obj.addDisplayMode(self.wireframe,"Wireframe")
        self.onChanged(obj,"Color")

    def updateData(self, fp, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        # fp is the handled feature, prop is the name of the property that has changed
        x = fp.getPropertyByName("XSize").Value
        y = fp.getPropertyByName("YSize").Value
        z = 1.0
        ox = fp.getPropertyByName("XOffset").Value
        oy = fp.getPropertyByName("YOffset").Value
        # Set the size of the PrintBed
        self.data.width = x
        self.data.height = y
        self.data.depth = z
        # Translate the printbed to proper location
        self.trans.translation.setValue([(x/2)+ox, (y/2)+oy, -0.5])
        pass

    def getDisplayModes(self,obj):
        "'''Return a list of display modes.'''"
        modes=[]
        modes.append("Shaded")
        modes.append("Wireframe")
        return modes

    def getDefaultDisplayMode(self):
        "'''Return the name of the default display mode. It must be defined in getDisplayModes.'''"
        return "Shaded"

    def setDisplayMode(self,mode):
        return mode

    def onChanged(self, vp, prop):
        "'''Here we can do something when a single property got changed'''"
        Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop == "Color":
            c = vp.getPropertyByName("Color")
            self.color.rgb.setValue(c[0],c[1],c[2])

    def getIcon(self):
        return ":/icons/PartDesign_Revolution.svg"

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

class PrintVolume:
    'The StrokeLimit Object'
    def __init__(self, obj):
        obj.addProperty("App::PropertyDistance", "XStroke", "Machine", "The X Axis Stroke").XStroke=readSetting("machinex")
        obj.addProperty("App::PropertyDistance", "YStroke", "Machine", "The Y Axis Stroke").YStroke=readSetting("machiney")
        obj.addProperty("App::PropertyDistance", "ZStroke", "Machine", "The Z Axis Stroke").ZStroke=readSetting("machinez")
        obj.Proxy = self
        self.Type = "Machine"

    def onChanged(self, fp, prop):
        Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        Console.PrintMessage("Recompute Machine feature\n")

class ViewProviderPrintVolume:
    'The StrokeLimit View Provider Object'
    def __init__(self, obj):
        #obj.addProperty("App::PropertyColor","Color","Machine","Color of the box").Color=(1.0,0.0,0.0)
        obj.Proxy = self

    def attach(self, obj):
        "'''Setup the scene sub-graph of the view provider, this method is mandatory'''"
        self.wireframe = coin.SoGroup()
        self.scale = coin.SoScale()
#        self.color = coin.SoBaseColor()
        self.trans = coin.SoTranslation()

        self.data=coin.SoCube()
        # Switch Z to proper default value
        self.trans.translation.setValue([0,0,100])
        self.wireframe.addChild(self.trans)
        style=coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        self.wireframe.addChild(style)
        self.wireframe.addChild(self.scale)
#        self.wireframe.addChild(self.color)
        self.wireframe.addChild(self.data)
        obj.addDisplayMode(self.wireframe,"Wireframe")

    def updateData(self, fp, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        # fp is the handled feature, prop is the name of the property that has changed
        x = fp.getPropertyByName("XStroke").Value
        y = fp.getPropertyByName("YStroke").Value
        z = fp.getPropertyByName("ZStroke").Value
        # Translate box to keep corner at (0,0)
        self.trans.translation.setValue([x/2 ,y/2 , z/2])
        self.data.width = x
        self.data.height = y
        self.data.depth = z
        pass

    def getDisplayModes(self,obj):
        "'''Return a list of display modes.'''"
        modes=[]
        modes.append("Wireframe")
        return modes

    def getDefaultDisplayMode(self):
        "'''Return the name of the default display mode. It must be defined in getDisplayModes.'''"
        return "Wireframe"

    def setDisplayMode(self,mode):
        return mode

    def onChanged(self, vp, prop):
        "'''Here we can do something when a single property got changed'''"
        Console.PrintMessage("Change property: " + str(prop) + "\n")
#        if prop == "Color":
#            c = vp.getPropertyByName("Color")
#            self.color.rgb.setValue(c[0],c[1],c[2])

    def getIcon(self):
        return ":/icons/PartDesign_Revolution.svg"

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

class PrintBedTaskPanel:
    def __init__(self):

        file = path.join(path.dirname(__file__),'MachineDef.ui')

        self.form = Gui.PySideUic.loadUi(file) # type: ignore

        self.form.doubleSpinBox_1.setValue(readSetting("machinex"))
        self.form.doubleSpinBox_2.setValue(readSetting("machiney"))
        self.form.doubleSpinBox_3.setValue(readSetting("machinez"))
        self.form.doubleSpinBox_6.setValue(readSetting("offsetx"))
        self.form.doubleSpinBox_7.setValue(readSetting("offsety"))
        self.form.doubleSpinBox_4.setValue(readSetting("bedx"))
        self.form.doubleSpinBox_5.setValue(readSetting("bedy"))

        self.form.doubleSpinBox_1.valueChanged.connect(self._machineXStroke)
        self.form.doubleSpinBox_2.valueChanged.connect(self._machineYStroke)
        self.form.doubleSpinBox_3.valueChanged.connect(self._machineZStroke)
        self.form.doubleSpinBox_6.valueChanged.connect(self._bedXOffset)
        self.form.doubleSpinBox_7.valueChanged.connect(self._bedYOffset)
        self.form.doubleSpinBox_4.valueChanged.connect(self._bedXSize)
        self.form.doubleSpinBox_5.valueChanged.connect(self._bedYSize)

    def accept(self):
        makePrintBedGrp()
        Gui.Control.closeDialog()

    def reject(self):
        Gui.Control.closeDialog()

    def getStandardButtons(self):
        return QtWidgets.QDialogButtonBox.StandardButton.Ok|QtWidgets.QDialogButtonBox.StandardButton.Cancel

    def _machineXStroke(self, val):
        writeSetting("machinex", val)

    def _machineYStroke(self, val):
        writeSetting("machiney", val)

    def _machineZStroke(self, val):
        writeSetting("machinez", val)

    def _bedXOffset(self, val):
        writeSetting("offsetx", val)

    def _bedYOffset(self, val):
        writeSetting("offsety", val)

    def _bedXSize(self, val):
        writeSetting("bedx", val)

    def _bedYSize(self, val):
        writeSetting("bedy", val)

def readSetting(key):
    global defaultVals
    grp = ParamGet("User parameter:BaseApp/Preferences/Mod/3DPrinting/MachineDef")
    val = grp.GetFloat(key, defaultVals[key])
    Console.PrintMessage("Reading Key: " + key + " Value: " + str(val) + "\n")
    return val

def writeSetting(key, val):
    grp = ParamGet("User parameter:BaseApp/Preferences/Mod/3DPrinting/MachineDef")
    Console.PrintMessage("Setting " + key + " to " + str(val) + '\n')
    grp.SetFloat(key, val)

# Run as macro
#panel=PrintBedTaskPanel()
#FreeCADGui.Control.showDialog(panel)
