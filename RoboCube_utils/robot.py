# from mpdb import Mpdb

# def test():
#     a = 42
#     Mpdb().set_trace()  # Breakpoint here
#     print(a)

# test()

from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.hubs import PrimeHub
from pybricks.tools import wait, StopWatch
stopwatch = StopWatch()
stopwatch.resume()

hub = PrimeHub()  # If your broadcasting isn't working, consult this line
class Robot:
  def __init__(self):
    # Print initializing robot 
    print(("\n"*100)+"""___       _ _   _       _ _     _                         _          \n|_ _|_ __ (_) |_(_) __ _| (_)___(_)_ __   __ _   _ __ ___ | |__   ___ | |_ \n| || '_ \\| | __| |/ _` | | |_  / | '_ \\ / _` | | '__/ _ \\| '_ \\ / _ \\| __|\n| || | | | | |_| | (_| | | |/ /| | | | | (_| | | | | (_) | |_) | (_) | |_ \n|___|_| |_|_|\__|_|\__,_|_|_/___|_|_| |_|\__, | |_|  \___/|_.__/ \___/ \__|\n|___/                             """)
    # Turn off display
    hub.display.off()
    # Set the power button to red
    hub.light.on(Color.RED)
    # Boring stuff
    hub.system.set_stop_button(Button.BLUETOOTH)
    self.hold = Motor(Port.A, Direction.CLOCKWISE, reset_angle=False, profile=5)
    self.spin = Motor(Port.C, Direction.CLOCKWISE, reset_angle=False, profile=5)
    self.move = Motor(Port.E, Direction.CLOCKWISE, reset_angle=False, profile=5)
    self.holddown()
    self.spin.run_target(speed=100, target_angle=0, then=Stop.HOLD, wait=True)
    
    self.RED_CLOSE = Color(349, 90, 72)
    self.BLUE_CLOSE = Color(197, 84, 68)
    self.ORANGE_CLOSE = Color(358, 86, 92)
    self.GREEN_CLOSE = Color(125, 68, 61)
    self.YELLOW_CLOSE = Color(73, 62, 75)
    self.WHITE_CLOSE = Color(205, 17, 76)

    self.RED_MIDDLE = Color(348, 91, 37)
    self.BLUE_MIDDLE = Color(197, 84, 32)
    self.ORANGE_MIDDLE = Color(358, 87, 61)
    self.GREEN_MIDDLE = Color(125, 69, 36)
    self.YELLOW_MIDDLE = Color(71, 65, 45)
    self.WHITE_MIDDLE = Color(203, 19, 52)

    self.RED_FAR = Color(350, 90, 24)
    self.BLUE_FAR = Color(200, 80, 11)
    self.ORANGE_FAR = Color(358, 87, 26)
    self.GREEN_FAR = Color(130, 66, 9)
    self.YELLOW_FAR = Color(71, 62, 29)
    self.WHITE_FAR = Color(210, 15, 32)

    # Map all colors to their base names
    self.COLOR_MAP = {
      self.RED_CLOSE: "red",
      self.BLUE_CLOSE: "blue",
      self.ORANGE_CLOSE: "red",
      self.GREEN_CLOSE: "green",
      self.YELLOW_CLOSE: "yellow",
      self.WHITE_CLOSE: "white",
      self.RED_MIDDLE: "red",
      self.BLUE_MIDDLE: "blue",
      self.ORANGE_MIDDLE: "red",
      self.GREEN_MIDDLE: "green",
      self.YELLOW_MIDDLE: "yellow",
      self.WHITE_MIDDLE: "white",
      self.RED_FAR: "red",
      self.BLUE_FAR: "blue",
      self.ORANGE_FAR: "red",
      self.GREEN_FAR: "green",
      self.YELLOW_FAR: "yellow",
      self.WHITE_FAR: "white",
    }
    self.top_mid_sensor = ColorSensor(Port.B)
    self.top_right_sensor = ColorSensor(Port.D)
    self.mid_mid_sensor = ColorSensor(Port.F)
    sensors = [self.top_mid_sensor, self.top_right_sensor, self.mid_mid_sensor]
    for sensor in sensors:
      sensor.detectable_colors(colors=list(self.COLOR_MAP.keys()))

    self.XI_SPEED = 25 # Change if needed
    self.XI_SLEEP_MS = 300

  def holdup(self):
    timeout_ms = 1000  # Timeout in milliseconds
    start_time = stopwatch.time()

    while True:
      if stopwatch.time() - start_time > timeout_ms: break
      self.move.run_target(speed=100, target_angle=-50, then=Stop.HOLD, wait=True)
      self.hold.run_target(speed=100, target_angle=-35, then=Stop.HOLD, wait=True)
      wait(100)  # Avoid busy-waiting
    
  def holddown(self):
    self.hold.run_target(speed=100, target_angle=0, then=Stop.HOLD, wait=True)
    self.move.run_target(speed=100, target_angle=0, then=Stop.HOLD, wait=True)
  def turn_yi(self):
    self.spin.run_angle(speed=650, rotation_angle=90, then=Stop.HOLD, wait=True)
  def turn_Uw(self):
    self.holdup()
    self.turn_yi()
    
  def turn_xi(self):
    self.holddown()
    self.hold.run_target(speed=self.XI_SPEED, target_angle=-88, then=Stop.HOLD, wait=True)
    self.move.run_target(speed=self.XI_SPEED, target_angle=-15, then=Stop.HOLD, wait=True)
    self.holddown()
    self.hold.run_target(speed=self.XI_SPEED, target_angle=-21, then=Stop.HOLD, wait=True)
    self.move.run_target(speed=self.XI_SPEED, target_angle=-25, then=Stop.HOLD, wait=True)
    self.hold.run_target(speed=self.XI_SPEED, target_angle=-38, then=Stop.HOLD, wait=True)
    self.move.run_target(speed=self.XI_SPEED, target_angle=-42, then=Stop.HOLD, wait=True)
    self.hold.run_target(speed=self.XI_SPEED, target_angle=-58, then=Stop.HOLD, wait=True)
    self.move.run_target(speed=self.XI_SPEED, target_angle=16, then=Stop.HOLD, wait=True)
    self.holdup()
    self.holddown()


  def check_color(self, sensor):
    # Detect and print the base color name
    detected_color = sensor.color()
    detected_hsv = sensor.hsv()
    if not detected_color in self.COLOR_MAP:
      assert "NOOOO! JEDI FOUND OUR STASH OF UNOFFICIAL LEGO FIRMWARE!"
    formatted_color = self.COLOR_MAP[detected_color]
    if formatted_color == "red" and detected_hsv[0]>355:
      formatted_color = "orange"
    return formatted_color
  def set_power_color(self, color):
    color = eval("Color." + color.upper())
    hub.light.on(color)





# Spin zero is when the spin is aligned 90 degrees
# Move zero is marked when the two parallel black pieces are vertical
# Hold zero is marked when the light blue piece is verticalP
robot = Robot()