from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import pika
from datetime import datetime

class Emitter(QThread):
	"""Thread-class responsible for publish topics"""
	def __init__(self, numCharacters, numMessages):
		self.numCharacters = numCharacters
		self.numMessages = numMessages
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel =  self.connection.channel()
		self.channel.queue_declare(queue='hello')

		QThread.__init__(self)

	def run(self):
		for x in range(self.numMessages):
			now = datetime.now()
			message = "{}, ID: {} - ".format(now.strftime("%Y/%m/%d - %H:%M:%S:%f"), x+1) + ((self.numCharacters - 30) * "A")
			self.channel.basic_publish(exchange='',
	                      routing_key='hello',
	                      body=message)
	def new(self):
		self.run()
		

class Receptor(QThread):
	"""Thread-class responsible for consuming topics"""
	mysignal = pyqtSignal(list)
	def __init__(self, numCharacters, numMessages):
		self.numCharacters = numCharacters
		self.numMessages = numMessages
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='hello')
		self.lista = []
		self.totalList = []
		self.horarios = []
		self.count = 0
		self.arq = open('logs/recept.data', 'a')

		QThread.__init__(self)

	def run(self):
		self.channel.basic_consume(self.callback,
                      queue='hello',
                      no_ack=True)
		self.channel.start_consuming()


	def callback(self, ch, method, properties, body):
		a = datetime.now()
		nowList = []
		self.horarios.append(a)
		self.lista.append(body.decode())
		if len(self.lista) == self.numMessages:
			self.arq.write("Results of {} iteration\n".format(self.count + 1))
			print("\n\nResults:\n")
			for i in range(len(self.lista)):
				a = datetime(int(self.lista[i][0:4]), int(self.lista[i][5:7]), int(self.lista[i][8:10]), int(self.lista[i][13:15]), int(self.lista[i][16:18]), int(self.lista[i][19:21]), int(self.lista[i][22:28]))
				info = "Message delay {}: {}".format(i+1, self.horarios[i] - a)
				self.arq.write(info + "\n")
				print(info)
				nowList.append(self.horarios[i]-a)
			self.arq.write("\n")
			
			if self.count < 30:
				self.totalList.append(nowList)
				self.lista.clear()
				self.horarios.clear()
				self.count += 1
				self.emit(SIGNAL("again(QString)"), str(self.count))
			else:
				self.arq.close()
				self.mysignal.emit(self.totalList)