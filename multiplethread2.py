class myThreadGPS (threading.Thread):
    def __init__(self, ser, start_event, end_event, pos):
        threading.Thread.__init__(self)
        self.ser = ser
        self.start_event = start_event
        self.end_event = end_event
        self.pos = pos
    def run(self):
        self.start_event.wait()
        self.start_event.clear()
        print "Starting GPS"
        self.pos[0] = gps.gps_getDataINF(self.ser)
        self.end_event.set()

class myThreadLAS (threading.Thread):
    def __init__(self, ser, start_event, end_event, dis):
        threading.Thread.__init__(self)
        self.ser = ser
        self.start_event = start_event
        self.end_event = end_event
        self.dis = dis
    def run(self):
        self.start_event.wait()
        self.start_event.clear()
        print "Starting Laser"
        self.dis[0] = laser.lrf_getDistanceINF(self.ser)
        self.end_event.set()

#Declare the used events
gps_end_event = threading.Event()
laser_end_event = threading.Event()
gps_start_event = threading.Event()
laser_start_event = threading.Event()
#Initialize shared variables
pos = [None]
dis = [None]
# Create new threads
thread1 = myThreadGPS(gpsSerial, gps_start_event, gps_end_event, pos)
thread2 = myThreadLAS(laserSerial, laser_start_event, laser_end_event, dis)

# Start new Threads
thread1.start()
thread2.start()
#Start events initially set to True
gps_start_event.set()
laser_start_event.set()
while True:
    #Wait for both threads to end and reset them.
    gps_end_event.wait()
    gps_end_event.clear()
    laser_end_event.wait()
    laser_end_event.clear()
    #print the shared variables
    print pos[0]
    print dis[0]
    gps_start_event.set()
    laser_start_event.set()
