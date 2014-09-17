from PyQt4 import QtGui, QtCore
from PIL import Image, ImageDraw, ImageFont, ImageQt
import sys
import re
from os import path

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

LABEL = "resources/label.png"
SAVE_PATH = "output/"
FONT = "resources/CaeciliaLTStd-Bold.otf"
ICON = "resources/Kindle.png"
class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.im = ""
        self.initUI()
        self.retranslateUi()
        self.setState(False)
        self.initActions()
        self.initVariables()
        
    def initVariables(self):
        
        self.text_x = 10
        self.text_y = 10
        self.text_color = None
        self.is_label = True
        self.is_text = False
        
        self.font_size = 40
        self.font = ImageFont.truetype(FONT, self.font_size)
        self.pic = None
        self.clear_pic = None
        self.label = Image.open(LABEL).convert("RGBA")
        self.file_path = None

    def initUI(self):
        
        self.centralWidget = QtGui.QWidget(self)
        self.MainLayout = QtGui.QHBoxLayout(self.centralWidget)
        #------------------------------------------
        self.LeftVertLayout = QtGui.QVBoxLayout()
        
        self.open_HorLayout = QtGui.QHBoxLayout()
        
        self.open_path = QtGui.QLineEdit(self.centralWidget)
        self.open_path.setMinimumSize(QtCore.QSize(0, 20))
        self.open_path.setReadOnly(True)
        self.button_open = QtGui.QPushButton(self.centralWidget)
        self.button_open.setMinimumSize(QtCore.QSize(0, 20))
        
        self.open_HorLayout.addWidget(self.open_path)
        self.open_HorLayout.addWidget(self.button_open)
        self.LeftVertLayout.addLayout(self.open_HorLayout)
        #------------------------------------------
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.LeftVertLayout.addItem(spacerItem)
        #------------------------------------------
        self.line_1 = QtGui.QFrame(self.centralWidget)
        self.line_1.setFrameShape(QtGui.QFrame.HLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_1)
        #------------------------------------------
        self.name_Grid = QtGui.QGridLayout()
        self.label_name = QtGui.QLabel(self.centralWidget)
        self.label_surname = QtGui.QLabel(self.centralWidget)
        self.name = QtGui.QLineEdit(self.centralWidget)
        self.surname = QtGui.QLineEdit(self.centralWidget)
        
        self.name_Grid.addWidget(self.label_name, 0, 0, 1, 1)     
        self.name_Grid.addWidget(self.label_surname, 1, 0, 1, 1)
        self.name_Grid.addWidget(self.name, 0, 1, 1, 1)
        self.name_Grid.addWidget(self.surname, 1, 1, 1, 1)
        self.LeftVertLayout.addLayout(self.name_Grid)
        #------------------------------------------
        self.line_2 = QtGui.QFrame(self.centralWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_2)
        #------------------------------------------
        self.textcolor_Grid = QtGui.QGridLayout()
        self.buttonGroup_TextColor = QtGui.QButtonGroup(self)
        
        self.radio_White = QtGui.QRadioButton(self.centralWidget)
        self.radio_White.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_White.setChecked(True)
        self.radio_Black = QtGui.QRadioButton(self.centralWidget)
        self.radio_Black.setMinimumSize(QtCore.QSize(0, 20))
        
        self.buttonGroup_TextColor.addButton(self.radio_White)
        self.textcolor_Grid.addWidget(self.radio_White, 1, 0, 1, 1)
        self.buttonGroup_TextColor.addButton(self.radio_Black)
        self.textcolor_Grid.addWidget(self.radio_Black, 2, 0, 1, 1)
        
        self.label_textcolor = QtGui.QLabel(self.centralWidget)
        self.label_textcolor.setMinimumSize(QtCore.QSize(0, 20))
        self.textcolor_Grid.addWidget(self.label_textcolor, 0, 1, 1, 1)
        
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.textcolor_Grid.addItem(spacerItem1, 0, 2, 1, 1)
        
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.textcolor_Grid.addItem(spacerItem2, 0, 0, 1, 1)
        self.LeftVertLayout.addLayout(self.textcolor_Grid)
        #------------------------------------------
        self.line_3 = QtGui.QFrame(self.centralWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_3)
        #------------------------------------------
        self.placetext_Grid = QtGui.QGridLayout()
        self.label_wherePlace = QtGui.QLabel(self.centralWidget)
        self.label_wherePlace.setMinimumSize(QtCore.QSize(0, 20))
        self.label_wherePlace.setMaximumSize(QtCore.QSize(16777215, 20))
        
        self.placetext_Grid.addWidget(self.label_wherePlace, 2, 0, 1, 1)
        
        self.grid_radio_placetext = QtGui.QGridLayout()
        self.radio_leftupper = QtGui.QRadioButton(self.centralWidget)
        self.radio_leftupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_leftupper.setChecked(True)
        
        self.buttonGroup_PlaceText = QtGui.QButtonGroup(self)
        self.buttonGroup_PlaceText.addButton(self.radio_leftupper)
        self.grid_radio_placetext.addWidget(self.radio_leftupper, 0, 0, 1, 1)
        
        self.radio_rightlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightlower.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_rightlower.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonGroup_PlaceText.addButton(self.radio_rightlower)
        self.grid_radio_placetext.addWidget(self.radio_rightlower, 1, 1, 1, 1)
        self.radio_leftlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_leftlower.setMinimumSize(QtCore.QSize(0, 20))
        self.buttonGroup_PlaceText.addButton(self.radio_leftlower)
        self.grid_radio_placetext.addWidget(self.radio_leftlower, 1, 0, 1, 1)
        self.radio_rightupper = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_rightupper.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonGroup_PlaceText.addButton(self.radio_rightupper)
        self.grid_radio_placetext.addWidget(self.radio_rightupper, 0, 1, 1, 1)
        self.placetext_Grid.addLayout(self.grid_radio_placetext, 3, 0, 1, 1)
        self.LeftVertLayout.addLayout(self.placetext_Grid)
        #------------------------------------------
        self.line_4 = QtGui.QFrame(self.centralWidget)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_4)
        #------------------------------------------
        self.version_HorLayout = QtGui.QHBoxLayout()
        self.label_versionKindle = QtGui.QLabel(self.centralWidget)
        self.label_versionKindle.setMinimumSize(QtCore.QSize(0, 20))
        self.label_versionKindle.setMaximumSize(QtCore.QSize(16777215, 20))
        self.version_HorLayout.addWidget(self.label_versionKindle)
        self.combo_versionKindle = QtGui.QComboBox(self.centralWidget)
        self.combo_versionKindle.setMinimumSize(QtCore.QSize(0, 20))
        self.combo_versionKindle.addItem(_fromUtf8(""))
        self.combo_versionKindle.addItem(_fromUtf8(""))
        self.combo_versionKindle.addItem(_fromUtf8(""))
        self.version_HorLayout.addWidget(self.combo_versionKindle)
        self.LeftVertLayout.addLayout(self.version_HorLayout)
        #------------------------------------------
        self.line_5 = QtGui.QFrame(self.centralWidget)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_5)
        #------------------------------------------
        self.slide_HorLayout = QtGui.QHBoxLayout()
        self.check_slide = QtGui.QCheckBox(self.centralWidget)
        self.check_slide.setChecked(True)
        self.slide_HorLayout.addWidget(self.check_slide)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.slide_HorLayout.addItem(spacerItem3)
        self.LeftVertLayout.addLayout(self.slide_HorLayout)
        #------------------------------------------
        self.button_create = QtGui.QPushButton(self.centralWidget)
        self.button_create.setMinimumSize(QtCore.QSize(0, 20))
        self.LeftVertLayout.addWidget(self.button_create)
        #------------------------------------------
        self.MainLayout.addLayout(self.LeftVertLayout)
        self.RightVertLayout = QtGui.QVBoxLayout()
        
        self.picture_label = QtGui.QLabel(self.centralWidget)
        self.picture_label.setMinimumSize(QtCore.QSize(300, 400))
        self.picture_label.setMaximumSize(QtCore.QSize(300, 400))
        self.picture_label.setStyleSheet(_fromUtf8("border-style: solid;\n"
                                                   "border-width: 1px;\n"
                                                   "border-color: white;"))
        self.RightVertLayout.addWidget(self.picture_label)
        #------------------------------------------
        self.grid_arrows = QtGui.QGridLayout()
        self.button_up = QtGui.QPushButton(self.centralWidget)
        self.button_up.setMinimumSize(QtCore.QSize(35, 35))
        self.button_up.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_up, 0, 1, 1, 1, QtCore.Qt.AlignBottom)
        self.button_left = QtGui.QPushButton(self.centralWidget)
        self.button_left.setMinimumSize(QtCore.QSize(35, 35))
        self.button_left.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_left, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.button_right = QtGui.QPushButton(self.centralWidget)
        self.button_right.setMinimumSize(QtCore.QSize(35, 35))
        self.button_right.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_right, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.button_down = QtGui.QPushButton(self.centralWidget)
        self.button_down.setMinimumSize(QtCore.QSize(35, 35))
        self.button_down.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_down, 2, 1, 1, 1, QtCore.Qt.AlignTop)
        self.RightVertLayout.addLayout(self.grid_arrows)
        #------------------------------------------
        self.MainLayout.addLayout(self.RightVertLayout)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 648, 20))
        self.menuMain = QtGui.QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.action_Exit = QtGui.QAction(self)
        self.menuMain.addAction(self.action_Exit)
        self.menuBar.addAction(self.menuMain.menuAction())

        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle("MainWindow")
        
        #for ico files 
        #im = QtGui.QImageReader(ICON).read()
        #self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(ICON))
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.button_open.setText("Open...")
        self.label_name.setText("Name")
        self.label_surname.setText("Surname")
        self.radio_White.setText("White")
        self.radio_Black.setText("Black")
        self.label_textcolor.setText("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Text color</span></p></body></html>")
        self.label_wherePlace.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Where to place text</span></p></body></html>")
        self.radio_leftupper.setText("Left Upper")
        self.radio_rightlower.setText("Right Lower")
        self.radio_leftlower.setText("Left Lower")
        self.radio_rightupper.setText("Right Upper")
        self.label_versionKindle.setText("Version of Kindle")
        self.combo_versionKindle.setItemText(0, "Kindle 3, 4, 5, Touch (800 x 600)")
        self.combo_versionKindle.setItemText(1, "Kindle DX (1200 x 824)")
        self.combo_versionKindle.setItemText(2, "Kindle Paperwhite (1024 x 768)")
        
        self.check_slide.setText("Slide and release the power to wake")
        self.button_create.setText("Create")
        self.picture_label.setText("<html><head/><body><p align=\"center\"><br/></p></body></html>")
        self.button_up.setText("ᐃ")
        self.button_up.setShortcut("Up")
        self.button_left.setText("ᐊ")
        self.button_left.setShortcut("Left")
        self.button_right.setText("ᐅ")
        self.button_right.setShortcut("Right")
        self.button_down.setText("ᐁ")
        self.button_down.setShortcut("Down")
        self.menuMain.setTitle("Main")
        self.action_Exit.setText("&Exit")
        
    def setState(self, enabled):
                      
        self.name.setEnabled(enabled)
        self.surname.setEnabled(False)
        self.radio_leftlower.setEnabled(enabled)
        self.radio_leftupper.setEnabled(enabled)
        self.radio_rightlower.setEnabled(enabled)
        self.radio_rightupper.setEnabled(enabled)
        self.radio_Black.setEnabled(enabled)
        self.radio_White.setEnabled(enabled)
        self.combo_versionKindle.setEnabled(enabled)
        self.check_slide.setEnabled(enabled)
        self.button_left.setEnabled(enabled)
        self.button_right.setEnabled(enabled)
        self.button_up.setEnabled(enabled)
        self.button_down.setEnabled(enabled)

    def putImage(self):
        
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.pic))
        pixmap = pixmap.scaled(self.picture_label.size())
        self.picture_label.setPixmap(pixmap)
    
    
    
    def redraw(self, glob_redraw=False):
        
        self.is_label = self.check_slide.isChecked()
        self.is_text = self.name.text() or self.surname.text()
        self.pic = Image.open(self.file_path)
        self.pic = self.pic.convert("RGBA")
        
        if self.pic.size != (600, 800):
            self.pic = self.pic.resize((600, 800))
        if self.is_label:
            self.pic.paste(self.label, (0, self.pic.size[1] - self.label.size[1]), mask= self.label)
        
        if glob_redraw:
            self.resizeImage()
        
        if self.is_text:
            size = self.font_size
            draw = ImageDraw.Draw(self.pic)
            font = self.font
            text_color = "White"
            if self.radio_Black.isChecked():
                text_color = "Black"
            else:
                text_color = "White"
            
            self.correctText(font=font, size=size)
            
            #draw name
            if self.name.text():
                draw.text((self.text_x, self.text_y), self.name.text(), text_color, font=font)
            #draw surname
            if self.surname.text():
                draw.text((self.text_x, self.text_y + size), self.surname.text(), text_color, font=font)
        
        if not glob_redraw:
            self.putImage()
        
    def moveText(self):
        default_move = {"ᐃ"  : (0, -10),
                                                "ᐊ" : (-10, 0),
                                                "ᐅ" : (10, 0),
                                                "ᐁ": (0, 10)}
        self.text_x += default_move[self.sender().text()][0]
        self.text_y += default_move[self.sender().text()][1]
        self.redraw()
    
    def placeText(self, corner):
        default_coord = {"Left Upper" : (10, 10),
                          "Left Lower" : (10, self.pic.size[1]),
                          "Right Upper" : (self.pic.size[0], 10),
                          "Right Lower" : (self.pic.size[0], self.pic.size[1])}
        
        self.text_x, self.text_y = default_coord[self.sender().text()]
        self.redraw()
    
    def correctText(self, font, size):
        
        font = font
        size_x = self.pic.size[0] - 10
        size_y = self.pic.size[1] - 10 - self.label.size[1]
        text_height = 0
        text_lenght = 0
        name = self.name.text()
        surname = self.surname.text()
        
        if self.text_x < 10:
            self.text_x = 10
        if self.text_y < 10:
            self.text_y = 10
        
        if name and surname:
            text_height = 2*size
        else:
            text_height = size
        
        if len(name) >= len(surname):
            text_lenght = font.getsize(name)[0]
        else:
            text_lenght = font.getsize(surname)[0]
                
        if self.text_x + text_lenght > size_x:
            dx = (self.text_x + text_lenght) - size_x
            self.text_x -= dx
        if self.text_y + text_height > size_y:
            dy = (self.text_y + text_height) - size_y
            self.text_y -= dy        
    
    def resizeImage(self):
        s = self.combo_versionKindle.currentText()
        pattern = re.compile(r"(\d*).x.(\d*)")
        height = int(re.search(pattern, s).group(1))
        width = int(re.search(pattern, s).group(2))
        self.pic = self.pic.convert("RGB")
        #upscaling
        
        if self.pic.size != (width, height):
            if self.pic.size > (width, height):
                self.pic = self.pic.resize((width, height), Image.ANTIALIAS) #downscaling
            else:
                self.pic = self.pic.resize((width, height), Image.BICUBIC)   #upscaling
        self.pic = self.pic.convert("RGBA")
    
    def openImage(self):
        try:
            self.file_path = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        except:
            self.statusBar.showMessage('Wrong file name')
        
        self.setState(enabled=True)
        self.redraw()
        
        self.open_path.setText(self.file_path)
        self.statusBar.showMessage("Opened file")
          
    def saveImage(self):
        
        default = "Sample"
        name = ""
        self.redraw(glob_redraw=True)
        if self.name.text():
            name+=self.name.text()
        if self.surname.text():
            name+= ' ' + self.surname.text()
        if not name:
            name = default
        name += ' ' + str(self.pic.size[1]) + 'x' + str(self.pic.size[0])
              
        if path.isfile(path.join(SAVE_PATH, name + ".png")):
            i = 2
            while path.isfile(path.join(SAVE_PATH, name+'-' + str(i) + '.png')):
                i+=1
            name+= '-' + str(i)
        name +=".png"
        self.pic.save(path.join(SAVE_PATH, name))
        self.statusBar.showMessage("File " + name +" created!")
    
    def surnameState(self):
        
        if self.name.text():
            self.surname.setEnabled(True)
        else:
            self.surname.setEnabled(False)
            self.surname.setText("")
            
    def initActions(self):
        
        self.check_slide.stateChanged.connect(lambda: self.redraw(False))
        self.button_open.clicked.connect(self.openImage)
        self.button_create.clicked.connect(self.saveImage)
        self.name.textChanged.connect(lambda: self.redraw(False))
        self.name.textChanged.connect(self.surnameState)
        self.surname.textChanged.connect(lambda: self.redraw(False))
        self.radio_Black.clicked.connect(lambda: self.redraw(False))
        self.radio_White.clicked.connect(lambda: self.redraw(False))
        self.radio_leftlower.clicked.connect(self.placeText)
        self.radio_leftupper.clicked.connect(self.placeText)
        self.radio_rightlower.clicked.connect(self.placeText)
        self.radio_rightupper.clicked.connect(self.placeText)
        self.button_up.pressed.connect(self.moveText)
        self.button_down.pressed.connect(self.moveText)
        self.button_left.pressed.connect(self.moveText)
        self.button_right.pressed.connect(self.moveText)

def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
    
def test():
    s = (400, 1200)
    r = (800, 600)
    print(r>s)
    
if __name__ == '__main__':
    main()
    #test()
