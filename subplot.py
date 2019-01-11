import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

running = True
timestamps = []
oil = []
coolant = []

#stores as float in lists (used to graph)
def append_data(data):
    if(data[0] != ''):
        if(data[1] != ''):
            if(data[2] != ''):
                timestamps.append(int(data[0])/1000.0)
                oil.append(float(data[1]))
                coolant.append(float(data[2]))

#transfer of 9600 bits per second and timeout added to wait for data to collect 
#before printing
ser = serial.Serial('COM5',baudrate = 9600, timeout = 1)
    
fig = plt.figure()
#(rows,columns,position)
userw1 = fig.add_subplot(2,1,1)
userw2 = fig.add_subplot(2,1,2)

def update(i):
    while running:
        a_data = ser.readline().decode('utf-8')
        plotdata = a_data.strip().split(',')
                    

        #print(plotdata)
        append_data(plotdata)
        print(timestamps)
            
    #userw1.clear()
    userw1.plot(timestamps,oil)
    #userw2.clear()
    userw2.plot(timestamps,coolant)

display = animation.FuncAnimation(fig,update,interval = 1000)
plt.show()