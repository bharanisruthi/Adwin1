class ADBucket(object):
   """create a new Bucket."""

    def __init__(self, capacity=0, content=0.0):
        
        """
        capacity: number of buckets which are aggregating
        content: Sum of elements in the bucket
        """
        
        super(ADBucket, self).__init__()
        self.capacity = capacity
        self.content = content
        self.square  = pow(content,2)


    def incCapacity(self):
        self.capacity+=1
