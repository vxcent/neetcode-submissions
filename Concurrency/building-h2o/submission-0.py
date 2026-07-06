from threading import Semaphore
from threading import Barrier

class H2O:
    def __init__(self):
        self.h_turn = Semaphore(2)
        self.oxygen_turn = Semaphore(1)
        self.water_barrier = Barrier(3)

    def hydrogen(self, releaseHydrogen: 'Callable[[], None]') -> None:
        self.h_turn.acquire()
        # releaseHydrogen() outputs "H". Do not change or remove this line.
        self.water_barrier.wait()
        releaseHydrogen()
        self.h_turn.release()

    def oxygen(self, releaseOxygen: 'Callable[[], None]') -> None:
        # releaseOxygen() outputs "O". Do not change or remove this line.
        self.oxygen_turn.acquire()
        self.water_barrier.wait()
        releaseOxygen()
        self.oxygen_turn.release()
