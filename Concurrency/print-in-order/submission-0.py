from threading import Event
class Foo:
    def __init__(self):
        self.done = (Event(), Event())

    def first(self, printFirst: 'Callable[[], None]') -> None:
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.done[0].set()

    def second(self, printSecond: 'Callable[[], None]') -> None:
        self.done[0].wait()
        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()
        self.done[1].set()

    def third(self, printThird: 'Callable[[], None]') -> None:
        self.done[1].wait()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()
