#iRobot Class
from  pycreate2 import Create2

class IRobot:
    def __init__(self):
        self.bot = None
        # Serial port name "ttyUSB0"
        self.port = "/dev/ttyUSB0"
        self.sensors = None
        # Initialize the bot in full access mode
        self.start()
        # Ensure bot is stopped
        self.drive_stop()

    def start(self):
        self.bot = Create2(port=self.port)
        self.bot.start()
        # No protection/safety in full mode
        self.bot.full()
        self.sensors = self.bot.get_sensors()

    # Inputs: speed = 0 - 1 (float)
    def moveForward(self, speed):
        power = IRobot.speedToPower(speed)
        self.bot.drive_direct(power, power)

    # Inputs: speed = 0 - 1 (float)
    def moveBackwards(self, speed):
        power = IRobot.speedToPower(speed)
        self.bot.drive_direct(-power, -power)

    # Inputs: speed = 0 - 1 (float) 
    def turnLeft(self, speed):
        power = IRobot.speedToPower(speed)
        self.bot.drive_direct(-power, power)

    # Inputs: speed = 0 - 1 (float)
    def turnRight(self, speed):
        power = IRobot.speedToPower(speed)
        self.bot.drive_direct(power, -power)

    def moveStop(self):
        self.bot.drive_stop()

    def get_sensors(self):
        self.sensors = self.bot.get_sensors()

    def close(self):
        self.bot.close()

    # Inputs: speed = 0 - 1 (float)
    # Returns: power = -500 - 500 (int)
    def speedToPower(self, speed):
        return int(speed * 500)
    
    def printSensors(self):
        print('-'*70)
        print('{:>40} | {:<5}'.format('Sensor', 'Value'))
        print('-'*70)
        for k, v in self.sensors._asdict().items():
            print(f"{k}: {v}")
