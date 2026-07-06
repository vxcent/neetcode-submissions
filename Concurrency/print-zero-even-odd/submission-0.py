from threading import Semaphore

# we need to print zeros before calling odd/even
# we assume the program starts from zero, then odd, then even as sequence
# each thread runs its own range, so the counts fall out naturally:
#   zero prints n times; odd prints ceil(n/2) times; even prints floor(n/2)
class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n

        self.zero_turn = Semaphore(1)
        self.odd_turn = Semaphore(0)
        self.even_turn = Semaphore(0)

    # printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(1, self.n + 1):
            self.zero_turn.acquire()
            printNumber(0)
            if i % 2 == 1:
                self.odd_turn.release()
            else:
                self.even_turn.release()

    def even(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(2, self.n + 1, 2):
            self.even_turn.acquire()
            printNumber(i)
            self.zero_turn.release()

    def odd(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(1, self.n + 1, 2):
            self.odd_turn.acquire()
            printNumber(i)
            self.zero_turn.release()
