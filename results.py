from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Results(QDialog):
	def __init__(self, listOfMeanAmosts, listOfVarianceAmosts, listOfStandartDeviation, parent=None):
		super(Results, self).__init__(parent)

		self.setWindowTitle("Results - RabbitMQ Workload Generator")

		self.setGeometry(300,100,700,400)
