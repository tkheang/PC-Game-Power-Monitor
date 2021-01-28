import psutil
import time

found = False
startTime = 0.0
endTime = 0.0

# Program to monitor
program = ""

def measureWatts():
    return

while found == False:
    start = input("Scan for program?: y/n ")
    if start == "y":
        if program in (p.name() for p in psutil.process_iter()):
            startTime = time.time()
            found = True
            print("Program is running")
        else:
            print("Program is not running")
    else:
        exit()

while found == True:
    if program not in (p.name() for p in psutil.process_iter()):
        endTime = time.time()
        found = False
        print("Program has stopped running")
    else:
        print("Program is still running...")
        measureWatts()
        time.sleep(1)

print("Program has run for " + str((endTime - startTime)) + " seconds")
print("Power consumed during runtime: ")