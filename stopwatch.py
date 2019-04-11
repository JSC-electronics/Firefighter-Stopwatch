import time


class StopWatch(object):
    __times = []

    def start_watch(self):
        self.__times.append(time.time())

    def measure_split_time(self):
        self.__times.append(time.time())

    def print_times(self):
        if len(self.__times) <= 1:
            return

        start = self.__times[0]
        for idx in range(1, len(self.__times)):
            val = self.__times[idx]

            print('{}. mezicas: {}'.format(idx, val - start))

if __name__ == "__main__":
    stopwatch = StopWatch()
    stopwatch.start_watch()
    time.sleep(1)
    stopwatch.measure_split_time()
    stopwatch.print_times()
