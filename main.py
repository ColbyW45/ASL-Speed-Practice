# ASL Finger Spelling Practice

import random as r
import sys, time

from PyQt6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QPushButton, QSlider, QLabel, QMenuBar, QToolBar, QSpacerItem, QCheckBox,
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
		self.setWindowIcon(QIcon("icon.jpeg"))
		self.setContentsMargins(5, 5, 5, 5)
		self.resize(500,500)

		# Vars at init
		self.playPauseBttnState = False

		# Load data (move later)
		lettersDict = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J", 11:"K", 12:"L", 13:"M", 14:"N", 
		   			15:"O", 16:"P", 17:"Q", 18:"R", 19:"S", 20:"T", 21:"U", 22:"V", 23:"W", 24:"X", 25:"Y", 26:"Z"}
		self.R = Randomizer(lettersDict)

		appMenu = QMenuBar()
		appMenu.addMenu("File")
		appMenu.addMenu("Edit")
		self.setMenuBar(appMenu)
		
		self.updateBtn = QPushButton("Update")
		self.button2 = QPushButton("Load")
		#tabBar.addTab(self.updateBtn, "Menu")
		
		# Home layout
		self.Home()

	def SettingsToolBar(self):

		settingsToolbar = QToolBar()
		self.addToolBar(settingsToolbar)

		# Create settings toolbar layout
		settingsToolbarWidget = QWidget()
		settingsToolbarLayout = QHBoxLayout()
		settingsToolbarWidget.setLayout(settingsToolbarLayout)
		
		# Delay input label
		delayInputLabel = QLabel("Time between letters:")
		delayInputLabel.setMaximumWidth(115)
		settingsToolbarLayout.addWidget(delayInputLabel)

		# Delay input field
		self.delayInput = QSlider(Qt.Orientation.Horizontal)
		#self.delayInput.TickPosition(self.delayInput.TicksBothSides)
		#self.delayInput.setText("1.75")
		self.delayInput.setMaximumWidth(50)

		settingsToolbarLayout.addWidget(self.delayInput, Qt.AlignmentFlag.AlignLeft)

		# Define QTimer using delay input field
		timerInterval = 2
		#float(self.delayInput.text())
		print(timerInterval)
		self.timer = QtCore.QTimer(self, interval=timerInterval * 25, timeout=self.Run)

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
		self.playButton.setIcon(QIcon("Icons\play-icon.png"))
		settingsToolbarLayout.addWidget(self.playButton)

		# Pause button
		self.pauseButton = QPushButton()
		self.pauseButton.setIcon(QIcon("Icons\pause-icon.png"))
		settingsToolbarLayout.addWidget(self.pauseButton)


		settingsToolbar.addWidget(settingsToolbarWidget)

		
	def Home(self):
		self.SettingsToolBar()

		createCentralWidget = QWidget()
		centralWidgetLayout = QVBoxLayout()
		createCentralWidget.setLayout(centralWidgetLayout)
		
		# Creates the GraphicDisplay widget
		self.TextGraphicDisplay()

		# Adds the GraphicDisplay widget to central widget layout
		centralWidgetLayout.addWidget(self.GraphicsView)
		
		# Progress Bar
		self.progBarVal = 0
		self.progBarMax = 250

		self.progressBar = QProgressBar()
		self.progressBar.setFixedHeight(20)
		self.progressBar.setMaximum(self.progBarMax)
		centralWidgetLayout.addWidget(self.progressBar) 
		
		
		self.setCentralWidget(createCentralWidget)

		self.playButton.clicked.connect(self.playButtonPressed)
		self.pauseButton.clicked.connect(self.pauseButtonPressed)
		#self.playPauseButton.clicked.connect(self.Run)

		print(self.playPauseBttnState)

	@QtCore.pyqtSlot()
	def playButtonPressed(self):
		#self.timer = 0
		QtCore.QTimer.singleShot(0, self.Run)
		self.timer.start()

	@QtCore.pyqtSlot()
	def pauseButtonPressed(self):
		self.timer.stop()

	def Run(self):
		#print(self.delayInput.text())

		self.progBarVal += 1
		self.progressBar.setValue(int(self.progBarVal))

		if self.progBarVal == self.progBarMax:
			self.progBarVal = 0

			self.UpdateGDText()
		
		
	def TextGraphicDisplay(self):
		self.scene = QGraphicsScene()

		displayString = self.R.randomStr()
		text = displayString

		displayFont = QFont("Atkinson Hyperlegible", 150)
		displayFont.setBold(True)
		self.textObject = self.scene.addSimpleText(text, displayFont)
		#addText(text, displayFont)

		self.GraphicsView = QGraphicsView(self.scene, self)
		#GraphicsView.setGeometry(0,0,600,500)

	def UpdateGDText(self, displayString="Error: could not load display element"):
		displayString = self.R.randomStr()
		#print(displayString)
		self.textObject.setText(displayString)


class Randomizer():

	def __init__(self, items) -> None:
		self.delay = 1.75
		# Delay in seconds
		self.items = items
		self._testStr = "Test string"

	def randomStr(self):			
		itemsKey = r.randint(1,26)
		a = self.items[itemsKey]
			
		return a
		
	def gdUpdateTextObject(self, window):
		text = self.randomStr()

		window.scene.clear()

		displayFont = QFont("Atkinson Hyperlegible", 60)
		displayFont.setBold(True)
		textObject = window.scene.addText(text, displayFont)



if __name__ == "__main__":
	# Start PyQt application
	app = QApplication(sys.argv)
	
	window = Window()
	window.show()

	sys.exit(app.exec())