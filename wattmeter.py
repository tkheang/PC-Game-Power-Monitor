import win32ui
import time
import os
import asyncio

from kasa import SmartPlug
from dotenv import load_dotenv

def WindowExists(name):
    try:
        win32ui.FindWindow(None, name)
    except win32ui.error:
        return False
    else:
        return True

async def measurePower(plug):
    await plug.update()
    pstat = plug.emeter_realtime
    # Power is in watts
    return pstat["power_mw"] / 1000

async def main():
    # Try to connect to Kasa smart plug
    load_dotenv()
    plug = SmartPlug(os.getenv("deviceIP"))
    try:
        await plug.update()
        if plug.is_on:
            print("Smart plug found!")
    except:
        print("Smart plug not found! Plug into wall or check .env settings")
        exit()
    
    # Detect program to monitor
    program = input("Program to monitor: ")
    found = False
    totalPower = 0.0
    count = 0
    while found == False:
        if WindowExists(program):
            found = True
            startTime = time.time()
            print(program + " is running. Tracking power usage...")
        else:
            print("Program " + program + " not found! Exiting...")
            exit()

    # Accumulate total power every second
    while found == True:
        if WindowExists(program) == False:
            found = False
            endTime = time.time()
            print(program + " has stopped running")
        else:
            totalPower += await measurePower(plug)
            count += 1
            time.sleep(1)
    
    # Calculate power used
    runTime = endTime - startTime
    avgPower = totalPower / count
    totalEnergy = avgPower / 3600000
    print(program + " ran for " + str(runTime) + " seconds")
    print("Average power consumed: " + str(avgPower) + " W")
    print("Total energy consumed: " + str(totalEnergy) + " kWh")
    print("Total energy cost: $" + str(totalEnergy * 0.22))
    print("Total energy cost per month: $" + str(totalEnergy * 0.22 * 30))

if __name__ == "__main__":
    asyncio.run(main())