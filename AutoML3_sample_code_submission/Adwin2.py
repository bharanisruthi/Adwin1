'''
To detect concept drift in a changing data we have used the algorithm stated in: 
Learning from Time-Changing Data with Adaptive Windowing, Albert Bifet and Ricard Gavald`
Link: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.144.2279&rep=rep1&type=pdf

The fundamental principle of the algorithm is that, we divide the data in two windows 
and if we see the distribution of the data in the two windows more than a certain threshold that means that the algorithm
identifies that they belong to two different distributions and detect a concept drift.

The threshold value is called epsilon cut. It is determined by the following formula
m =1/(1/n0 + 1/n1) (harmonic mean of n0 and n1), where n0 and n1 are the sub window sizes
δ0 =δ/n (Delta is the confidence value) and n is the length of the window
epsilon cut =sqrt(2/m * window_variance * ln(2/δ0))+ 2/(3m) * window_variance * ln(2/δ0)

How the input is stored:
    We store the input in buckets, that store the content and capacity. Content is the sum of real numbers 
    and capacity tells us how many real numbers are aggregated in a bucket.
    
    The buckets are set in different levels of pow(2,i) from i=0
    
    We also define a parameter, M , it is used to tune the memory utilization. Here we have used M=5. 
    It means at a level i, we can only have 5 buckets. In case, it exceeds we aggregate the oldest buckets to next level.
    
    After that we start from window sizes,  n0= lastbucketlength n1 = (windowlength- lastbucket length) and find epsilon cut. 
    We continue this step, by increasing n0 by adding another bucket to the first sub window and decreasing n1 by 1 bukcet.
    If we find concept drift, we delete the buckets in oldest level.
    
    Below is an example of the algorithm:
    Inputs: [1,2,3,4] for t = t0 to t3. and M=2
        For t0:
            Input = 1
            content:[1]
            capcity:[1]
        For t1:
            Input = 2
            content:[1][2]
            capcity:[1][1]
        For t2:
            Input = 3
            content:[1][2][3]
            capcity:[1][1][1]
            Since M=2 , we compress the oldest two buckets
            content:[3] [3]
            capcity:[1] [2]
        For t3:
            Input = 4
            content:[3][4] [3]
            capcity:[1][1] [2]
            If we , detect change the delete the oldest bucket
            So, the window would be
            content:[3][4]
            capcity:[1][1]
            

Calculating varaince:
Let us say we are calculating varaince of {x1,x2,x3} with mean x
it would be sd-sq = (pow((x1-x),2)+pow((x2-x),2)+pow((x3-x),2))/(n-1) here n=3
= (3(pow(x,2))+pow(x1,2)+pow(x2,2)+pow(x3,2)-2*x*(x1+x2+x3))/(3-1)

Inorder to compute the above equation, at the time of storing inputs
we also store the  square and square sum
So, generalizing the numerator for every level the varaince would be
(content*bucketcount(pow(x,2))+pow(x1,2)+pow(x2,2)+pow(x3,2)..+pow(xn,2)-2*x*(bucketsum))
where  is the window_mean

'''


import math
from AutoML3_sample_code_submission.ADBucketsList import *

class Adwin2:
    def __init__(self, delta=0.002, max_buckets=5, min_clock=32, min_win_len=10, min_sub_win_len=5):
        self.windowLength = 0
        self.minSubWindowLength = min_sub_win_len
        self.t=0
        self.minT = min_clock
        self.delta = delta
        self.minWindowLength = min_win_len
        self.M = max_buckets
        self.adBucketsList = None
        self.windowSum = 0

    def calculateVariance(self):
        t = self.adBucketsList.head
        variance = 0.0
        mean = self.windowSum / self.windowLength
        while t is not None:
            variance += (t.count * t.level) * pow(mean, 2) + t.squareSum - (2*mean*t.sum)
            t = t.next
        return variance / (self.windowLength - 1)


    def insertInput(self, value):
        if self.adBucketsList is None:
            self.adBucketsList = ADBucketsList()
        self.windowLength += 1
        self.t += 1
        self.windowSum += value
        self.adBucketsList.addAnInput(value)
        return self.isChangeDetected()

    def epsilon(self,n0,n1,delta):
        m = 1.0 / ((1.0 / n0) + (1.0 / n1))
        deltaDash = abs(delta)/(n0+n1)
        if deltaDash == 0:
            return False
        else:
            logValue = float(math.log((2 /deltaDash)))
            print("logValue",logValue)
            winVariance = self.calculateVariance()
            print("winVariance",winVariance)
            epsiloncut = math.sqrt((2 / m) * winVariance * logValue) + ((2 / (3 * m)) * logValue)
            print("epsiloncut",epsiloncut)
            return abs(delta) > epsiloncut

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
                j = self.adBucketsList.level
                while not isExit and buckets.prev is not None:
                        bucketsList = buckets.buckets
                        for i in range(buckets.count-1,-1,-1):
                            n0 += bucketsList[i].capacity
                            n1 -= bucketsList[i].capacity
                           
                            sum0 += bucketsList[i].content
                            sum1 -= bucketsList[i].content
                          
                            #mudiff=0.0
                            if n1 is not 0 and n0 is not 0:
                                mudiff = (sum0 / n0) - (sum1 / n1)
                            if self.t% self.minT ==0 and n0 > self.minWindowLength  and n1 > self.minWindowLength and self.epsilon(n0, n1, mudiff):
                                deletedBucket = self.adBucketsList.deleteLastBucket()
                                self.windowLength -= deletedBucket.count
                                self.windowSum -= deletedBucket.sum
                                isChanged = True
                                isExit = True
                                reducedWindowLengthFlag = True
                                break
                        buckets = buckets.prev

        return isChanged








