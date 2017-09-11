import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
import io
from reportlab.lib.utils import ImageReader
from datetime import datetime
import webbrowser

def make_pdf(listOfMeanAmosts, listOfVarianceAmosts, listOfStandartDeviation, qtdChars, qtdMessages):
	"""Function that produces the report in PDF"""
	c = canvas.Canvas('logs/results.pdf')
	c.setFont("Helvetica", 25)
	Image = ImageReader("rabbitimg.png")
	c.drawImage(Image, 40,630,500, preserveAspectRatio=True,mask='auto')
	c.drawString(120,690,"RabbitMQ Workload Generator")
	c.setFont("Helvetica", 13)
	c.drawString(90,600,"These were the results of the experiments carried out at {}.".format(datetime.now().strftime("%Y/%m/%d at %H:%M:%S")))
	c.drawString(50, 585, "The experiments were performed under the parameters {} messages of {} characters".format(qtdMessages, qtdChars))
	c.drawString(50, 570, "tested 30x.")
	c.drawString(200, 525, "RESULTS OF THE EXPERIMENT:")
	c.drawString(90, 460, "The average sample time is to quantify the performance of the message queue. ")
	c.drawString(50, 445, "The X-axis represents the messages while Y represents the time in microseconds.")

	fig = plt.figure(figsize=(7, 4.5))
	a, = plt.plot(listOfMeanAmosts, label="Mean")
	plt.xlabel("Messages")
	plt.ylabel("Time (microseconds)")
	plt.annotate(str(listOfMeanAmosts[0])+"µs", xy=(1, listOfMeanAmosts[0]+0.3),
				 xytext=(0,listOfMeanAmosts[0]-0.6))
	plt.plot([0], [listOfMeanAmosts[0]], 'o', color='blue')
	plt.annotate(str(listOfMeanAmosts[-1])+"µs", xy=(len(listOfMeanAmosts)-1, listOfMeanAmosts[-1]+0.3),
				 xytext=(len(listOfMeanAmosts)-1,listOfMeanAmosts[-1]+0.3))
	plt.plot([len(listOfMeanAmosts)-1], [listOfMeanAmosts[-1]], 'o', color='blue')
	plt.title("Mean Time of The Samples 30 Times Repeated")
	plt.legend(handles=[a])
	plt.grid(True)

	imgdata = io.BytesIO()
	fig.savefig(imgdata, format='png')
	imgdata.seek(0)  # rewind the data

	Image = ImageReader(imgdata)


	c.drawImage(Image, 40,50,500, preserveAspectRatio=True,mask='auto')


	c.showPage()
	c.setFont("Helvetica", 13)

	c.drawString(90, 780, "The variance is also adequate for 30 times and is calculated based on the mean")
	c.drawString(50, 765, "So is the standard deviation. The X-axis represents themessages while Y represents ")
	c.drawString(50, 750, "the time in microseconds.")

	fig = plt.figure(figsize=(7, 4.5))
	a, = plt.plot(listOfVarianceAmosts, label="Variance", color="red")
	plt.xlabel("Messages")
	plt.ylabel("Time (microseconds)")
	plt.annotate(str(listOfVarianceAmosts[0])+"µs", xy=(1, listOfVarianceAmosts[0]+0.3),
				 xytext=(0,listOfVarianceAmosts[0]-0.6))
	plt.plot([0], [listOfVarianceAmosts[0]], 'o', color='red')
	plt.annotate(str(listOfVarianceAmosts[-1])+"µs", xy=(len(listOfVarianceAmosts)-1,
				 listOfVarianceAmosts[-1]+0.3), xytext=(len(listOfVarianceAmosts)-1,
				 listOfVarianceAmosts[-1]+0.3))
	plt.plot([len(listOfVarianceAmosts)-1], [listOfVarianceAmosts[-1]], 'o', color='red')
	plt.title("Variance Time of The Samples 30 Times Repeated")
	plt.legend(handles=[a])
	plt.grid(True)


	imgdata = io.BytesIO()
	fig.savefig(imgdata, format='png')
	imgdata.seek(0)  # rewind the data

	Image = ImageReader(imgdata)


	c.drawImage(Image, 40,365,500, preserveAspectRatio=True,mask='auto')

	c.drawString(90, 400, "The standard deviation is calculated according to the variance. For this case the ")
	c.drawString(50, 385, "same methodology as the previous representations is used.")


	fig = plt.figure(figsize=(7, 4.5))
	a, = plt.plot(listOfStandartDeviation, label="Standart Deviation", color="green")
	plt.xlabel("Messages")
	plt.ylabel("Time (microseconds)")
	plt.annotate(str(listOfStandartDeviation[0])+"µs", xy=(1, listOfStandartDeviation[0]+0.3),
				 xytext=(0,listOfStandartDeviation[0]-0.6))
	plt.plot([0], [listOfStandartDeviation[0]], 'o', color='green')
	plt.annotate(str(listOfStandartDeviation[-1])+"µs", xy=(len(listOfStandartDeviation)-1,
				 listOfStandartDeviation[-1]+0.3), xytext=(len(listOfStandartDeviation)-1,
				 listOfStandartDeviation[-1]+0.3))
	plt.plot([len(listOfStandartDeviation)-1], [listOfStandartDeviation[-1]], 'o', color='green')
	plt.title("Standart Deviation Time of The Samples 30 Times Repeated")
	plt.legend(handles=[a])
	plt.grid(True)

	imgdata = io.BytesIO()
	fig.savefig(imgdata, format='png')
	imgdata.seek(0)  # rewind the data

	Image = ImageReader(imgdata)


	c.drawImage(Image, 40,-10,500, preserveAspectRatio=True,mask='auto')
	c.setTitle("RabbitMQ Workload Generator")

	c.save()
	webbrowser.open("logs/results.pdf")