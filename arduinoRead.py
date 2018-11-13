import threading
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import datetime

now = datetime.datetime.now()
timeLable = now.strftime("%F %T")
timeLable = timeLable.replace(":",".")
file = open("SavedData/Data-" + timeLable+".txt", "a")

fig = plt.figure()
axl = fig.add_subplot(1,1,1)

xData, yData = [],[]#array to be filled by the reading tread

#updates
def update(i):
    axl.clear()
    axl.plot(xData, yData)
    last = xData[len(xData)-1]
    if (last> 2000):
        a, b, c, d = plt.axis()
        plt.axis([last - 2000, last, c, d])



def Task1(ser,x,y):

    while 1:
        b = ser.readline().decode("utf-8")
        parts = b.split(',')
        #print(b)
        try:
            x.append(int(parts[0]))
            y.append(float(parts[1]))
            file.write(b)#I am not including \n because b has a new line character
        except:
            print("ERROR on data convert: either missing data or not int/float data")
        #time.sleep(1)


def Main():
    ser = serial.Serial('COM3')
    time.sleep(1)
    ser.flushInput()
    time.sleep(1)
    t1 = threading.Thread(target = Task1, args=[ser,xData,yData])
    #print ("Starting Thread 1")
    t1.start()
    an = ani.FuncAnimation(fig, update, interval=200)

    plt.show()
    #print( "=== exiting ===")


if __name__ == '__main__':
    Main()