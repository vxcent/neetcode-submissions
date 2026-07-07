from threading import Semaphore


# Hierarchy of execution:
#   test fizzbuzz (%15) first, then buzz (%5), then fizz (%3), else the number.
# `number` is the single dispatcher: it walks 1..n and, per value, releases
# exactly ONE worker's semaphore then blocks on `done_turn` until it finishes.
# No Barrier needed because only one worker executes per number.
class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        self.fizzbuzz_turn = Semaphore(0)
        self.buzz_turn = Semaphore(0)
        self.fizz_turn = Semaphore(0)
        self.done_turn = Semaphore(0)

    # printFizz() outputs "fizz"
    def fizz(self, printFizz: 'Callable[[], None]') -> None:
        for i in range(3, self.n + 1, 3):
            if i % 5 != 0:
                self.fizz_turn.acquire()
                printFizz()
                self.done_turn.release()

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz: 'Callable[[], None]') -> None:
        for i in range(5, self.n + 1, 5):
            if i % 3 != 0:
                self.buzz_turn.acquire()
                printBuzz()
                self.done_turn.release()

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz: 'Callable[[], None]') -> None:
        for i in range(15, self.n + 1, 15):
            self.fizzbuzz_turn.acquire()
            printFizzBuzz()
            self.done_turn.release()

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber: 'Callable[[int], None]') -> None:
        for i in range(1, self.n + 1):
            if i % 15 == 0:
                self.fizzbuzz_turn.release()
                self.done_turn.acquire()
            elif i % 5 == 0:
                self.buzz_turn.release()
                self.done_turn.acquire()
            elif i % 3 == 0:
                self.fizz_turn.release()
                self.done_turn.acquire()
            else:
                printNumber(i)
