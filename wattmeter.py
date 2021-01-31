import win32ui
import time
import os
import asyncio

from numpy import arange
from datetime import timedelta
from matplotlib import pyplot as plt
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
    # Try to connect to TP-Link Kasa smart plug
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
    totalPower = 0.0
    timeout = 0
    sec = 0
    powerList = []
    timeList = []
    while(1):
        if WindowExists(program) == True:
            startTime = time.time()
            print(program + " is running. Tracking power usage...")
            break
        else:
            # Exit if program is not found in 15 retries
            print("Program " + program + " not found! Retrying...")
            timeout += 1
            time.sleep(1)
            if timeout > 14:
                print("Program " + program + " could not be found! Please try again.")
                exit()

    # Accumulate total power every second
    while(1):
        if WindowExists(program) == False:
            endTime = time.time()
            print(program + " has stopped running")
            break
        else:
            instPower = await measurePower(plug)
            totalPower += instPower
            sec += 1
            powerList.append(instPower)
            timeList.append(sec)
            time.sleep(1)
    
    # Calculate power used
    runTime = endTime - startTime
    avgPower = totalPower / sec
    # Energy in kWh
    energy = (avgPower / 1000) * (runTime / 3600)
    # $0.22 per kWh
    cost = energy * 0.22
    monthlyCost = cost * 30
    yearlyCost = cost * 365
    # Metric tons CO2
    monthlyCO2 = energy * 7.07e-4 * 30
    yearlyCO2 = energy * 7.07e-4 * 365

    # Print results
    print(f"{program} ran for " + str(timedelta(seconds = runTime)) + " (d:h:s:ms)")
    print(f"Average power consumed: {avgPower:0.02f} W")
    print(f"Total energy consumed: {energy:0.08f} kWh")
    print(f"Total energy cost: ${cost:0.8f}")
    print(f"Total energy cost per month: ${monthlyCost:0.08f}")
    print(f"Total energy cost per year: ${yearlyCost:0.08f}")
    print(f"Total equivalent CO2 emissions per month: {monthlyCO2:0.08f} metric tons")
    print(f"Total equivalent CO2 emissions per year: {yearlyCO2:0.08f} metric tons")

    # Print results in matplotlib
    plt.plot(timeList, powerList)
    plt.xticks(arange(0, timeList[-1], 60))
    plt.title("Power vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Power (watts)")
    plt.figtext(0.1, 0.26, f"{program} ran for " + str(timedelta(seconds = runTime)) + " (d:h:s:ms)", fontsize = 10, va = "top", ha = "left")
    plt.figtext(0.1, 0.23, f"Average power consumed: {avgPower:0.02f} W", fontsize = 10, va = "top", ha = "left")
    plt.figtext(0.1, 0.20, f"Total energy consumed: {energy:0.08f} kWh", fontsize = 10, va = "top", ha = "left")
    plt.figtext(0.1, 0.17, f"Total energy cost: ${cost:0.8f}", fontsize = 10, va = "top", ha = "left")
    plt.figtext(0.1, 0.14, f"Total energy cost per month: ${monthlyCost:0.08f}", fontsize = 10, va = "top", ha = "left")
    plt.figtext(0.1, 0.11, f"Total energy cost per year: ${yearlyCost:0.08f}", fontsize = 10, va = "top", ha = "left")
    plt.figtext(0.1, 0.08, f"Total equivalent CO2 emissions per month: {monthlyCO2:0.08f} metric tons", fontsize = 10, va = "top", ha = "left")
    plt.figtext(0.1, 0.05, f"Total equivalent CO2 emissions per year: {yearlyCO2:0.08f} metric tons", fontsize = 10, va = "top", ha = "left")
    plt.subplots_adjust(bottom = 0.3)
    plt.show()

if __name__ == "__main__":
    asyncio.run(main())