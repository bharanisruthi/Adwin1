
from AutoML3_sample_code_submission.ADBucket import ADBucket

class ADBuckets:

    def __init__(self,size=6,prev=None,next=None):
        self.size = size
        self.buckets = [None]*self.size
        self.prev = None
        self.next = None
        self.count=0
        self.sum =0.0

        for i in range(size):
            self.buckets[i] = ADBucket(0,0)


        if prev is not None:
            self.prev = prev
            prev.next = self

        if next is not None:
            self.next = next
            next.prev = self