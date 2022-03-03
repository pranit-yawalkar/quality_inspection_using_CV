import serial
import time

serialComm = serial.Serial("COM5", 9600)
serialComm.timeout = 1

while True:
    i = input("input (on/off): ").strip()
    if i == "done":
        print("Program Finished...")
        break
    serialComm.write(i.encode())
    time.sleep(0.5)
    print(serialComm.readline().decode("ascii"))

serialComm.close()