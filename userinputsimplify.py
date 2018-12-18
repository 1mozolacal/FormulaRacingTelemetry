def user_input_simplification(number,dict,configFile):
    configFile = open("config.txt","r")
    for i in range(number):
        line_reading = configFile.readline()
        comport = line_reading.strip().split('=')
        print(comport[0])
        comportdict[comport[0]] = comport[1]
        print(comportdict)
user_input_simplification(1)
