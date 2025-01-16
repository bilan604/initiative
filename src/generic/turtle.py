from datetime import datetime

from src.generic.loader import get_env_variable


DEVELOPMENT = get_env_variable('DEVELOPMENT')


class Turtle(object):
    # A rate-limiter on operations. A guard turtle?
    def __init__(self, shell=1):  
        self.prev = datetime.now()
        self.shell = 0.1  # A fast-ish turtle. Shell is the global time between any operations. Shell. Get it? Shell protec?
        self.PREV = {}
        self.SHELL = {'doThis': 10}  # Map[str, int]: add an operation for a increased delay.
    
    def get_seconds_between_datetimes(self, datetime1, datetime2):
        timedelta = datetime2 - datetime1
        seconds = timedelta.total_seconds()
        return abs(int(seconds))

    def update(self):
        now = datetime.now()    
        self.prev = now
        return    

    def updateOperation(self, operation):
        now = datetime.now()
        self.update()
        self.PREV[operation] = now
        return    

    def getGlobalSince(self):
        now = datetime.now()
        return self.get_seconds_between_datetimes(self.prev, now)

    def getSince(self, operation) -> int:
        if operation not in self.PREV:
            return 9999999  # should be infinite technically. Unless this code is being run from the 5-th dimension.
        now = datetime.now()
        return self.get_seconds_between_datetimes(self.PREV[operation], now)

    def getRemaining(self, operation):
        if operation not in self.SHELL:
            cooldown = self.shell
        else:
            cooldown = self.SHELL[operation]
        return cooldown - self.getSince(operation)

    def can(self):
        if self.getGlobalSince() >= self.shell:
            return True
        return False

    def canOperate(self, operation):
        if self.getRemaining(operation) <= 0:
            return True
        return False
    
    def __tutorial__(self):
        s = """
################
# example usage A
turtle = Turtle()

for i in range(1000000000):
    if turtle.can():
        if DEVELOPMENT == 'TRUE': print("SPAM SPAM SPAM")
        turtle.update()

################
# example usage B
turtle = Turtle()

for i in range(1000000000):
    if turtle.canOperate('doThis'):
        if DEVELOPMENT == 'TRUE': print("SPAM SPAM SPAM")
        turtle.updateOperation('doThis')
        """
        return s


