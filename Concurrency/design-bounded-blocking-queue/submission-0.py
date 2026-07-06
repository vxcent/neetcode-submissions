from collections import deque
from threading import Semaphore, Lock


class BoundedBlockingQueue(object):

    def __init__(self, capacity: int):
        self.empty_spots = Semaphore(capacity)
        self.queue = deque()
        self.filled_spots = Semaphore(0)
        self.lock = Lock()

    def enqueue(self, element: int) -> None:
        self.empty_spots.acquire()
        with self.lock:
            self.queue.append(element)
        self.filled_spots.release()

    def dequeue(self) -> int:
        self.filled_spots.acquire()
        with self.lock:
            value = self.queue.popleft()
        self.empty_spots.release()
        return value

    def size(self) -> int:
        with self.lock:
            return len(self.queue)
