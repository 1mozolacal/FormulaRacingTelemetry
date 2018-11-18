import serial
import csv
import datetime

running = True
errorcount = 0
timestamps = []
oil = []
coolant = []

def append_data(data):
        timestamps.append(int(data[0]))
        oil.append(float(data[1]))
        coolant.append(float(data[2]))

#transfer of 9600 bits per second and timeout added to wait for data to collect 
#before printing
ser = serial.Serial('COM4',baudrate = 9600, timeout = 1)

with open('data.csv', 'a', newline='') as file:
        #one time setups
        adata = csv.writer(file)
        adata.writerow([datetime.datetime.now()])
        
        while running:
                a_data = ser.readline()
                #change bytes to string text format:utf-8
                anew_data = a_data.decode('utf-8')
                #remove any spaces,newlines and other radnom characters
                anew_data = anew_data.strip()
                #split the string into three and store 
                #each data into its dedicated variable
                plotdata = anew_data.split(',')

                #testing
                print(plotdata)
                #print(len(plotdata))

                if len(plotdata) != 3:
                        errorcount += 1
                else:
                        #append to csv files with dates for each run
                        #print(str(plotdata[0]))
                        # only save timestamp to file
                        adata.writerow(plotdata)

                        append_data(plotdata)

                        # PLOT DATA HERE IN REAL-TIME

                        if float(plotdata[1]) > 80.0:
                                print("error")
