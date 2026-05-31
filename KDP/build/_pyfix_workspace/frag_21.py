import time


class Breaker:
    fail = 0
    opened_at = 0
    STATE = "closed"

    def call(self, fn, *a):
        if self.STATE == "open":
            if time.time() - self.opened_at < 30:
                raise OpenError
            self.STATE = "half_open"
        try:
            r = fn(*a)
            self.fail = 0
            self.STATE = "closed"
            return r
        except Exception:
            self.fail += 1
            if self.fail >= 5:
                self.STATE = "open"
                self.opened_at = time.time()
            raise
