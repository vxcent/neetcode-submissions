from threading import Semaphore

# 5 forks, each a Semaphore(1) — a fork can be held by one philosopher at a time.
# Which forks a philosopher needs is fixed by their index (left = i, right = i+1 mod 5).
# The deadlock (all 5 grab their left fork, then wait forever on the right) is broken
# by allowed_to_eat: at most 2 philosophers may enter the fork-taking section at once,
# so a full 5-way circular wait can never form.
class DiningPhilosophers:
    def __init__(self):
        self.forks = [Semaphore(1) for _ in range(5)]
        self.allowed_to_eat = Semaphore(2)

    # call the functions directly to execute, for example, eat()
    # Given a philo, first determine their left and right:
    #   0 -> 0,1   1 -> 1,2   2 -> 2,3   3 -> 3,4   4 -> 4,0
    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:
        left_fork, right_fork = self.getLeftandRightForks(philosopher)
        self.allowed_to_eat.acquire()
        self.forks[left_fork].acquire()
        self.forks[right_fork].acquire()
        pickLeftFork()
        pickRightFork()
        eat()
        putLeftFork()
        putRightFork()
        self.forks[left_fork].release()
        self.forks[right_fork].release()
        self.allowed_to_eat.release()

    # Map philosopher id to fork ids, which match the semaphore indices.
    def getLeftandRightForks(self, philosopher):
        left_fork = philosopher
        right_fork = (philosopher + 1) % 5
        return left_fork, right_fork
