# ASL Finger Spelling Practice

import random as r
import sys, time

from PyQt6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QPushButton, QLabel, QTabWidget,
	QProgressBar, QLineEdit, QVBoxLayout, QGridLayout, QMdiArea, QGraphicsScene, QGraphicsView
)
from PyQt6 import QtGui
from PyQt6.QtCore import (Qt, QUrl)
from PyQt6.QtGui import (QIcon, QFont, QGuiApplication, QColor)


class Window(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("ASL Practice")
		# Set window Icon (Currently placeholder)
		self.setWindowIcon(QIcon("icon.jpeg"))
		self.setContentsMargins(5, 5, 5, 5)
		self.resize(500,500)
		
		# Mainwindow layout setup
		self.UI()
		
	def UI(self):
		createCentralWidget = QWidget()
		centralWidgetLayout = QVBoxLayout()

		tabBar = QTabWidget()
		self.setMenuWidget(tabBar)
		
		self.createGraphicDisplay()
		# Creates the GraphicDisplay widget

		centralWidgetLayout.addWidget(self.GraphicsView)
		# Adds the GraphicDisplay widget to central widget layout

		# Progress Bar
		progressBar = QProgressBar()
		progressBar.setFixedHeight(20)
		centralWidgetLayout.addWidget(progressBar)
		
		createCentralWidget.setLayout(centralWidgetLayout)
		self.setCentralWidget(createCentralWidget)
		
		button = QPushButton("Load")
		button2 = QPushButton("Test Button 2")
		

		tabBar.addTab(button, "File")
		tabBar.addTab(button2, "Menu")
		
	def createGraphicDisplay(self):
		self.scene = QGraphicsScene()

		self.gdCreateTextObject()

		self.GraphicsView = QGraphicsView(self.scene, self)
		#GraphicsView.setGeometry(0,0,600,500)

	def gdCreateTextObject(self, displayString="Error"):
		self.text = displayString

		displayFont = QFont("Atkinson Hyperlegible", 60)
		displayFont.setBold(True)
		textObject = self.scene.addText(self.text, displayFont)


class DisplayRandomizer():

	def __init__(self, items) -> None:
		self.delay = 1.75
		# Delay in seconds
		self.items = items
		self._testStr = "Test string"

	def randomStr(self):

		time.sleep(self.delay)
			
		itemsKey = r.randint(1,26)
		a = self.items[itemsKey]
			
		return a
		
	def gdUpdateTextObject(self, window):
		text = self.randomStr()

		window.scene.clear()

		displayFont = QFont("Atkinson Hyperlegible", 60)
		displayFont.setBold(True)
		textObject = window.scene.addText(text, displayFont)


def main(window):
	lettersDict = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J", 11:"K", 12:"L", 13:"M", 14:"N", 
		   			15:"O", 16:"P", 17:"Q", 18:"R", 19:"S", 20:"T", 21:"U", 22:"V", 23:"W", 24:"X", 25:"Y", 26:"Z"}


	R = DisplayRandomizer(lettersDict)

	#window.gdCreateTextObject(R._testStr)
	for _ in range(3):
		R.gdUpdateTextObject(window)


if __name__ == "__main__":
	# Start PyQt application
	app = QApplication(sys.argv)
	
	window = Window()
	window.show()

	main(window)

	sys.exit(app.exec())