# iRobot Class
from pycreate2 import Create2


class iRobot:
    def __init__(self):
        self.bot = None
        # Serial port name "ttyUSB0"
        self.port = "/dev/ttyUSB0"
        self.sensors = None
        self.enabledClass = False
        # Initialize the bot in full access mode
        self.start()

    def start(self):
        try:
            self.bot = Create2(port=self.port)
            self.bot.start()
            # No protection/safety in full mode
            self.bot.full()
            self.sensors = self.bot.get_sensors()
            self.enabledClass = True
        except:
            self.enabledClass = False
            return

# Public Methods

    # Inputs: speed = 0 - 1 (float)
    def moveForward(self, speed):
        if(self.enabledClass == False):
            return
        
        power = iRobot.speedToPower(self, speedToConvert=speed)
        self.bot.drive_direct(power, power)

    # Inputs: speed = 0 - 1 (float)
    def moveBackwards(self, speed):
        if(self.enabledClass == False):
            return
        power = iRobot.speedToPower(self, speedToConvert=speed)
        self.bot.drive_direct(-power, -power)

    # Inputs: speed = 0 - 1 (float)
    def turnLeft(self, speed):
        if(self.enabledClass == False):
            return
        power = iRobot.speedToPower(self, speedToConvert=speed)
        self.bot.drive_direct(-power, power)

    # Inputs: speed = 0 - 1 (float)
    def turnRight(self, speed):
        if(self.enabledClass == False):
            return
        power = iRobot.speedToPower(self, speedToConvert=speed)
        self.bot.drive_direct(power, -power)

    def moveStop(self):
        if(self.enabledClass == False):
            return
        self.bot.drive_stop()

    def get_sensors(self):
        if(self.enabledClass == False):
            return
        self.sensors = self.bot.get_sensors()

    def close(self):
        if(self.enabledClass == False):
            return
        self.bot.close()

# Private Methods
    # Inputs: speed = 0 - 1 (float)
    # Returns: power = -500 - 500 (int)
    def speedToPower(self, speedToConvert):
        return int(speedToConvert * 500)

    def printSensors(self):
        print('-'*70)
        print('{:>40} | {:<5}'.format('Sensor', 'Value'))
        print('-'*70)
        for k, v in self.sensors._asdict().items():
            print(f"{k}: {v}")
