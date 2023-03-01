import time

class Time:
    time_started = time.time_ns()

    @classmethod
    def get_time(cls):
        return float((time.time_ns() - cls.time_started) * 1e-9)
