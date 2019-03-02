import serial
import time


class MotorController:
    def __init__(self):
        # Open grbl serial port
        self.serial_instance = serial.Serial('/dev/ttyUSB3', 115200)

        # Wake up grbl
        self.serial_instance.write("\r\n\r\n")
        time.sleep(2)  # Wait for grbl to initialize
        self.serial_instance.flushInput()  # Flush startup text in serial input

        self.serial_instance.write("G90" + '\n')  # Send g-code block to grbl
        grbl_out = self.serial_instance.readline()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())

    def move_magnet(self, x, y, feedrate=100):
        """
        Move magnet to x, y location at feedrate
        :param x: loc to move
        :param y: loc to move
        :param feedrate: feedrate of move in mm/min
        :return:
        """
        # Stream g-code to grbl
        command_buffer = "G01 X{} Y{} F{}".format(x, y, feedrate)
        print('Sending: ' + command_buffer)
        self.serial_instance.write(command_buffer + '\n')  # Send g-code block to grbl
        grbl_out = self.serial_instance.readline()  # Wait for grbl response with carriage return
        print(' : ' + grbl_out.strip())

    def __del__(self):
        # Close file and serial port
        self.serial_instance.close()

c = MotorController()
c.move_magnet(5, 10)
time.sleep(6)
c.move_magnet(0, 0)