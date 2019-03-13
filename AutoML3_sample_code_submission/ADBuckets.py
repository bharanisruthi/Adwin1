
from AutoML3_sample_code_submission.ADBucket import ADBucket

class ADBuckets:

    def __init__(self,size=6,prev=None,next=None):
        self.size = size
        self.buckets = [None]*self.size
        self.prev = None
        self.next = None
        self.count=0
        self.sum =0.0
        self.squareSum=0.0
        self.level=0

        for i in range(size):
            self.buckets[i] = ADBucket(0,0)


        if prev is not None:
            self.prev = prev
            prev.next = self

        if next is not None:
            self.next = next
            next.prev = self

    def printBuckets(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for i in range(0,len(self.buckets)):
            print("bucket i content capacity",i,self.buckets[i].content,self.buckets[i].capacity)
        print("count,sum,level,squareSum:",self.count,self.sum,self.level,self.squareSum)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")



