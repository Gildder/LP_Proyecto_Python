from Escenario import *
from Jugador import*
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
from PyQt4 import QtCore
import sys
import math

class EstadosPuente:
	Subido=1
	Bajando=2
	Bajado=3


class EscenarioUno(Escenario):

	def __init__(self,*args):
		Escenario.__init__(self,*args)
		self.theta=45
		self.ganar=True
		self.mover=True
		self.caer=False
		self.hilop=HiloPuente(self)
		self.hiloC=HiloCaida(self)
		self.estadoPuente=EstadosPuente.Subido 
		self.jugador=Jugador(40,500,Qt.white,5)
		self.hiloj=HiloCaida(self)
		self.setWindowTitle("Escenario Uno")
		
	def paintEvent(self, event):       
		factRad= math.pi/180 #factor de conversion de grados a radianes
		corxPuente=250*math.cos(self.theta*factRad) #coordenada de la punta del puente
		coryPuente=250*math.sin(self.theta*factRad)
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		imagen=QImage("esc1","png")
		center=QPoint(0,0)
		paint.drawImage(center,imagen)
		pen =QPen (Qt.blue, 10,Qt.SolidLine)
		paint.setPen(pen)
		paint.drawLine(650,520,650+corxPuente,520-coryPuente)
		self.pintarJugador(paint)
		paint.end()
		
	def pintarJugador(self,painter):
		center=QPoint(self.jugador.getPosX(),self.jugador.getPosY())
		pen=QPen(Qt.blue,2,Qt.SolidLine)
		painter.setPen(pen)
		painter.setBrush(self.jugador.getColor())
		radio=self.jugador.getRadio()
		painter.drawEllipse(center,radio,radio)
	
	def setAngle(self,angulo):
		self.theta=angulo
		self.repaint()
		
	def keyPressEvent(self,e):
		if self.mover and e.key()==QtCore.Qt.Key_Right:
			self.trasladarJugador()
			if self.mover:
				print("llamada a repaint")
				self.repaint()
		
		elif self.mover and e.key()==QtCore.Qt.Key_Left:
			self.jugador.retroceder()
			self.repaint()
		
		elif self.mover and e.key()==Qt.Key_Enter:
			self.bajarPuente()
			
	def bajarPuente(self):
		if (self.estadoPuente==EstadosPuente.Subido):
			self.hilop.start()
			self.estadoPuente=EstadosPuente.Bajado
		
		
	def trasladarJugador(self):
		x=self.jugador.getPosX()
		# si la posicion X es mayor que 400 llega al abismo
		# ademas si el puente no esta bajado, el jugador caera
		if x>=400 and not self.estadoPuente==EstadosPuente.Bajado:
			self.mover=False
			self.caer=True
			# ejecuta el hilo de caida
			self.hiloC.start()
			self.ganar=False
		else:
			self.jugador.avanzar()
			
class HiloPuente(Thread):
	#clase que sirve para descender el puente

	def __init__(self,Escenario):
		Thread.__init__(self)
		self.escenario=Escenario
	
	def run(self):
		angulo=45
		self.escenario.estadoPuente=EstadosPuente.Bajando
		self.escenario.mover=False
		while True:
			angulo+=16.85
			if (angulo<=180):
				self.escenario.setAngle(angulo)
				sleep(0.5)
			else:
				self.escenario.mover=True
				self.escenario.estadoPuente=EstadosPuente.Bajado
				break
						
class HiloCaida(Thread):
	
	def __init__(self,esc):
		Thread.__init__(self)
		self.escenario=esc
		
	def run(self):
		self.escenario.mover=False
		yo= self.escenario.jugador.getPosY()
		xo= self.escenario.jugador.getPosX()
		y=0
		t=0
		while True:
			if (y<=690):
				xo=xo+15
				y=yo+9.8*t
				t+=4
				self.escenario.jugador.setPosY(y)
				self.escenario.jugador.setPosX(xo)
				print(y,xo)
				self.escenario.repaint()
				sleep(0.25)
			else:
				break
				
app = QApplication(sys.argv)
nivel1 = EscenarioUno()
nivel1.show()
app.exec_()