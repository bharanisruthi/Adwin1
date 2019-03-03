
from AutoML3_sample_code_submission.ADBuckets import *


class ADBucketsList(object):
    """docstring for ADBucketsList."""
    def __init__(self,M=5, head=None):
        super(ADBucketsList, self).__init__()
        self.head = head
        self.M=M
        if self.head is None:
            self.head = ADBuckets(M+1,None,None)


    def addInputAtNextBucket(self,curr,next,value):
        if next is None:
            next = ADBucket(self.M+1,curr)

        next.buckets[next.count] = value
        next.sum+=value.content
        next.count+=1


    def checkForCompression(self,head):
        if head is None:
            return

        if head.count is self.M+1:
            b0=head.buckets[0]
            b1=head.buckets[1]

            compressedBucket = ADBucket(0,0.0)
            compressedBucket.content = b0.content + b1.content
            compressedBucket.capacity = b0.capacity+b1.capacity
            self.addInputAtNextBucket(head, head.next, compressedBucket)

            for i in range(self.M-2):
                head.buckets[i]= head.buckets[i+2]

            head.count-=2

        self.checkForCompression(head.next)

    def addAnInput(self, input):
        newBucket = ADBucket(1,input)
        self.head.buckets[self.head.count]= newBucket
        self.head.sum +=input
        self.head.count+=1
        self.checkForCompression(self.head)




    def deleteLastBucket(self):
        curr = self.head
        while curr.next is not None:
            curr = curr.next

        deletedBucket = curr
        curr.prev.next = None
        return deletedBucket