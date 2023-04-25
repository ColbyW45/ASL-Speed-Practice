# ASL Finger Spelling Practice

import random as r
import os, sys, pandas

from PyQt6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QPushButton, QSlider, QLabel, QMenuBar, QMenu, QToolBar, QSpacerItem, QCheckBox,
	QProgressBar, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMdiArea, QGraphicsScene, QGraphicsView
)
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import (Qt, QObject, QUrl, QThread, pyqtSignal)
from PyQt6.QtGui import (QIcon, QFont, QGuiApplication, QColor)

class Window(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("ASL Practice")
		# Set window Icon (Currently placeholder)
		self.setWindowIcon(QIcon("icons\icon.jpeg"))
		self.setContentsMargins(5, 5, 5, 5)
		self.resize(750,500)

		# Load data (move later)
		lettersDict = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J", 11:"K", 12:"L", 13:"M", 14:"N", 
		   			15:"O", 16:"P", 17:"Q", 18:"R", 19:"S", 20:"T", 21:"U", 22:"V", 23:"W", 24:"X", 25:"Y", 26:"Z"}
		self.R = Randomizer(lettersDict)
		
		# Menu Bar
		appMenu = QMenuBar()
		fileMenuItem = QMenu("&File", self)
		appMenu.addMenu(fileMenuItem)

		fileMenuItem.addAction("&Load")

		#fileMenuItem.is
		
		editMenuItem = QMenu("&Edit",self)
		appMenu.addMenu(editMenuItem)
		self.setMenuBar(appMenu)
		
		self.updateBtn = QPushButton("Update")
		self.button2 = QPushButton("Load")
		#tabBar.addTab(self.updateBtn, "Menu")
		
		# Home layout
		self.Home()

	def SettingsToolBar(self):

		#settingsToolbar = QToolBar()

		# Create settings toolbar layout
		settingsToolbarWidget = QWidget()
		settingsToolbarLayout = QHBoxLayout()
		settingsToolbarWidget.setLayout(settingsToolbarLayout)
		
		# Add spacing
		settingsToolbarLayout.addSpacing(50)
		
		# Delay input label
		delayInputLabel = QLabel("Time between letters:")
		delayInputLabel.setMaximumWidth(115)
		settingsToolbarLayout.addWidget(delayInputLabel)

		# Delay input field
		self.delayInput = QSlider(Qt.Orientation.Horizontal)
		self.delayInput.setRange(1, 5)
		self.delayInput.setValue(2)
		self.delayInput.setSingleStep(1)
		self.delayInput.setMaximumWidth(75)
		self.delayInput.setTickPosition(QSlider.TickPosition.TicksBelow)
		self.delayInput.setTickInterval(1)

		settingsToolbarLayout.addWidget(self.delayInput, Qt.AlignmentFlag.AlignLeft)

		self.delayInput.valueChanged.connect(self.DelayUpdated)

		# Defines timer ON RUNTIME, updated in self.DelayUpdated()
		# Interval in milliseconds
		self.timer = QtCore.QTimer(self, interval=self.delayInput.value() * 5, timeout=self.Run)

		# Add delay input field value indicator
		self.delayInputVal = QLabel(str(self.delayInput.value()*0.25))
		self.delayInputVal.setMaximumWidth(25)
		settingsToolbarLayout.addWidget(self.delayInputVal)

		# Add spacing
		settingsToolbarLayout.addSpacing(10)

		# Ramp speed label
		delayInputLabel = QLabel("Gradually ramp speed?")
		delayInputLabel.setMaximumWidth(125)
		settingsToolbarLayout.addWidget(delayInputLabel)

		# Ramp speed check box 
		self.rampSpeedToggle = QCheckBox()
		#self.rampSpeedToggle.setMaximumWidth(15)
		settingsToolbarLayout.addWidget(self.rampSpeedToggle)

		# Add spacing
		settingsToolbarLayout.addSpacing(10)

		# Play button
		self.playButton = QPushButton()
		self.playButton.setIcon(QIcon("icons\play-icon.png"))
		self.playButton.setMaximumWidth(50)
		settingsToolbarLayout.addWidget(self.playButton)

		# Pause button
		self.pauseButton = QPushButton()
		self.pauseButton.setIcon(QIcon("icons\pause-icon.png"))
		self.pauseButton.setMaximumWidth(50)
		settingsToolbarLayout.addWidget(self.pauseButton)


		#settingsToolbar.addWidget(settingsToolbarWidget)

		return settingsToolbarWidget

		
	def Home(self):
		#toolbar = self.SettingsToolBar()
		#self.addToolBar(toolbar)

		central_widget = QWidget()
		central_widget_layout = QHBoxLayout()
		central_widget.setLayout(central_widget_layout)

		# Left Column
		self.left_column_widget = QWidget()
		left_column_layout = QGridLayout()
		self.left_column_widget.setLayout(left_column_layout)
		
		self.leftColumnMinWidth = 35
		self.leftColumnMaxWidth = 100

		central_widget_layout.addWidget(self.left_column_widget)

		self.left_column_widget.setFixedWidth(self.leftColumnMinWidth)

		#self.left_column_widget.setStyleSheet(
			#"background:#6c757d;"
					#)

		#left_column_layout.addWidget(QWidget(), 0, 0, Qt.AlignmentFlag.AlignTop)

		# Load file menu toggle
		self.fileMenuToggleState = False
		self.fileMenuToggle = QPushButton("T")
		self.fileMenuToggle.setMaximumWidth(15)
		self.fileMenuToggle.clicked.connect(self.File_Menu_View_Toggle)
		left_column_layout.addWidget(self.fileMenuToggle, 1, 0, Qt.AlignmentFlag.AlignTop)

		#self.load_file_button = QPushButton("Load File")
		#left_column_layout.addWidget(self.load_file_button)

		#self.load_file_button.clicked.connect()

		# ******************************************

		# Right Column
		right_column_widget = QWidget()
		right_column_layout = QVBoxLayout()
		right_column_widget.setLayout(right_column_layout)
		
		right_column_widget.setMinimumWidth(500)

		central_widget_layout.addWidget(right_column_widget)

		# Add option bar
		right_column_layout.addWidget(self.SettingsToolBar())

		# Creates the GraphicDisplay widget
		self.TextGraphicDisplay()

		# Adds the GraphicDisplay widget to central widget layout
		right_column_layout.addWidget(self.GraphicsView)
		
		# Progress Bar
		self.progBarVal = 0
		self.progBarMax = 250

		self.progressBar = QProgressBar()
		self.progressBar.setFixedHeight(20)
		self.progressBar.setMaximum(self.progBarMax)
		right_column_layout.addWidget(self.progressBar) 
		
		self.setCentralWidget(central_widget)

		self.playButton.clicked.connect(self.playButtonPressed)
		self.pauseButton.clicked.connect(self.pauseButtonPressed)

	def FilePreviewWindow(self):
		file_list = QWidget()
		fl_layout = QGridLayout()
		file_list.setLayout(fl_layout)

		file_option_1 = QPushButton()
		file_option_2 = QPushButton()
		file_option_3 = QPushButton()
		file_option_4 = QPushButton()
		file_option_5 = QPushButton()
		file_option_6 = QPushButton()

		for file in range(len(os.listdir('.\data'))):
			print(file)



	# Button Functions
	@QtCore.pyqtSlot()
	def playButtonPressed(self):
		#self.timer = 0
		QtCore.QTimer.singleShot(0, self.Run)
		self.timer.start()

	@QtCore.pyqtSlot()
	def pauseButtonPressed(self):
		self.timer.stop()

	def Home_To_File_Preview_Window(self):
		#self.setcentralWidget()
		pass

	def File_Menu_View_Toggle(self):
		if self.fileMenuToggleState == False:
			self.fileMenuToggleState = True
			self.left_column_widget.setFixedWidth(self.leftColumnMaxWidth)
		
		elif self.fileMenuToggleState == True:
			self.fileMenuToggleState = False
			self.left_column_widget.setFixedWidth(self.leftColumnMinWidth)

		



	def Run(self):
		#print(self.delayInput.text())

		self.progBarVal += 1
		self.progressBar.setValue(int(self.progBarVal))

		if self.progBarVal == self.progBarMax:
			self.progBarVal = 0

			self.UpdateGDText()
			
	def DelayUpdated(self):
		self.delayInputVal.setText(str(self.delayInput.value()*0.25))
		# Interval in milliseconds
		self.timer.setInterval(self.delayInput.value() * 5)
		
	def TextGraphicDisplay(self):
		self.scene = QGraphicsScene()

		displayString = self.R.randomStr()
		text = displayString

		displayFont = QFont("Atkinson Hyperlegible", 150)
		displayFont.setBold(True)
		self.textObject = self.scene.addSimpleText(text, displayFont)

		self.GraphicsView = QGraphicsView(self.scene, self)
		#self.GraphicsView.
		#GraphicsView.setGeometry(0,0,600,500)

	def UpdateGDText(self, displayString="Error: could not load display element"):
		displayString = self.R.randomStr()
		#print(displayString)
		self.textObject.setText(displayString)


class Randomizer():

	def __init__(self, items) -> None:
		self.items = items
		self._testStr = "Test string"

	def randomStr(self):			
		itemsKey = r.randint(1,26)
		a = self.items[itemsKey]
			
		return a
	
class Data():
	lettersDict = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J", 11:"K", 12:"L", 13:"M", 14:"N", 
		   			15:"O", 16:"P", 17:"Q", 18:"R", 19:"S", 20:"T", 21:"U", 22:"V", 23:"W", 24:"X", 25:"Y", 26:"Z"}
	
	def CSV_Handler():
		file = r'.\data\alphabet.csv'

		csv_ds = pandas.read_csv(file, header=0)
		print(csv_ds)
		
		test = dict(csv_ds)
		print(test)



def main() -> None :
	# Start PyQt application
	#print(os.listdir('.\data'))
	app = QApplication(sys.argv)
	
	window = Window()
	window.show()

	Data.CSV_Handler()

	sys.exit(app.exec())

main()