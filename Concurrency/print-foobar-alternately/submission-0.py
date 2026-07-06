from threading import Event
class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_printed = Event()
        self.bar_printed = Event()
        self.bar_printed.set()


    def foo(self, printFoo: 'Callable[[], None]') -> None:

        for i in range(self.n):
            self.bar_printed.wait()
            self.bar_printed.clear()
            # printFoo() outputs "foo". Do not change or remove this line.
            printFoo()
            self.foo_printed.set()


    def bar(self, printBar: 'Callable[[], None]') -> None:

        for i in range(self.n):
            self.foo_printed.wait()
            self.foo_printed.clear()
            # printBar() outputs "bar". Do not change or remove this line.
            printBar()
            self.bar_printed.set()
