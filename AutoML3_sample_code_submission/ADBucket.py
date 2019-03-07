class ADBucket(object):
    """docstring for ADBucket."""

    def __init__(self, capacity=0, content=0.0):
        super(ADBucket, self).__init__()
        self.capacity = capacity
        self.content = content


    def incCapacity(self):
        self.capacity+=1