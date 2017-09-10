from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import pika
from datetime import datetime

class Emitter(QThread):
	"""docstring for Emitter"""
	def __init__(self, numCharacters, numMessages):
		self.numCharacters = numCharacters
		self.numMessages = numMessages
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel =  self.connection.channel()
		self.channel.queue_declare(queue='hello')

		QThread.__init__(self)

	def run(self):
		arq = open('emissores.txt', 'w')
		for x in range(self.numMessages):
			now = datetime.now()
			message = "{}, ID: {} - ".format(now.strftime("%Y/%m/%d - %H:%M:%S:%f"), x+1) + ((self.numCharacters - 30) * "A")
			self.channel.basic_publish(exchange='',
	                      routing_key='hello',
	                      body=message)
			arq.write(message+"\n")
		arq.close()

class Receptor(QThread):
	"""docstring for Receptor"""
	def __init__(self, numCharacters, numMessages):
		self.numCharacters = numCharacters
		self.numMessages = numMessages
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='hello')
		self.lista = []
		self.horarios = []
		self.arq = open('receptores.txt', 'w')

		QThread.__init__(self)

	def run(self):
		self.channel.basic_consume(self.callback,
                      queue='hello',
                      no_ack=True)
		self.channel.start_consuming()


	def callback(self, ch, method, properties, body):
		print(body.decode())

		a = datetime.now()
		self.horarios.append(a)
		self.arq.write(body.decode() + a.strftime(" - %Y/%m/%d - %H:%M:%S:%f\n"))
		self.lista.append(body.decode())
		if len(self.lista) == self.numMessages:
			self.arq.close()
			print("\n\nResultado:\n")
			for i in range(len(self.lista)):
				a = datetime(int(self.lista[i][0:4]), int(self.lista[i][5:7]), int(self.lista[i][8:10]), int(self.lista[i][13:15]), int(self.lista[i][16:18]), int(self.lista[i][19:21]), int(self.lista[i][22:28]))
				print("Atraso da mensagem {}: {}".format(i+1, self.horarios[i] - a))
				