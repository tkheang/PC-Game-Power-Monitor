import psutil
import time
import os
import asyncio
import kasa
from dotenv import load_dotenv

def measureWatts(plug):
    plug.update()
    emeter = plug.emeter_realtime()
    # Power is in watts
    power = emeter["power"]
    return power

def main():
    load_dotenv()
    
    # Try to connect to Kasa smart plug
    try:
        deviceIP = os.getenv("deviceIP")
        plug = kasa.SmartPlug(deviceIP)
        if plug.is_on:
            print("Smart plug found!")
    except:
        print("Smart plug not found!")
        exit()

    # Program to monitor
    program = "AcroRd32.exe"
    found = False

    if input("Scan for program?: y/n ") == "y":
        print("Scanning...")
        while found == False:
                if program in (p.name() for p in psutil.process_iter()):
                    startTime = time.time()
                    found = True
                    print("Program found!")
                else:
                    print("Still scanning...")
                    time.sleep(1)
    else:
        exit()

    while found == True:
        # Exit when program has stopped running
        if program not in (p.name() for p in psutil.process_iter()):
            endTime = time.time()
            found = False
            print("Program has stopped running")
        else:
            print("Program is still running...")
            currentPower = measureWatts(plug)
            totalConsumption += currentPower
            count += 1
            print("Current power consumption: " + currentPower + " watts")
            time.sleep(1)

    totalConsumption = totalConsumption / count
    runTime = endTime - startTime

    print("Program has run for " + str(runTime) + " seconds")
    print("Average power consumed during runtime: " + totalConsumption + " watts")

if __name__== "__main__":
  main()