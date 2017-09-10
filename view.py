from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

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
		self.btnQntMessages.clicked.connect(self.getItemMessages)
		hboxselection.addWidget(labelQntChar)
		hboxselection.addWidget(self.btnQntChar)
		hboxselection.addWidget(labelQntMessages)
		hboxselection.addWidget(self.btnQntMessages)

		hbox2.addWidget(lblselecoes)

		self.btnRunTests = QPushButton("Run tests!")

		totalbox = QVBoxLayout()
		totalbox.addLayout(hbox1)
		totalbox.addLayout(hbox2)
		totalbox.addLayout(hboxselection)
		totalbox.addWidget(self.btnRunTests)
		self.setLayout(totalbox)

		self.connect(self.btnRunTests, SIGNAL("clicked()"), self.runTests)

		self.setGeometry(300,100,700,400)

	def getItemChars(self):
		items = ("100 Characters", "200 Characters")

		item, ok = QInputDialog.getItem(self, "Select number of characters", 
		"Number of characters", items, 0, False)

		if ok and item:
			self.btnQntChar.setText(item)

	def getItemMessages(self):
		items = ("120 Messages", "240 Messages")

		item, ok = QInputDialog.getItem(self, "Select number of messages", 
		"Number of messages", items, 0, False)

		if ok and item:
			self.btnQntMessages.setText(item)

	def runTests(self):
		if self.btnQntChar.text() == "Select..." or self.btnQntMessages.text() == "Select...":
			print("Entrada inválida")
			msg = QMessageBox.information(self, "Entrada inválida!",
											"Alguns valores não foram selecionados.",
											 QMessageBox.Close)

app = QApplication(sys.argv)
dlg = index()
dlg.exec_()