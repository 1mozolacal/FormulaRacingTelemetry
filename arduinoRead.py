#imports
import threading
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import datetime

#Parse config file
def readConfigFile():
    configSettings = {}#return this dict
    configFile = open("config.txt", "r")#opens config file
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



now = datetime.datetime.now()#gets current time
timeLable = now.strftime("%F %T")#converts time to string
timeLable = timeLable.replace(":",".")#remove ":" (this throw errors)
file = open("SavedData/Data-" + timeLable+".txt", "a")#make a file for writing saved data into

#set up pyplot varible
fig = plt.figure()
axl = fig.add_subplot(1,1,1)

#arrays for inputing data from sensor
xData, yData = [],[]#array to be filled by the reading tread

#update function is called by the animate function for the graph
def update(i):
    axl.clear()#clears old graphed stuff
    axl.plot(xData, yData)#plot new data
    last = xData[len(xData)-1]#get the last time
    if (last> 2000):#if you should start scrolling
        a, b, c, d = plt.axis()#get axis
        plt.axis([last - 2000, last, c, d])#keep y axis the same but shifts the x axis


#a tread to constantly read the serial data
def Task1(ser,x,y):

    while 1:#while loop to allows read the serial input
        b = ser.readline().decode("utf-8")#readline(make sure that there is infact a \n char otherwise this won't end)
        parts = b.split(',')#splits by a ','
        #print(b)
        try:#trys to parse data(sometimes at the begining there isn't a full line
            x.append(int(parts[0]))#time
            y.append(float(parts[1]))#value
            file.write(b)#I am not including \n because b has a new line character
        except:
            print("ERROR on data convert: either missing data or not int/float data")
        #time.sleep(1)


def Main():
    ser = serial.Serial('COM3')#open and Arduino serial
    time.sleep(1)
    ser.flushInput()#Ensure the stored input is emptyed(will sometime contain infomation from last run)
    time.sleep(1)
    t1 = threading.Thread(target = Task1, args=[ser,xData,yData])#make the serial reading thread
    #print ("Starting Thread 1")
    t1.start()#start the serial reading tread
    an = ani.FuncAnimation(fig, update, interval=200)#sets up the animate function for the graph

    plt.show()#make the graph visable
    #print( "=== exiting ===")


if __name__ == '__main__':#ensures that the programing is being run not just called
    Main()#run the main setup