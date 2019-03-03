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
        self.M = 5
        self.adBucketsList = None
        self.windowSum = 0

    def epsilon(self,n0,n1,delta):
        harmonic_mean = (stats.hmean([ n0 , n1 ]))/(n0+n1)
        deltaDash = delta/math.sum(n0,n1)
        epsiloncut = math.sqrt((1/2*harmonic_mean)*math.log(4/deltaDash))
        return epsiloncut

    def isChangeDetected(self):
        isChanged = False
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
                while not isExit and buckets.prev is not None:
                        bucketsList = buckets.buckets
                        for i in range(buckets.count()-1,-1,-1):
                            n0 += bucketsList[i].capacity
                            n1 += bucketsList[i].capacity
                            sum0 += bucketsList[i].content
                            sum1 += bucketsList[i].content
                            mudiff=0.0
                            if n1 !=0 and n0!=0:
                                mudiff = (sum0 / n0) - (sum1 / n1)
                            if n0 > self.minWindowLength  and n1 > self.minWindowLength and self.epsilon(n0, n1, mudiff):
                                deletedBucket = self.adBucketsList.deleteLastBucket()
                                self.windowLength -= deletedBucket.count()
                                self.windowSum -= deletedBucket.sum
                                isChanged = True
                                isExit = True
                                reducedWindowLengthFlag = True
                                break
                        buckets = buckets.prev        
            return isChanged




    def insertInput(self, value):
        if self.adBucketsList is None:
            self.adBucketsList = ADBucketsList()
        self.adBucketsList.addAnInput(value)
        self.windowLength+=1
        self.t+=1
        self.windowSum+=value
        winDowMean = self.windowSum / self.windowLength
        return self.isChangeDetected()
