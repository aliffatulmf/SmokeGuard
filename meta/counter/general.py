class CounterInt:
    def __init__(self):
        self.__count = 0

    def tap(self, increment=1):
        if not isinstance(increment, int) or increment < 0:
            raise ValueError("The increment value must be a positive integer")
        self.__count += increment

    def reset(self):
        self.__count = 0

    def size(self):
        return self.__count
