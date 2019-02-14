import serial
import time
import threading
import gps
import laser

#serial
def serialSensor(device, baudRate):
    ser = serial.Serial(
    port=device,
    baudrate=baudRate,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
    #timeout=0
    )
    return ser

#Device 1
gpsSerial = serialSensor("/dev/ttyUSB0",9600)

#Device 2
laserSerial = serialSensor("/dev/ttyUSB1",19200)

class myThreadGPS (threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
    def run(self):
        print "Starting GPS"
        gps.gps_getDataINF(self.ser)

class myThreadLAS (threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
    def run(self):
        print "Starting Laser"
        laser.lrf_getDistanceINF(self.ser)
# Create new threads
thread1 = myThreadGPS(gpsSerial)
thread2 = myThreadLAS(laserSerial)

# Start new Threads
thread1.start()
thread2.start()
