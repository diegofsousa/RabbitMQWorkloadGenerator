from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from architecture import Emitter, Receptor
from results import Results
from math import sqrt

class index(QDialog):
	def __init__(self, parent=None):
		super(index, self).__init__(parent)

		self.setWindowTitle("RabbitMQ Workload Generator")
		hbox1 = QHBoxLayout()
		hbox2 = QVBoxLayout()

		pixmap = QPixmap('rabbitimg.png')

		lbllogo = QLabel()
		lbllogo.setPixmap(pixmap)
		lblintrucoes = QLabel("<center><h3>INSTRUCTIONS:</h3></center>\n\n"
			+"1. Make sure that the <b>RabbitMQ</b> message queue is installed <br>and properly configured as a service;"
			+"<br>2. Verify that the queue is not being used at the time of the<br> experiments;"
			+"<br>3. Select the test parameters below and click on <b>'Run tests!'</b>.\n\n\n"
			+"<center><h3>ABOUT:</h3></center>\n\n"
			+"This software was developed by the team of graduates <br>Antonio S. V. C. Junior, Diego F. S. Lima, Vitorio S. A. Rocha<br> and is of free distribution in: <br> https://github.com/diegofsousa/RabbitMQWorkloadGenerator.")
		lblselecoes = QLabel("<center><h3>Workload Selections:</h3></center>")



		hbox1.addWidget(lbllogo)
		hbox1.addWidget(lblintrucoes)

		hboxselection = QHBoxLayout()
		labelQntChar = QLabel("Number of characters:")
		self.btnQntChar = QPushButton("Select...")
		self.btnQntChar.clicked.connect(self.getItemChars)
		labelQntMessages = QLabel("Number of messages:")
		self.btnQntMessages = QPushButton("Select...")
		self.btnQntReset = QPushButton("Reset configurations")
		self.btnQntMessages.clicked.connect(self.getItemMessages)
		hboxselection.addWidget(labelQntChar)
		hboxselection.addWidget(self.btnQntChar)
		hboxselection.addWidget(labelQntMessages)
		hboxselection.addWidget(self.btnQntMessages)
		hboxselection.addWidget(self.btnQntReset)

		hbox2.addWidget(lblselecoes)

		self.btnRunTests = QPushButton("Run tests!")

		totalbox = QVBoxLayout()
		totalbox.addLayout(hbox1)
		totalbox.addLayout(hbox2)
		totalbox.addLayout(hboxselection)
		totalbox.addWidget(self.btnRunTests)
		self.setLayout(totalbox)

		self.receptor = Receptor(None, None)
		self.connect(self.receptor, SIGNAL("again(QString)"), self.again)
		self.receptor.mysignal.connect(self.questionUser)
		#self.receptor.start()

		self.connect(self.btnRunTests, SIGNAL("clicked()"), self.runTests)
		self.connect(self.btnQntReset, SIGNAL("clicked()"), self.clearConfiguration)		

		self.setGeometry(300,100,700,400)

	def getItemChars(self):
		items = ("240 Characters","480 Characters", "960 Characters")

		item, ok = QInputDialog.getItem(self, "Select number of characters", 
		"Number of characters", items, 0, False)

		if ok and item:
			self.btnQntChar.setText(item)

	def getItemMessages(self):
		items = ("120 Messages", "240 Messages", "480 Messages", "960 Messages")

		item, ok = QInputDialog.getItem(self, "Select number of messages", 
		"Number of messages", items, 0, False)

		if ok and item:
			self.btnQntMessages.setText(item)

	def runTests(self):
		if self.btnQntChar.text() == "Select..." or self.btnQntMessages.text() == "Select...":
			msg = QMessageBox.information(self, "Entrada inválida!",
											"Alguns valores não foram selecionados.",
											 QMessageBox.Close)
		else:
			self.receptor.numCharacters = int(self.btnQntChar.text()[0:3])
			self.receptor.numMessages = int(self.btnQntMessages.text()[0:3])
			self.receptor.start()
			self.emitter = Emitter(int(self.btnQntChar.text()[0:3]), int(self.btnQntMessages.text()[0:3]))
			self.emitter.start()

	def again(self, numberIter):
		self.btnRunTests.setEnabled(False)
		self.btnRunTests.setText("Running tests... ({}/30)".format(numberIter))
		print("veio aqui")
		self.emitter.new()

	def questionUser(self, lista):
		resp = QMessageBox.question(None, "Show results?",
									 "Do you want to see the results of the experiments?",
									QMessageBox.Yes|QMessageBox.No)
		if resp == 16384:
			print("Mostrar resultados!")
			# print(lista)

			listOfMeanAmosts = []
			listOfVarianceAmosts = []
			listOfStandartDeviation = []

			# some algorithms
			for i in range(len(lista[0])):
				auxSum = 0
				for j in range(30):
					auxSum =+ lista[j][i]
				listOfMeanAmosts.append(auxSum/30)

			for i in range(len(lista[0])):
				auxSum = 0
				for j in range(30):
					auxSum =+ (lista[j][i] - listOfMeanAmosts[i]).total_seconds()**2
				listOfVarianceAmosts.append(auxSum/30)

			for i in range(len(lista[0])):
				listOfStandartDeviation.append(sqrt(listOfVarianceAmosts[i]))

			print(listOfMeanAmosts)
			print(listOfVarianceAmosts)
			print(listOfStandartDeviation)
			dlg = Results(listOfMeanAmosts, listOfVarianceAmosts, listOfStandartDeviation)
			dlg.exec_()

		else:
			self.clearConfiguration()

	def clearConfiguration(self):
		arq = open('receptores.txt', 'w')
		arq.write("")
		arq.close()
		self.receptor.lista.clear()
		self.receptor.totalList.clear()
		self.receptor.horarios.clear()
		self.receptor.count = 0
		self.receptor.arq = open('receptores.txt', 'a')
		self.btnRunTests.setEnabled(True)
		self.btnRunTests.setText("Run tests!")





app = QApplication(sys.argv)
dlg = index()
dlg.exec_()