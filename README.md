# PC Game Power Monitor
A simple program that tracks the energy usage and cost per gaming session. Developed as a submission for HackUCI 2021.  

**Required Hardware**  
TP-Link Kasa smart plug with energy monitoring (must be compatible with python-kasa). I used the [KP-115](https://www.kasasmart.com/us/products/smart-plugs/kasa-smart-plug-slim-energy-monitoring-kp115).  

**Required Libaries**  
[python-kasa](https://github.com/python-kasa/python-kasa)  
[pywin32](https://github.com/mhammond/pywin32)  
numpy  
matplotlib  
dotenv  

**Usage**  
Plug in and set up the smart plug as per the instructions. Create an .env file in the same directory as wattmeter.py and add the line: deviceIP = "YOUR SMART PLUG IP HERE" (place the smart plug's IP address inside the quotes). Start the program and enter the exact name of the game's window you want to monitor. Launch the game and the program should detect it and begin logging data. Upon game exit, the program will calculate the total game time, average power, average energy, energy cost, and equivalent CO2 emissions.  
