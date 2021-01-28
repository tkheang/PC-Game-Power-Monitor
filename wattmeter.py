import psutil
import time


found = False
startTime = 0.0
endTime = 0.0
runTime = 0.0

# Program to monitor
program = "AcroRd32.exe"

def measureWatts():
    return

start = input("Scan for program?: y/n ")
if start == "y":
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
        measureWatts()
        time.sleep(1)

runTime = endTime - startTime

print("Program has run for " + str(runTime) + " seconds")
print("Power consumed during runtime: ")