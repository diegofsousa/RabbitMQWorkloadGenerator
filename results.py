from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys
import random

class Results(QDialog):
	def __init__(self, listOfMeanAmosts, listOfVarianceAmosts, listOfStandartDeviation, parent=None):
		super(Results, self).__init__(parent)

		self.listOfMeanAmosts = listOfMeanAmosts
		self.listOfVarianceAmosts = listOfVarianceAmosts
		self.listOfStandartDeviation = listOfStandartDeviation

		self.setWindowTitle("Results - RabbitMQ Workload Generator")

		# For Mean
		self.figureMean = Figure()
		self.canvasMean = FigureCanvas(self.figureMean)

		# For Variance
		self.figureVariance = Figure()
		self.canvasVariance = FigureCanvas(self.figureVariance)

		# For SDeviation
		# self.figureSDeviation = Figure()
		# self.canvasSDeviation = FigureCanvas(self.figureSDeviation)

		lblTitle = QLabel("<center><h3>Results of the experiment:</h3></center>")

		lblMean = QLabel("The average sample time is to quantify the\n performance of the message queue.\n The X-axis represents the messages\n while Y represents the time in microseconds.")
		lblVariance = QLabel("The variance is also adequate for 30 times\n and is calculated based on the mean. So\n is the standard deviation. The X-axis represents\n the messages while Y represents the time in\n microseconds.")
		# lblSDeviation = QLabel("The average sample time is to quantify\n the performance of the message queue.\n The X-axis represents the messages\n while Y represents the time in microseconds.")

		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox3 = QHBoxLayout()

		hbox1.addWidget(self.canvasMean)
		hbox1.addWidget(lblMean)
		self.plotMean()

		hbox2.addWidget(self.canvasVariance)
		hbox2.addWidget(lblVariance)
		self.plotVarianceSD()

		btnExit = QPushButton("Back to experiment")
		btnSavePDF = QPushButton("Save as PDF!")
		hbox3.addWidget(btnExit)
		hbox3.addWidget(btnSavePDF)

		totalbox = QVBoxLayout()
		totalbox.addWidget(lblTitle)
		totalbox.addLayout(hbox1)
		totalbox.addLayout(hbox2)
		totalbox.addLayout(hbox3)
		# totalbox.addLayout(hbox3)
		self.setLayout(totalbox)

		self.connect(btnExit, SIGNAL("clicked()"), SLOT("reject()"))

		self.setGeometry(300,100,1000,700)

	def plotMean(self):
		''' plot some random stuff '''
		N = len(self.listOfMeanAmosts)
		x = range(1,len(self.listOfMeanAmosts)+1)
		width = 1/1.1
		z = [i * 1.2 for i in self.listOfMeanAmosts]
		plt = self.figureMean.add_subplot(111)

		plt.bar(x, self.listOfMeanAmosts, width, color="c")
		plt.grid(True)
		plt.set_title("Mean Time of The Samples 30 Times Repeated")
		#plt.set_xlabel("Messages")
		#plt.set_ylabel("Time (microseconds)")
		self.canvasMean.draw()

	def plotVarianceSD(self):
		''' plot some random stuff '''
		plt = self.figureVariance.add_subplot(111)

		#plt.bar(x, self.listOfVarianceAmosts, width, color="g")
		a, = plt.plot(self.listOfVarianceAmosts, label='Variance', linestyle='--')
		b, = plt.plot(self.listOfStandartDeviation, label='Standart Deviation', linestyle='-.')
		plt.legend([a, b],["Variance", "Standart Deviation"])
		plt.grid(True)
		plt.set_title("Variance Time of The Samples 30 Times Repeated")
		#plt.set_xlabel("Messages")
		#plt.set_ylabel("Time (microseconds)")
		#plt.legend((a,b), ("Variance", "Standart Deviation"), 'upper left')
		self.canvasVariance.draw()