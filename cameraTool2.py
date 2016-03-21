from PyQt4 import QtCore, QtGui
import pymel.core as pm
from functools import partial


class QClickLabel(QtGui.QLabel):
    
    clicked = QtCore.pyqtSignal()
    
    def __init__(self, name):
        super(QClickLabel, self).__init__()
        self.setText(name)

    def mouseReleaseEvent(self, ev):
        self.clicked.emit()

class CameraWidget(QtGui.QTreeWidget):
    
    cameraClick = QtCore.pyqtSignal(QClickLabel)
    cameraLock = QtCore.pyqtSignal(QtGui.QCheckBox)
    cameraLensChange = QtCore.pyqtSignal(QtGui.QComboBox)
    
    select_node = None
    
    def __init__(self, camera_list=None, focal_lengths=None):        
        super(CameraWidget, self).__init__()
        
        if camera_list ==None:
            camera_list = self.getCameras()
        
        if focal_lengths ==None:
            focal_lengths = ['35mm', '50mm', '70mm']
        
        self.initUi(camera_list, focal_lengths)        
        self.setMultipleSelection(True)

    def initUi(self, camera_list, focal_lengths):
        
        self.setColumnCount(3)
        
        for row, camera in enumerate(camera_list):
            
            font = QtGui.QFont( "Arial", 10, QtGui.QFont.Bold)
            
            item = QtGui.QTreeWidgetItem()
            item.setText(0, camera.name())
            
            # Build custom Label with clickable signal
            #label = QClickLabel(camera.name())
            #label.row = row
            #label.clicked.connect(partial(self.cameraClicked, label))
            #label.setFont(font)
            
            # Build Checkbox and assign the row into the objext
            checkbox = QtGui.QCheckBox()
            checkbox.row = row
            checkbox.stateChanged.connect(partial(self.cameraLocked, checkbox))
            
            combo = QtGui.QComboBox()
            combo.row = row
            combo.insertItems(0, focal_lengths)
            combo.currentIndexChanged.connect(partial(self.cameraLensChanged, combo))
        
            self.setHeaderLabels(['Camera Name', 'Lock', 'Focal Length'])
            self.insertTopLevelItem(row, item)
            #self.setItemWidget(item, 0, label)
            self.setItemWidget(item, 1, checkbox)
            self.header().resizeSection(1, 50)
            self.setItemWidget(item, 2, combo)
        
        self.itemClicked.connect(self.selectCamera)
        self.itemClicked.connect(self.lookThruCamera)
        
    # ==== Maya Functions ====    
    def getCameras(self):
        """Filter out the cameras we want here and pass to build list"""
        camera_list = pm.ls(type='camera')
        return camera_list

    def selectCamera(self, item):
        camera = str(item.text(0))
        if pm.objExists(camera):
            pm.select(camera)
    
    def lookThruCamera(self, item):
        camera = str(item.text(0))
        if pm.objExists(camera):
            pm.lookThru(camera)
    
    # ==================
    
    def setMultipleSelection(self, settr):
        self._multiple_selection = settr
        if self._multiple_selection == True:
            self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        else:
            self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    
    # ==== SIGNALS ====
    def cameraClicked(self, camera):
        self.cameraClick.emit(camera)
    
    def cameraLocked(self, checkbox):
        self.cameraLock.emit(checkbox)
    
    def cameraLensChanged(self, combobox):
        self.cameraLensChange.emit(combobox)
        
if __name__ == '__main__':
        cam = CameraWidget()
        cam.show()