from RoboCube_utils.robot import robot
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Stop, Button, Color
print("Import finished")
#robot.holdup()
#
while True:
  for i in range(4):
    robot.turn_yi()
    if robot.check_color(robot.mid_mid_sensor) == "white":
      break
  if i == 4:
    print("The color is on top or bottom")
    robot.turn_xi()
    if robot.check_color(robot.mid_mid_sensor) == "white":
      print("White is on back, xi to get white on top")
      robot.turn_xi()
    else:
      print("White is on front, y2 to get white on bottom")
      robot.turn_yi()
      robot.turn_yi()
      print("White is on back, xi to get white on top")
      robot.turn_xi()
  else:
    print("The color is on the back, xi to get it on top")
    robot.turn_xi()