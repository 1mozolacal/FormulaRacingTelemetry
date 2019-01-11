import serial
import csv
import datetime
import matplotlib.pyplot as plt

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
ser = serial.Serial('COM5',baudrate = 9600, timeout = 1)


        
while running:
        a_data = ser.readline().decode('utf-8')
                #change bytes to string text format:utf-8
                #remove any spaces,newlines and other radnom characters
        plotdata = a_data.strip().split(',')
                #split the string into three and store 
                #each data into its dedicated variable

        print(plotdata)