#iRobotTestV0.1
# testing 1 2 3 
from  pycreate2 import Create2
import time

# PrettyPrint
def prettyPrint(sensors):
    print('-'*70)
    print('{:>40} | {:<5}'.format('Sensor', 'Value'))
    print('-'*70)
    for k, v in sensors._asdict().items():
        print(f"{k}: {v}")


# Port Name "ttyUSB0"
port = "/dev/ttyUSB0" 
bot = Create2(port)

# Start the Create 2
bot.start()

# Put the Create2 into 'safe' mode so we can drive it
# This will still provide some protection
#bot.safe()

# You are responsible for handling issues, no protection/safety in
# this mode ... becareful
bot.full()

# directly set the motor speeds ... move forward
bot.drive_direct(100, 100)
for i in range(10):
    time.sleep(0.2)
    sensors = bot.get_sensors()  # returns all data
    prettyPrint(sensors)

# turn in place
bot.drive_direct(200,-200)  # inputs for motors are +/- 500 max
time.sleep(0.2)
for i in range(10):
    time.sleep(0.2)
    sensors = bot.get_sensors()  # returns all data
    prettyPrint(sensors)

# directly set the motor speeds ... move forward
bot.drive_direct(100, 100)
for i in range(10):
    time.sleep(0.2)
    sensors = bot.get_sensors()  # returns all data
    prettyPrint(sensors)

# Stop the bot
bot.drive_stop()

# query some sensors
sensors = bot.get_sensors()  # returns all data
print(sensors.light_bumper_left)

# Close the connection
# bot.close()