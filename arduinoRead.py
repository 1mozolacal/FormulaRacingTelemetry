#imports
import threading
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import datetime
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

print("Program Starting...")


#Parse config file
def readConfigFile():
    configSettings = {}#return this dict
    configFile = open("config.txt", "r")#opens config file

    #region Communication port settings
    comPortRAW = configFile.readline()
    comPortEqualLoc = comPortRAW.find("=")#gets the locaiton of the equal sign
    if(comPortEqualLoc == -1 or comPortEqualLoc >= len(comPortRAW)-2):#2 instead of a 1 because of the new line character
        print("Error in the com port setting")
        print("closing in 10 sec")
        time.sleep(10)#So they can see the print
        exit()
    comPort = comPortRAW[int(comPortEqualLoc+1):int(len(comPortRAW)-1)]#takes all the character after the equals sign(-1 to get rid of the newline character)
    configSettings["comPort"] = comPort
    #endregion


    namesLineArray = configFile.readline().split(";")  # gets array
    namesLineDict = {}  # Kinda of like an enum for the different values
    for i in range(0, len(namesLineArray), 2):
        namesLineDict[int(namesLineArray[i + 1])] = namesLineArray[i]  # the number is the key string is the value

    dataSelected = configFile.readline()
    dataSelected = dataSelected[6:len(dataSelected)]#removes the "graph=" part
    dataSelectedArray = dataSelected.replace(" ","").split(',')
    for i in range(0,len(dataSelectedArray)):#converts the array of strings to integers
        dataSelectedArray[i] = int(dataSelectedArray[i])

    #the number of different things that can customize a dataset(in the future there will be ranges and so on)
    differentDataFeatures = 2
    #0 = (int) the number
    #1 = (String) the name
    dataConfigArray =  [[None for x in range(differentDataFeatures)] for y in range(len(dataSelectedArray))] # when calling[Which type of data][the feature]
    # note make a default one to replace if a None value is found

    for i in range(0,len(dataSelectedArray)):
        dataConfigArray[i][0] = dataSelectedArray[i]#the number
        dataConfigArray[i][1] = namesLineDict[dataSelectedArray[i]]#the name



    configSettings["dataConfig"] = dataConfigArray

    return configSettings#returns the varible inputed by a

systemVar = readConfigFile()#a dict of user inputed varibles

cmap = ListedColormap(['#affc67','r'])
boundMax = 100;
boundWarning = 50;
norm = BoundaryNorm([0,0,boundWarning,boundMax], cmap.N)

now = datetime.datetime.now()#gets current time
timeLable = now.strftime("%F %T")#converts time to string
timeLable = timeLable.replace(":",".")#remove ":" (this throw errors)
file = open("SavedData/Data-" + timeLable+".txt", "a")#make a file for writing saved data into

#set up pyplot varible
fig = plt.figure()
axl = fig.add_subplot(1,1,1)

#arrays for inputing data from sensor
xData, yData = [],[]#array to be filled by the reading tread
colour = []
#update function is called by the animate function for the graph
def update(i):
    if(not len(xData)>1):#there need to be aleast two data points inorder to make a line
        return;

    points = np.array([xData, yData]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    spilter = np.asarray(yData)
    lc.set_array(spilter)
    plt.gca().add_collection(lc)
    plt.xlim(0, xData[-1])
    plt.ylim(0, 100)
    '''
    axl.clear()#clears old graphed stuff
    axl.scatter(xData, yData, c=colour)#plot new data
    last = xData[len(xData)-1]#get the last time
    if (last> 2000):#if you should start scrolling
        a, b, c, d = plt.axis()#get axis
        plt.axis([last - 2000, last, c, d])#keep y axis the same but shifts the x axis
    '''

#a tread to constantly read the serial data
def Task1(ser,x,y,col):

    while 1:#while loop to allows read the serial input
        b = ser.readline().decode("utf-8")#readline(make sure that there is infact a \n char otherwise this won't end)
        parts = b.split(',')#splits by a ','
        #print(b)
        try:#trys to parse data(sometimes at the begining there isn't a full line
            val = float(parts[1])
            x.append(int(parts[0]))#time
            y.append(val)#value
            if(val>60):
                col.append(1)
            else:
                col.append(-1)
            file.write(b)#I am not including \n because b has a new line character
        except:
            print("ERROR on data convert: either missing data or not int/float data")
        #time.sleep(1)


def Main():
    ser = serial.Serial(systemVar["comPort"])#open and Arduino serial
    time.sleep(1)
    ser.flushInput()#Ensure the stored input is emptyed(will sometime contain infomation from last run)
    time.sleep(1)
    t1 = threading.Thread(target = Task1, args=[ser,xData,yData,colour])#make the serial reading thread
    #print ("Starting Thread 1")
    t1.start()#start the serial reading tread
    an = ani.FuncAnimation(fig, update, interval=200)#sets up the animate function for the graph

    plt.show()#make the graph visable
    #print( "=== exiting ===")


if __name__ == '__main__':#ensures that the programing is being run not just called
    Main()#run the main setup