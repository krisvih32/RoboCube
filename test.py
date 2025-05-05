from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
hold = Motor(Port.A, Direction.CLOCKWISE, reset_angle=False, profile=5)
spin = Motor(Port.C, Direction.CLOCKWISE, reset_angle=False, profile=5)
move = Motor(Port.E, Direction.CLOCKWISE, reset_angle=False, profile=5)
print("Hold: ", hold.angle(), "Spin: ", spin.angle(), "Move: ", move.angle())