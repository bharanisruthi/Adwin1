import math
from scipy import stats
from AutoML3_sample_code_submission.ADBucketsList import *

class Adwin2:
    def __init__(self, delta=0.002, max_buckets=5, min_clock=32, min_win_len=10, min_sub_win_len=5):
        self.windowLength = 0
        self.minSubWindowLength = 5
        self.t=0
        self.minT = 35
        self.delta = 0.02
        self.minWindowLength = 10
        self.M = 2
        self.adBucketsList = None
        self.windowSum = 0

    def insertInput(self, value):
        if self.adBucketsList is None:
            self.adBucketsList = ADBucketsList()
        self.windowLength += 1
        self.t += 1
        self.windowSum += value
        self.adBucketsList.addAnInput(value)
        winDowMean = self.windowSum / self.windowLength
        print()
        return self.isChangeDetected()

    def epsilon(self,n0,n1,delta):
        m = 1.0 / ((1.0 / n0) + (1.0 / n1))
        deltaDash = abs(delta)/(n0+n1)
        logValue = math.log((4 /deltaDash))
        epsiloncut = math.sqrt((1/(2*m))*logValue)
        print("epsiloncut",epsiloncut)
        return abs(delta) > epsiloncut

    def isChangeDetected(self):
        isChanged = False
        print('--------------------------------------------------------------------------')
        print('t:', self.t)
        print('windowLength:', self.windowLength)
        self.adBucketsList.printBuckets()
        print('--------------------------------------------------------------------------')
        if (self.t % self.minT == 0 and self.windowLength >= self.minWindowLength):
            reducedWindowLengthFlag = True
            while (reducedWindowLengthFlag):
                reducedWindowLengthFlag = False
                n0 = 0
                n1 = self.windowLength
                sum0 = 0
                sum1 = self.windowSum
                buckets = self.adBucketsList.head
                while buckets.next is not None:
                    buckets = buckets.next
                isExit = False
                j = self.adBucketsList.level
                while not isExit and buckets.prev is not None:
                        bucketsList = buckets.buckets
                        for i in range(buckets.count-1,-1,-1):
                            n0 += bucketsList[i].capacity
                            n1 -= bucketsList[i].capacity
                            print("n0",n0)
                            print("n1",n1)
                            sum0 += bucketsList[i].content
                            sum1 -= bucketsList[i].content
                            print("sum0", sum0)
                            print("sum1", sum1)
                            #mudiff=0.0
                            if n1 is not 0 and n0 is not 0:
                                mudiff = (sum0 / n0) - (sum1 / n1)
                            if n0 > self.minWindowLength  and n1 > self.minWindowLength and self.epsilon(n0, n1, mudiff):
                                deletedBucket = self.adBucketsList.deleteLastBucket()
                                self.windowLength -= deletedBucket.count
                                self.windowSum -= deletedBucket.sum
                                isChanged = True
                                isExit = True
                                reducedWindowLengthFlag = True
                                break
                        buckets = buckets.prev

        return isChanged








