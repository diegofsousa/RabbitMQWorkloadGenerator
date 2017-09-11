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

c = canvas.Canvas('test.pdf')
c.setFont("Helvetica", 25)
c.drawString(120,790,"RabbitMQ Workload Generator")
c.setFont("Helvetica", 13)
c.drawString(90,750,"These were the results of the experiments carried out at {}.".format(datetime.now().strftime("%Y/%m/%d at %H:%M:%S")))
c.drawString(50, 735, "The experiments were performed under the parameters <> messages of <> characters ")
c.drawString(50, 720, "tested 30x.")
c.drawString(200, 680, "RESULTS OF THE EXPERIMENT:")
c.drawString(90, 640, "The average sample time is to quantify the performance of the message queue. ")
c.drawString(50, 625, "The X-axis represents the messages while Y represents the time in microseconds.")

seq00 = [0.889, 1.048, 1.12, 1.18, 1.249, 1.329, 1.459, 1.681, 1.917, 2.433, 2.653, 2.876, 3.075, 3.223,
       3.422, 3.621, 3.811, 4.032, 4.155, 4.37, 4.767, 4.987, 5.183, 5.388, 5.538, 5.719, 5.858, 5.93, 6.029,
       6.208]

N = len(seq00)
x = range(1,31)
width = 1/1.1
z = [i * 1.2 for i in seq00]
fig = plt.figure(figsize=(7, 4.5))
plt.bar(x, seq00, width, color="c")
#plt.plot(x, seq, color="black", marker=',', linestyle=':', linewidth=2)
plt.grid(True)
plt.ylim(0,10)
plt.plot([1], [1], 'o')
plt.plot([30], [6.2], 'o')
plt.annotate('0.889J', xy=(1, 1), xytext=(0.05, 1.5))
plt.annotate('6.208J', xy=(30, 6.2), xytext=(28.5, 6.5))
plt.title("Consumo de energia do app Spotify (Em primeiro plano)")
plt.xlabel("Observações")
plt.ylabel("Energia (Joules)")

imgdata = io.BytesIO()
fig.savefig(imgdata, format='png')
imgdata.seek(0)  # rewind the data

Image = ImageReader(imgdata)


c.drawImage(Image, 40,232,500, preserveAspectRatio=True,mask='auto')
c.drawString(90, 270, "The variance is also adequate for 30 times and is calculated based on the mean")
c.drawString(50, 255, "So is the standard deviation. The X-axis represents themessages while Y represents ")
c.drawString(50, 240, "the time in microseconds.")

c.save()