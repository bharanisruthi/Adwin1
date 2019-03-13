from AutoML3_sample_code_submission.ADBuckets import *


class ADBucketsList(object):
    """docstring for ADBucketsList."""
    def __init__(self,M=6, head=None):
        super(ADBucketsList, self).__init__()
        self.head = head
        self.M=M
        self.level = 0
        if self.head is None:
            self.head = ADBuckets(M+1,None,None)


    def addInputAtNextBucket(self,curr,next,value):
        if next is None:
            self.level+=1
            next = ADBuckets(self.M+1,curr)
            next.level = value.capacity

        next.buckets[next.count] = value
        next.sum+=value.content
        next.count+=1
        next.squareSum+=value.square


    def checkForCompression(self,head):
        if head is None:
            return

        if head.count is self.M+1:
            b0=head.buckets[0]
            b1=head.buckets[1]

            compressedBucket = ADBucket(0,0.0)
            compressedBucket.content = b0.content + b1.content
            compressedBucket.capacity = b0.capacity+b1.capacity
            compressedBucket.square = b0.square+b1.square
            self.addInputAtNextBucket(head, head.next, compressedBucket)

            for i in range(self.M-1):
                head.buckets[i].content= head.buckets[i+2].content
                head.buckets[i].capacity = head.buckets[i + 2].capacity
                head.buckets[i].square = head.buckets[i+2].square
                head.buckets[i+2].content = 0.0
                head.buckets[i+2].capacity = 0
                head.buckets[i + 2].square = 0

            head.count-=2
            head.squareSum-=compressedBucket.square
            head.sum-=compressedBucket.content

        self.checkForCompression(head.next)

    def addAnInput(self, input):
        newBucket = ADBucket(1,input)
        self.head.buckets[self.head.count]= newBucket
        self.head.sum +=input
        self.head.count+=1
        self.head.squareSum+=pow(input,2)
        self.head.level = 1
        self.checkForCompression(self.head)




    def deleteLastBucket(self):
        curr = self.head
        while curr.next is not None:
            curr = curr.next

        deletedBucket = curr
        curr.prev.next = None
        return deletedBucket

    def printBuckets(self):
        n = self.head
        i = 0
        while (n is not None):
            print('i', i)
            n.printBuckets()
            n = n.next
            i += 1
