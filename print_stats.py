from pybricks.hubs import PrimeHub
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
def get_spike_battery_percentage(hub, samples=5, delay=100):
    """
    Estimates SPIKE Prime battery percentage by averaging voltage readings.
    hub: instance of PrimeHub
    samples: number of readings to average
    delay: time between readings (ms)
    """
    min_mv = 6000   # 6.0V = 0%
    max_mv = 8200   # 8.2V = 100%
    total_mv = 0

    for _ in range(samples):
        mv = hub.battery.voltage()
        total_mv += mv
        wait(delay)

    avg_mv = total_mv / samples
    # Clamp to expected range
    avg_mv = max(min_mv, min(max_mv, avg_mv))
    percent = (avg_mv - min_mv) / (max_mv - min_mv) * 100
    return round(percent, 1)
hub = PrimeHub()
hold = Motor(Port.A, Direction.CLOCKWISE, reset_angle=False, profile=5)
move = Motor(Port.E, Direction.CLOCKWISE, reset_angle=False, profile=5)
battery_percent = get_spike_battery_percentage(hub)
while True:
    print("\n"*50)
    print(f"SPIKE Prime Battery: {battery_percent}%")
    print(f"Hold: {hold.angle()}")
    print(f"Move: {move.angle()}")
    wait(500)