import mraa
import time
import threading
from datetime import datetime, timedelta
import socket

DELAY = 2
PWM_PIN = 5
RELE_PIN = 7
BUTTON_PIN = 8
SENSORA0_PIN = 0
SENSORA1_PIN = 1                  
x = mraa.I2c(0)
x.address(0x08)

HOST = '192.168.1.101'     # Endereco IP do Servidor
PORT = 6000            		# Porta que o Servidor esta

def sendCont(host, port, contg, contp):
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (host, port)
	tcp.connect(dest)
	msg = "ContG  =  " +  str(contg)  + "ContP  = " + str(contp) + "\n"
	tcp.send (msg)
	tcp.close()

def allSeconds():
        now = datetime.now()
        hours = now.strftime("%H")
        minute  = now.strftime("%M")
        Seconds = now.strftime("%S")
        return (int(hours)*3600) + (int(minute)*60) + int(Seconds)

def servo90():
	pwm.write(0.05)
	time.sleep(2.5)
	


pwm = mraa.Pwm(PWM_PIN) 			# Criada instancia da geracao do pwm
pwm.period_us(20000)                    			# Definindo o periodo do pwm em microsegundos
pwm.enable(True)                        			# Habilitando o funcionamento do pwm
button = mraa.Gpio(BUTTON_PIN)    	#criando instancia para gpio
rele   = mraa.Gpio(RELE_PIN)            		#criando instancia para gpio
button.dir(mraa.DIR_IN)                			# Definindo pino do gpio como saida
rele.dir(mraa.DIR_OUT)                   			# Definindo pino do gpio como entrada
sensorG  = mraa.Aio(SENSORA0_PIN)	#criada instancia do conversor AD
sensorP  = mraa.Aio(SENSORA1_PIN)	#criada instancia do conversor AD
contG = 0
contP = 0
s = threading.Thread(target=servo90, args=())
t = threading.Thread(target=sendCont, args=(HOST, PORT, contG, contP))
while True:
	x.writeByte(contG)
        x.writeByte(contP)
        x.writeByte(1)   
    	while(button.read() == 1):
        	rele.write(1)
        	if(sensorG.read()>500 and not s.isAlive()):
                	contG+=1
			x.writeByte(contG)
			x.writeByte(contP)
			x.writeByte(1)
			s = threading.Thread(target=servo90, args=())
			s.start()
			t = threading.Thread(target=sendCont, args=(HOST, PORT, contG, contP))
			t.start()
        	elif(sensorG.read() < 500):
                	if(not s.isAlive()):
				pwm.write(0.1)
			
        	if(sensorP.read()>500):
                	contP+=1
			x.writeByte(contG)
                        x.writeByte(contP)
			x.writeByte(1)
			time.sleep(0.5)
			t = threading.Thread(target=sendCont, args=(HOST, PORT, contG, contP))
			t.start()

		
	
	while(button.read() == 0):
		rele.write(0)
		contG = 0
		contP = 0
		x.writeByte(contG)
                x.writeByte(contP)
                x.writeByte(0)
