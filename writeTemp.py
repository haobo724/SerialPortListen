import csv
import time,os
import serial
import matplotlib.pyplot as plt
import threading,keyboard


import pandas as pd


a = pd.read_json()




def plot_temperature_data(filename):
    with open(filename,'r',newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        data = [[row[0], float(row[1])] for row in reader]
    print(data)

    x = [row[0] for row in data]
    y = [row[1] for row in data]

    plt.plot(x, y)
    plt.xlabel('time')
    plt.ylabel('temp')
    plt.title('temp-time')
    plt.show()
    
    
    
def read_from_serial(port,flag,baudrate=9600, timeout=0.5):
    ser = serial.Serial(port, baudrate, timeout=timeout)
    dataList = []
    saveName = 'temperature.csv'
    loop = True
    print('begin')
    ser.flushInput()
    while not flag.is_set():
        """ if keyboard.is_pressed('s'):
            print('Stopping...')
            loop = False
 """
        temp = ser.readline().decode('utf-8').rstrip()
        if temp =='':
            continue
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),temp)
        #time.sleep(0.5)

        dataList.append([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),temp])
    
        
        
    if not os.path.isfile(saveName):
        save_to_csv(saveName,dataList)
    else:
        save_to_csv(saveName,dataList,flag='a')

def save_to_csv(filename, data, flag='w'):
    with open(filename, flag, newline='') as csvfile:
        writer = csv.writer(csvfile)
        if flag == 'w':
            writer.writerow(['TimeStamp', 'temperature'])
        for row in data:
            writer.writerow(row)

def watchingthread(flag):
    keyboard.wait('s')
    print('Stopping...')
    stopEvent.set()

stopEvent = threading.Event()

thread = threading.Thread(target=read_from_serial, args=('COM3',stopEvent,))
thread2 = threading.Thread(target=watchingthread, args=(stopEvent,))
thread.start()
thread2.start()
thread.join()
thread2.join()

#ead_from_serial("COM3")

#plot_temperature_data(r'C:\Study\invandus\temploger\temperature.csv')
