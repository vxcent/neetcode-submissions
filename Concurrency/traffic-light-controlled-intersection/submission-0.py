from threading import Lock

class TrafficLight:
    def __init__(self):
        self.greenroad = 1        # which road currently has the green light
        self.lock = Lock()

    def carArrived(
        self,
        carId: int,                      # ID of the car
        roadId: int,                     # road the car travels on: 1 (A) or 2 (B)
        direction: int,                  # direction of the car
        turnGreen: 'Callable[[], None]', # turn the light green on the car's road
        crossCar: 'Callable[[], None]'   # make the car cross
    ) -> None:
        # The lock makes "check the light, switch if needed, cross" one atomic
        # step, so only one car crosses at a time and no car crosses on red.
        with self.lock:
            if self.greenroad != roadId:
                turnGreen()               # perform the switch, not just record it
                self.greenroad = roadId
            crossCar()
