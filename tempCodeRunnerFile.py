load_dotenv()
deviceIP = os.getenv("deviceIP")

# Try to connect to Kasa smart plug
try:
    plug = SmartPlug(deviceIP)
    """ if plug.is_on == True:
        print("Smart plug found!") """
except:
    print("Smart plug not found!")
    exit()

# Program to monitor
program = "AcroRd32.exe"
found = False

# Detect if program is running
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

# Exit when program has stopped running
while found == True:
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

# Calculate total power consumption
totalConsumption = totalConsumption / count
runTime = endTime - startTime

print("Program has run for " + str(runTime) + " seconds")
print("Average power consumed during runtime: " + totalConsumption + " watts")